"""
Master Orchestration Script for Phase 5 Latent Concept Grounding Experiment.
Runs the end-to-end scientific pipeline:
1. Verifies dataset generation (500 train per arm, 100 benchmark test).
2. Executes LoRA fine-tuning for Arms C, D, and E with equalized hyperparameters.
3. Evaluates all 5 arms (Arm A, B, C, D, E) on the 100 standardized benchmark episodes in MiniWorld-2D.
4. Generates publication-ready comparative metrics table and reports.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dev.src.training.train_lora import train_lora_model
from dev.src.evaluation.benchmark_runner import evaluate_benchmark
from dev.src.training.make_dataset import build_and_save_datasets


RESULTS_DIR = Path("dev/results/latent_grounding")
MODELS_DIR = Path("dev/models")
DATA_DIR = Path("dev/data/latent_grounding")
REPORTS_DIR = Path("dev/reports")


def run_full_pipeline(
    base_model_name: str = "Qwen/Qwen2.5-3B-Instruct",
    epochs: int = 3,
    eval_limit: int = None,
    skip_training: bool = False,
    device: str = "cuda:0",
) -> Dict[str, Any]:
    """
    Executes the complete experimental pipeline across all 5 arms.
    """
    t_start = time.time()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*70)
    print("PHASE 5: LATENT CONCEPT GROUNDING EXPERIMENT PIPELINE")
    print(f"Base Model: {base_model_name}")
    print(f"Epochs: {epochs} | Device: {device} | Eval Limit: {eval_limit}")
    print("="*70 + "\n")

    # Step 1: Ensure datasets exist
    benchmark_file = DATA_DIR / "benchmark_test_100.jsonl"
    if not benchmark_file.exists():
        print("[Step 1] Generating training and benchmark datasets...")
        build_and_save_datasets()
    else:
        print("[Step 1] Verified existing datasets in", DATA_DIR)

    # Step 2: Fine-Tuning Arms C, D, E
    sft_arms = [
        ("Arm_C_Natural_SFT", DATA_DIR / "train_arm_c_natural.jsonl", MODELS_DIR / "lora_arm_c"),
        ("Arm_D_Concept_SFT", DATA_DIR / "train_arm_d_concept.jsonl", MODELS_DIR / "lora_arm_d"),
        ("Arm_E_Arbitrary_SFT", DATA_DIR / "train_arm_e_arbitrary.jsonl", MODELS_DIR / "lora_arm_e"),
    ]

    training_summaries = {}
    if not skip_training:
        for arm_name, data_p, model_p in sft_arms:
            summary_file = model_p / "training_summary.json"
            if summary_file.exists():
                print(f"[Step 2] Found existing checkpoint for {arm_name} at {model_p}. Skipping training.")
                with open(summary_file, "r") as f:
                    training_summaries[arm_name] = json.load(f)
            else:
                print(f"[Step 2] Training {arm_name}...")
                summary = train_lora_model(
                    arm=arm_name,
                    model_name=base_model_name,
                    data_path=str(data_p),
                    output_dir=str(model_p),
                    num_epochs=epochs,
                    device=device,
                )
                training_summaries[arm_name] = summary
    else:
        print("[Step 2] Skipping training as requested.")

    # Step 3: Run Benchmark Evaluations on all 5 Arms
    all_arms = [
        ("Arm_A_Naive", None),
        ("Arm_B_CoT", None),
        ("Arm_C_Natural_SFT", str(MODELS_DIR / "lora_arm_c")),
        ("Arm_D_Concept_SFT", str(MODELS_DIR / "lora_arm_d")),
        ("Arm_E_Arbitrary_SFT", str(MODELS_DIR / "lora_arm_e")),
    ]

    evaluation_summaries = {}
    for arm_name, adapter_p in all_arms:
        print(f"\n[Step 3] Evaluating {arm_name}...")
        eval_summary = evaluate_benchmark(
            arm=arm_name,
            base_model_name=base_model_name,
            adapter_dir=adapter_p,
            benchmark_file=str(benchmark_file),
            output_dir=str(RESULTS_DIR),
            max_episodes=eval_limit,
            device=device,
        )
        evaluation_summaries[arm_name] = eval_summary

    # Step 4: Generate Consolidated Markdown Report
    report_md = generate_consolidated_markdown(evaluation_summaries, base_model_name)
    report_path = REPORTS_DIR / "empirical_evaluation_phase5_latent_grounding.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print("\n" + "="*70)
    print("PHASE 5 COMPLETE!")
    print(f"Master Report generated at: {report_path}")
    print("="*70 + "\n")

    return evaluation_summaries


def generate_consolidated_markdown(results: Dict[str, Any], base_model: str) -> str:
    """Formats benchmark results into an empirical markdown research report."""
    md = f"""# Empirical Benchmark Evaluation: Latent Concept Grounding in MiniWorld-2D

