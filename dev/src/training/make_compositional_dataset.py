"""
Dataset Generator for Phase 6: Zero-Shot Compositional Latent Grounding.
Generates:
1. `dev/data/compositional/train_atomic_concept.jsonl` (600 episodes: 300 <|c:fufu|> + 300 <|c:weli|>)
2. `dev/data/compositional/train_atomic_arbitrary.jsonl` (600 episodes: 300 <|mode_A|> + 300 <|mode_B|>)
3. `dev/data/compositional/benchmark_dual_test_100.jsonl` (100 dual-constraint test episodes)
"""

import sys
import json
import random
from pathlib import Path
from typing import Dict, Any, List

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dev.src.simulation.compositional_scenarios import (
    DOMAINS,
    build_atomic_spatial_scenario,
    build_atomic_tactile_scenario,
    build_dual_benchmark_scenario,
    format_compositional_prompt,
)
from dev.src.simulation.scenarios import plan_to_yaml_str

OUTPUT_DIR = Path("dev/data/compositional")


def build_and_save_compositional_datasets(
    num_spatial: int = 300,
    num_tactile: int = 300,
    num_test: int = 100,
    train_seed: int = 42,
    test_seed: int = 999,
    output_dir: Path = OUTPUT_DIR,
) -> Dict[str, str]:
    """Builds and writes all Phase 6 training and benchmark datasets to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rng_train = random.Random(train_seed)

    print(f"Generating {num_spatial} atomic spatial episodes and {num_tactile} atomic tactile episodes...")

    # 1. Generate Atomic Spatial Episodes (<|c:fufu|> and <|mode_A|>)
    spatial_episodes = []
    for i in range(num_spatial):
        domain = DOMAINS[i % len(DOMAINS)]
        cfg, gt_plan = build_atomic_spatial_scenario(seed=train_seed + i * 997, domain=domain, ep_idx=i)
        spatial_episodes.append((cfg, gt_plan))

    # 2. Generate Atomic Tactile Episodes (<|c:weli|> and <|mode_B|>)
    tactile_episodes = []
    for i in range(num_tactile):
        domain = DOMAINS[i % len(DOMAINS)]
        cfg, gt_plan = build_atomic_tactile_scenario(seed=train_seed + 5000 + i * 997, domain=domain, ep_idx=i)
        tactile_episodes.append((cfg, gt_plan))

    # Format Concept Training Dataset (Disjoint 300 fufu + 300 weli)
    concept_records = []
    for cfg, gt_plan in spatial_episodes:
        prompt = format_compositional_prompt(cfg, prefix="<|c:fufu|>")
        assistant_content = plan_to_yaml_str(gt_plan)
        concept_records.append({
            "scenario_id": cfg.scenario_id,
            "concept_type": "atomic_spatial",
            "token": "<|c:fufu|>",
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
                {"role": "assistant", "content": assistant_content},
            ],
        })

    for cfg, gt_plan in tactile_episodes:
        prompt = format_compositional_prompt(cfg, prefix="<|c:weli|>")
        assistant_content = plan_to_yaml_str(gt_plan)
        concept_records.append({
            "scenario_id": cfg.scenario_id,
            "concept_type": "atomic_tactile",
            "token": "<|c:weli|>",
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
                {"role": "assistant", "content": assistant_content},
            ],
        })

    # Shuffle training set so fufu and weli are uniformly interleaved
    rng_train.shuffle(concept_records)
    train_concept_file = output_dir / "train_atomic_concept.jsonl"
    with open(train_concept_file, "w", encoding="utf-8") as f:
        for rec in concept_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Saved {len(concept_records)} concept training examples to {train_concept_file}")

    # Format Arbitrary Training Dataset (Disjoint 300 mode_A + 300 mode_B)
    arbitrary_records = []
    for cfg, gt_plan in spatial_episodes:
        prompt = format_compositional_prompt(cfg, prefix="<|mode_A|>")
        assistant_content = plan_to_yaml_str(gt_plan)
        arbitrary_records.append({
            "scenario_id": cfg.scenario_id,
            "concept_type": "atomic_spatial",
            "token": "<|mode_A|>",
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
                {"role": "assistant", "content": assistant_content},
            ],
        })

    for cfg, gt_plan in tactile_episodes:
        prompt = format_compositional_prompt(cfg, prefix="<|mode_B|>")
        assistant_content = plan_to_yaml_str(gt_plan)
        arbitrary_records.append({
            "scenario_id": cfg.scenario_id,
            "concept_type": "atomic_tactile",
            "token": "<|mode_B|>",
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
                {"role": "assistant", "content": assistant_content},
            ],
        })

    rng_train.shuffle(arbitrary_records)
    train_arbitrary_file = output_dir / "train_atomic_arbitrary.jsonl"
    with open(train_arbitrary_file, "w", encoding="utf-8") as f:
        for rec in arbitrary_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Saved {len(arbitrary_records)} arbitrary training examples to {train_arbitrary_file}")

    # 3. Generate 100 Dual-Constraint Benchmark Test Episodes
    print(f"Generating {num_test} dual-constraint test episodes (seed={test_seed})...")
    benchmark_records = []
    for i in range(num_test):
        domain = DOMAINS[i % len(DOMAINS)]
        cfg, gt_plan = build_dual_benchmark_scenario(seed=test_seed + i * 1013, domain=domain, ep_idx=i)

        prompts = {
            "Baseline_No_Token": format_compositional_prompt(cfg, prefix=""),
            "Solo_Fufu": format_compositional_prompt(cfg, prefix="<|c:fufu|>"),
            "Solo_Weli": format_compositional_prompt(cfg, prefix="<|c:weli|>"),
            "Comp_Fufu_Weli": format_compositional_prompt(cfg, prefix="<|c:fufu|> <|c:weli|>"),
            "Comp_Weli_Fufu": format_compositional_prompt(cfg, prefix="<|c:weli|> <|c:fufu|>"),
            "Comp_Arbitrary_AB": format_compositional_prompt(cfg, prefix="<|mode_A|> <|mode_B|>"),
        }

        rec = {
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
            "ground_truth_plan": [p.__dict__ for p in gt_plan],
            "prompts": prompts,
        }
        benchmark_records.append(rec)

    test_benchmark_file = output_dir / "benchmark_dual_test_100.jsonl"
    with open(test_benchmark_file, "w", encoding="utf-8") as f:
        for rec in benchmark_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Saved {len(benchmark_records)} dual-constraint benchmark episodes to {test_benchmark_file}")

    return {
        "train_concept": str(train_concept_file),
        "train_arbitrary": str(train_arbitrary_file),
        "test_benchmark": str(test_benchmark_file),
    }


if __name__ == "__main__":
    build_and_save_compositional_datasets()

