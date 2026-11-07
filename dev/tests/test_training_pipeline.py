"""
Unit tests for Training & Evaluation Pipeline:
1. Verifies that SFTDataset properly masks prompt tokens with -100 (assistant-only loss).
2. Verifies dynamic batch collation and padding.
3. Verifies scenario reconstruction from JSON records.
"""

import unittest
import json
import tempfile
from pathlib import Path
from transformers import AutoTokenizer

from dev.src.training.train_lora import SFTDataset, collate_fn, SPECIAL_TOKENS
from dev.src.evaluation.benchmark_runner import reconstruct_scenario_config
from dev.src.simulation.scenarios import generate_scenario, format_scenario_prompt, plan_to_yaml_str


class TestTrainingPipeline(unittest.TestCase):

    def test_reconstruct_scenario_config(self):
        """Reconstructed scenario config matches original kinematics."""
        cfg, gt_plan = generate_scenario(seed=999, domain="ClinicalCare", episode_idx=5)
        record = {
            "scenario_id": cfg.scenario_id,
            "domain": cfg.domain,
            "description": cfg.description,
            "urgent_command": cfg.urgent_command,
            "robot_start": list(cfg.robot_start),
            "destination_human": list(cfg.destination_human),
            "target_object": {
                "name": cfg.target_object.name,
                "x": cfg.target_object.x,
                "y": cfg.target_object.y,
                "is_fragile": cfg.target_object.is_fragile,
                "is_hot": cfg.target_object.is_hot,
                "max_safe_force": cfg.target_object.max_safe_force,
                "max_safe_accel": cfg.target_object.max_safe_accel,
            },
            "hazards": [
                {
                    "name": h.name,
                    "x": h.x,
                    "y": h.y,
                    "vx": h.vx,
                    "vy": h.vy,
                    "radius": h.radius,
                    "is_vulnerable": h.is_vulnerable,
                    "min_safe_clearance": h.min_safe_clearance,
                }
                for h in cfg.hazards
            ],
        }

        reconstructed = reconstruct_scenario_config(record)
        self.assertEqual(reconstructed.scenario_id, cfg.scenario_id)
        self.assertEqual(reconstructed.domain, cfg.domain)
        self.assertEqual(reconstructed.target_object.name, cfg.target_object.name)
        self.assertEqual(len(reconstructed.hazards), len(cfg.hazards))
        self.assertEqual(reconstructed.hazards[0].name, cfg.hazards[0].name)
        self.assertEqual(reconstructed.hazards[0].min_safe_clearance, cfg.hazards[0].min_safe_clearance)

    def test_sft_dataset_prompt_masking(self):
        """Prompt tokens must be masked with -100 so loss is computed solely on the assistant plan."""
        # Use Qwen2.5-14B tokenizer which is locally cached
        tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-14B-Instruct", local_files_only=True)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token

        cfg, gt_plan = generate_scenario(seed=123, domain="Domestic", episode_idx=0)
        prompt = format_scenario_prompt(cfg, "Arm_D_Concept_SFT")
        assistant_content = plan_to_yaml_str(gt_plan)

        sample = {
            "scenario_id": cfg.scenario_id,
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
                {"role": "assistant", "content": assistant_content},
            ],
        }

        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
            f.write(json.dumps(sample) + "\n")
            temp_path = f.name

        try:
            ds = SFTDataset(temp_path, tok, max_seq_length=1024)
            self.assertEqual(len(ds), 1)
            item = ds[0]

            labels = item["labels"]
            input_ids = item["input_ids"]

            # Prompt tokens should be -100
            self.assertIn(-100, labels)
            # Assistant tokens should NOT be -100
            non_masked_labels = [l for l in labels if l != -100]
            self.assertGreater(len(non_masked_labels), 10)

            # Masked labels must precede non-masked labels
            first_unmasked_idx = next(i for i, l in enumerate(labels) if l != -100)
            self.assertTrue(all(l == -100 for l in labels[:first_unmasked_idx]))
            self.assertTrue(all(l != -100 for l in labels[first_unmasked_idx:]))

            # Batch collation
            batch = collate_fn([item, item], tok.pad_token_id)
            self.assertEqual(batch["input_ids"].shape[0], 2)
            self.assertEqual(batch["attention_mask"].shape[0], 2)
            self.assertEqual(batch["labels"].shape[0], 2)

        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

