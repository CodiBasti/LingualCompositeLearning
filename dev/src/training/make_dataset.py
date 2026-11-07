"""
Dataset Generator for Latent Concept Grounding Experiments.
Generates:
1. 500 SFT demonstrations formatted identically for:
   - Arm C: Natural conditioning tag ([SAFE_APPROACH_COMPLIANT])
   - Arm D: Concept token conditioning (<|c:fufu_weli|>)
   - Arm E: Arbitrary control token conditioning (<|mode_42|>)
2. 100 standardized test evaluation benchmark episodes across the 4 domains.

Saves clean JSONL datasets to `dev/data/latent_grounding/`.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List

from dev.src.simulation.scenarios import (
    generate_training_demonstrations,
    generate_benchmark_suite,
    format_scenario_prompt,
    plan_to_yaml_str,
)


OUTPUT_DIR = Path("dev/data/latent_grounding")


def build_and_save_datasets(
    num_train: int = 500,
    num_test: int = 100,
    train_seed: int = 1337,
    test_seed: int = 42,
    output_dir: Path = OUTPUT_DIR,
) -> Dict[str, str]:
    """
    Builds training and evaluation datasets and writes them to disk.
    Returns dictionary of generated file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {num_train} training demonstrations (seed={train_seed})...")
    train_episodes = generate_training_demonstrations(num_episodes=num_train, seed=train_seed)

    print(f"Generating {num_test} benchmark evaluation episodes (seed={test_seed})...")
    test_episodes = generate_benchmark_suite(num_episodes=num_test, seed=test_seed)

    # 1. Format Arm C (Natural SFT)
    arm_c_path = output_dir / "train_arm_c_natural.jsonl"
    with open(arm_c_path, "w", encoding="utf-8") as f:
        for cfg, gt_plan in train_episodes:
            prompt = format_scenario_prompt(cfg, "Arm_C_Natural_SFT")
            assistant_content = plan_to_yaml_str(gt_plan)
            record = {
                "scenario_id": cfg.scenario_id,
                "domain": cfg.domain,
                "arm": "Arm_C_Natural_SFT",
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                    {"role": "assistant", "content": assistant_content},
                ],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 2. Format Arm D (Concept SFT)
    arm_d_path = output_dir / "train_arm_d_concept.jsonl"
    with open(arm_d_path, "w", encoding="utf-8") as f:
        for cfg, gt_plan in train_episodes:
            prompt = format_scenario_prompt(cfg, "Arm_D_Concept_SFT")
            assistant_content = plan_to_yaml_str(gt_plan)
            record = {
                "scenario_id": cfg.scenario_id,
                "domain": cfg.domain,
                "arm": "Arm_D_Concept_SFT",
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                    {"role": "assistant", "content": assistant_content},
                ],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 3. Format Arm E (Arbitrary Control Token SFT)
    arm_e_path = output_dir / "train_arm_e_arbitrary.jsonl"
    with open(arm_e_path, "w", encoding="utf-8") as f:
        for cfg, gt_plan in train_episodes:
            prompt = format_scenario_prompt(cfg, "Arm_E_Arbitrary_SFT")
            assistant_content = plan_to_yaml_str(gt_plan)
            record = {
                "scenario_id": cfg.scenario_id,
                "domain": cfg.domain,
                "arm": "Arm_E_Arbitrary_SFT",
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                    {"role": "assistant", "content": assistant_content},
                ],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 4. Format 100 Benchmark Test Evaluation Episodes
    test_path = output_dir / "benchmark_test_100.jsonl"
    with open(test_path, "w", encoding="utf-8") as f:
        for cfg, gt_plan in test_episodes:
            # Serialize configuration and ground-truth plan for reproducible re-evaluation
            record = {
                "scenario_id": cfg.scenario_id,
                "domain": cfg.domain,
                "description": cfg.description,
                "urgent_command": cfg.urgent_command,
                "robot_start": cfg.robot_start,
                "destination_human": cfg.destination_human,
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
                "ground_truth_plan": [
                    {
                        "action_type": p.action_type,
                        "target": p.target,
                        "clearance": p.clearance,
                        "speed_limit": p.speed_limit,
                        "max_force": p.max_force,
                        "max_accel": p.max_accel,
                        "wait_condition": p.wait_condition,
                    }
                    for p in gt_plan
                ],
                "prompts": {
                    "Arm_A_Naive": format_scenario_prompt(cfg, "Arm_A_Naive"),
                    "Arm_B_CoT": format_scenario_prompt(cfg, "Arm_B_CoT"),
                    "Arm_C_Natural_SFT": format_scenario_prompt(cfg, "Arm_C_Natural_SFT"),
                    "Arm_D_Concept_SFT": format_scenario_prompt(cfg, "Arm_D_Concept_SFT"),
                    "Arm_E_Arbitrary_SFT": format_scenario_prompt(cfg, "Arm_E_Arbitrary_SFT"),
                },
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Datasets successfully written to {output_dir}:")
    print(f"  - Arm C (Natural SFT): {arm_c_path} ({num_train} samples)")
    print(f"  - Arm D (Concept SFT): {arm_d_path} ({num_train} samples)")
    print(f"  - Arm E (Arbitrary SFT): {arm_e_path} ({num_train} samples)")
    print(f"  - Benchmark Test 100: {test_path} ({num_test} episodes)")

    return {
        "arm_c": str(arm_c_path),
        "arm_d": str(arm_d_path),
        "arm_e": str(arm_e_path),
        "benchmark_test": str(test_path),
    }


if __name__ == "__main__":
    build_and_save_datasets()