**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Base Model:** `{base_model}`  
**Hardware:** NVIDIA GeForce RTX 5090 (32GB VRAM)  
**Evaluator:** Deterministic Kinematic Simulator (`MiniWorld-2D`) with Ground-Truth Numerical Physics  

---

## 1. Executive Summary & 5-Arm Comparative Results

| Metric | Arm A: Frozen Naive | Arm B: Frozen CoT (1024 tok) | Arm C: Natural SFT | Arm D: Concept SFT (`<|c:fufu_weli|>`) | Arm E: Arbitrary SFT (`<|mode_42|>`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
    arms = ["Arm_A_Naive", "Arm_B_CoT", "Arm_C_Natural_SFT", "Arm_D_Concept_SFT", "Arm_E_Arbitrary_SFT"]

    metrics = [
        ("Task Success Rate (%)", "task_success_rate", "{:.1f}%"),
        ("Safety Collision Rate (%)", "safety_collision_rate", "{:.1f}%"),
        ("Liquid Spill Rate (%)", "spill_violation_rate", "{:.1f}%"),
        ("Force Crushing Rate (%)", "force_violation_rate", "{:.1f}%"),
        ("Mean Tokens to EOS", "mean_tokens_generated", "{:.1f}"),
        ("Mean Latency (s)", "mean_latency_seconds", "{:.3f}s"),
        ("Mean Min Clearance (m)", "mean_min_hazard_distance", "{:.2f}m"),
        ("Mean Carrying Accel (m/s²)", "mean_carrying_acceleration", "{:.2f}"),
        ("Mean Grip Force (N)", "mean_grip_force", "{:.2f}N"),
    ]

    for label, key, fmt in metrics:
        row = [f"**{label}**"]
        for arm in arms:
            val = results.get(arm, {}).get(key, 0.0)
            row.append(fmt.format(val))
        md += "| " + " | ".join(row) + " |\n"

    md += """
---

## 2. Hypothesis Testing & Scientific Analysis

### H1: Latent Concept Grounding Eliminates CoT Verbosity Without Safety Degradation
- **Arm B (Chain-of-Thought)** articulates multi-paragraph reasoning steps before emitting the plan.
- **Arm D (Concept SFT)** conditions on `<|c:fufu_weli|>`, encapsulating *prudent navigation, clearance preservation, and liquid acceleration bounds*.
- **Token Efficiency Ratio:** Compares token budgets between Arm B and Arm D.

### H2: Concept Token Specificity vs. Arbitrary Symbol Control (Arm D vs. Arm E)
- **Arm E** conditions on `<|mode_42|>` with matched LoRA training capacity.
- Evaluates whether semantic concept grounding exhibits distinct generalization and stability compared to arbitrary token injection.

---

*Generated deterministically by `dev/src/evaluation/run_full_phase5_experiment.py`.*
"""
    return md


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 5 Experiment Orchestrator")
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-3B-Instruct")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--skip_training", action="store_true")

    args = parser.parse_args()

    run_full_pipeline(
        base_model_name=args.base_model,
        epochs=args.epochs,
        eval_limit=args.limit,
        skip_training=args.skip_training,
    )

