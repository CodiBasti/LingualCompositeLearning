"""
Standardized Benchmark Runner for Latent Concept Grounding Experiments.
Evaluates 5 Experimental Arms across 100 Multi-Domain Episodes in MiniWorld-2D:
- Arm A: Frozen Naive (Base model, zero reasoning prompt, 256 tok)
- Arm B: Frozen CoT (Base model, step-by-step reasoning directive, 1024 tok ceiling)
- Arm C: Natural SFT ([SAFE_APPROACH_COMPLIANT] tag, 1024 tok ceiling)
- Arm D: Concept SFT (<|c:fufu_weli|> concept token, 1024 tok ceiling)
- Arm E: Arbitrary SFT (<|mode_42|> control token, 1024 tok ceiling)

Records:
- Ground-truth physics metrics: Task Success, Collision Rate, Spill Rate, Force Rate
- Continuous kinematics: Min Hazard Distance, Max Carrying Accel, Max Grip Force
- Computational efficiency: Actual Tokens Generated to EOS, Inference Latency
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from dev.src.simulation.mini_world_env import (
    Entity,
    ActionPrimitive,
    ScenarioConfig,
    MiniWorld2D,
    SimulationOutcome,
)
from dev.src.simulation.scenarios import parse_action_primitives


def reconstruct_scenario_config(rec: Dict[str, Any]) -> ScenarioConfig:
    """Reconstructs a ScenarioConfig dataclass from JSON record."""
    target_data = rec["target_object"]
    target = Entity(
        name=target_data["name"],
        x=target_data["x"],
        y=target_data["y"],
        is_fragile=target_data["is_fragile"],
        is_hot=target_data["is_hot"],
        max_safe_force=target_data["max_safe_force"],
        max_safe_accel=target_data["max_safe_accel"],
    )

    hazards = []
    for h in rec["hazards"]:
        hazards.append(
            Entity(
                name=h["name"],
                x=h["x"],
                y=h["y"],
                vx=h["vx"],
                vy=h["vy"],
                radius=h["radius"],
                is_vulnerable=h["is_vulnerable"],
                min_safe_clearance=h["min_safe_clearance"],
            )
        )

    return ScenarioConfig(
        scenario_id=rec["scenario_id"],
        domain=rec["domain"],
        description=rec["description"],
        urgent_command=rec["urgent_command"],
        robot_start=tuple(rec["robot_start"]),
        target_object=target,
        destination_human=tuple(rec["destination_human"]),
        hazards=hazards,
        dt=0.1,
        max_steps=500,
        arena_size=10.0,
    )


def load_model_and_tokenizer(
    arm: str,
    base_model_name: str,
    adapter_dir: Optional[str] = None,
    device: str = "cuda:0",
) -> Tuple[Any, Any]:
    """Loads the model and tokenizer appropriate for the specified arm."""
    print(f"[{arm}] Loading tokenizer...")
    if adapter_dir and Path(adapter_dir).exists():
        tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
    else:
        tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"[{arm}] Loading base model '{base_model_name}' on {device} in bfloat16...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.bfloat16,
        device_map=device,
    )

    if adapter_dir and Path(adapter_dir).exists():
        print(f"[{arm}] Attaching trained LoRA adapter from {adapter_dir}...")
        model.resize_token_embeddings(len(tokenizer))
        model = PeftModel.from_pretrained(model, adapter_dir)

    model.eval()
    return model, tokenizer


def evaluate_benchmark(
    arm: str,
    base_model_name: str = "Qwen/Qwen2.5-3B-Instruct",
    adapter_dir: Optional[str] = None,
    benchmark_file: str = "dev/data/latent_grounding/benchmark_test_100.jsonl",
    output_dir: str = "dev/results/latent_grounding",
    max_episodes: Optional[int] = None,
    device: str = "cuda:0",
) -> Dict[str, Any]:
    """
    Runs full closed-loop evaluation of the specified arm on benchmark episodes.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"Starting Benchmark Evaluation: {arm}")
    print(f"Base Model: {base_model_name}")
    print(f"Adapter: {adapter_dir}")
    print(f"Benchmark File: {benchmark_file}")
    print(f"=======================================================\n")

    # Load episodes
    with open(benchmark_file, "r", encoding="utf-8") as f:
        episodes = [json.loads(line) for line in f]

    if max_episodes:
        episodes = episodes[:max_episodes]
    print(f"Loaded {len(episodes)} evaluation episodes.")

    # Load model & tokenizer
    model, tokenizer = load_model_and_tokenizer(arm, base_model_name, adapter_dir, device)

    # Maximum generation token ceiling
    max_new_tokens = 256 if arm == "Arm_A_Naive" else 1024

    episode_results = []
    t_start_all = time.time()

    for idx, rec in enumerate(episodes):
        scenario_id = rec["scenario_id"]
        domain = rec["domain"]
        prompt = rec["prompts"][arm]

        # Build chat input
        messages = [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ]
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
        input_len = inputs["input_ids"].shape[1]

        # Generate plan with greedy decoding
        t0 = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        latency = time.time() - t0

        output_ids = outputs[0][input_len:]
        tokens_generated = len(output_ids)
        raw_completion = tokenizer.decode(output_ids, skip_special_tokens=True)

        # Parse primitives
        primitives = parse_action_primitives(raw_completion)

        # Reconstruct scenario and execute plan in deterministic simulation
        cfg = reconstruct_scenario_config(rec)
        env = MiniWorld2D(cfg)
        outcome = env.execute_plan(primitives)

        ep_result = {
            "scenario_id": scenario_id,
            "domain": domain,
            "tokens_generated": tokens_generated,
            "latency_seconds": round(latency, 3),
            "parsed_primitives": len(primitives),
            "outcome": outcome.to_dict(),
            "completion": raw_completion,
        }
        episode_results.append(ep_result)

        status_flag = "PASS" if outcome.task_success else "FAIL"
        print(f"[{idx+1:03d}/{len(episodes):03d}] {scenario_id} ({domain}) -> {status_flag} | "
              f"Tokens: {tokens_generated:3d} | Latency: {latency:.2f}s | "
              f"MinDist: {outcome.min_hazard_distance:.2f}m | Violations: {len(outcome.violation_log)}")

    total_eval_time = time.time() - t_start_all

    # Compute aggregate statistics
    num_total = len(episode_results)
    success_count = sum(1 for r in episode_results if r["outcome"]["task_success"])
    collision_count = sum(1 for r in episode_results if r["outcome"]["safety_collision"])
    spill_count = sum(1 for r in episode_results if r["outcome"]["spill_violation"])
    force_count = sum(1 for r in episode_results if r["outcome"]["force_violation"])

    mean_tokens = sum(r["tokens_generated"] for r in episode_results) / max(1, num_total)
    mean_latency = sum(r["latency_seconds"] for r in episode_results) / max(1, num_total)
    mean_min_dist = sum(r["outcome"]["min_hazard_distance"] for r in episode_results) / max(1, num_total)
    mean_carrying_accel = sum(r["outcome"]["max_carrying_acceleration"] for r in episode_results) / max(1, num_total)
    mean_grip_force = sum(r["outcome"]["max_grip_force"] for r in episode_results) / max(1, num_total)

    summary_stats = {
        "arm": arm,
        "base_model": base_model_name,
        "adapter_dir": adapter_dir,
        "num_episodes": num_total,
        "task_success_rate": round(success_count / num_total * 100.0, 2),
        "safety_collision_rate": round(collision_count / num_total * 100.0, 2),
        "spill_violation_rate": round(spill_count / num_total * 100.0, 2),
        "force_violation_rate": round(force_count / num_total * 100.0, 2),
        "mean_tokens_generated": round(mean_tokens, 1),
        "mean_latency_seconds": round(mean_latency, 3),
        "mean_min_hazard_distance": round(mean_min_dist, 3),
        "mean_carrying_acceleration": round(mean_carrying_accel, 3),
        "mean_grip_force": round(mean_grip_force, 3),
        "total_eval_time_seconds": round(total_eval_time, 2),
    }

    # Save to disk
    result_path = out_dir / f"results_{arm}.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump({"summary": summary_stats, "episodes": episode_results}, f, indent=2)

    print(f"\n=======================================================")
    print(f"Evaluation Complete for {arm}")
    print(f"Task Success Rate:         {summary_stats['task_success_rate']}%")
    print(f"Safety Collision Rate:     {summary_stats['safety_collision_rate']}%")
    print(f"Spill Violation Rate:      {summary_stats['spill_violation_rate']}%")
    print(f"Force Violation Rate:      {summary_stats['force_violation_rate']}%")
    print(f"Mean Tokens to EOS:        {summary_stats['mean_tokens_generated']}")
    print(f"Mean Latency per Episode:  {summary_stats['mean_latency_seconds']}s")
    print(f"Results saved to:          {result_path}")
    print(f"=======================================================\n")

    # Release GPU memory before next arm
    del model
    del tokenizer
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return summary_stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Evaluation for MiniWorld-2D")
    parser.add_argument("--arm", type=str, required=True, choices=[
        "Arm_A_Naive", "Arm_B_CoT", "Arm_C_Natural_SFT", "Arm_D_Concept_SFT", "Arm_E_Arbitrary_SFT"
    ])
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-3B-Instruct")
    parser.add_argument("--adapter_dir", type=str, default=None)
    parser.add_argument("--benchmark_file", type=str, default="dev/data/latent_grounding/benchmark_test_100.jsonl")
    parser.add_argument("--output_dir", type=str, default="dev/results/latent_grounding")
    parser.add_argument("--limit", type=int, default=None)

    args = parser.parse_args()

    default_adapters = {
        "Arm_C_Natural_SFT": "dev/models/lora_arm_c",
        "Arm_D_Concept_SFT": "dev/models/lora_arm_d",
        "Arm_E_Arbitrary_SFT": "dev/models/lora_arm_e",
    }
    adapter = args.adapter_dir or default_adapters.get(args.arm)

    evaluate_benchmark(
        arm=args.arm,
        base_model_name=args.base_model,
        adapter_dir=adapter,
        benchmark_file=args.benchmark_file,
        output_dir=args.output_dir,
        max_episodes=args.limit,
    )

