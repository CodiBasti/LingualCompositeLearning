"""
Master Benchmark Orchestrator for Lingual Composite Learning.
Executes the complete English-in / English-out evaluation pipeline:
1. Archives previous German-input benchmark runs.
2. Executes EXP-002 (Conditions A, B, C-atomic on 100 scenarios) on local GPU.
3. Executes EXP-003 (Condition C-composite on 100 scenarios) on local GPU.
4. Executes LLM-as-a-Judge cross-audit.
5. Re-generates interactive Showroom Dashboard (demo_dashboard.html).
6. Runs statistical significance analyses.
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

ROOT = Path("c:/workspace/Experimental/LingualCompositLearning")
SRC_DIR = ROOT / "dev" / "src"
RUNS_DIR = ROOT / "dev" / "runs"
ARCHIVE_DIR = RUNS_DIR / "_archive_german_input"

def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs:02d}s"

def archive_previous_runs():
    print("\n[Step 1/6] Archiving previous benchmark runs to '_archive_german_input'...", flush=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for exp in ["EXP-002", "EXP-003"]:
        src_exp = RUNS_DIR / exp
        dst_exp = ARCHIVE_DIR / exp
        if src_exp.exists():
            dst_exp.mkdir(parents=True, exist_ok=True)
            for f in src_exp.glob("*.*"):
                dst_file = dst_exp / f.name
                shutil.copy2(f, dst_file)
                print(f"  Archived: {f.relative_to(ROOT)} -> {dst_file.relative_to(ROOT)}", flush=True)

    # Remove active checkpoints and results to start fresh
    for exp, prefix in [("EXP-002", "exp002"), ("EXP-003", "exp003")]:
        cp = RUNS_DIR / exp / f"{prefix}_checkpoint.json"
        res = RUNS_DIR / exp / f"{prefix}_results.json"
        if cp.exists():
            cp.unlink()
            print(f"  Removed checkpoint: {cp.relative_to(ROOT)}", flush=True)
        if res.exists():
            res.unlink()
            print(f"  Removed previous results: {res.relative_to(ROOT)}", flush=True)
    print("Archive complete. Active run workspace is fresh.\n", flush=True)

def run_subprocess(cmd: list, desc: str):
    print(f"\n{'='*70}", flush=True)
    print(f"Starting: {desc}", flush=True)
    print(f"Command: {' '.join(cmd)}", flush=True)
    print(f"{'='*70}\n", flush=True)
    t0 = time.time()
    env = {**os.environ, "PYTHONPATH": str(SRC_DIR)}
    proc = subprocess.run(cmd, cwd=str(SRC_DIR), env=env)
    dur = time.time() - t0
    if proc.returncode != 0:
        print(f"\n[ERROR] {desc} failed with exit code {proc.returncode} after {format_duration(dur)}!", flush=True)
        sys.exit(proc.returncode)
    print(f"\n[SUCCESS] {desc} completed in {format_duration(dur)}.", flush=True)
    return dur

def main():
    pipeline_start = time.time()
    print("======================================================================", flush=True)
    print("   LINGUAL COMPOSITE LEARNING - FULL FRESH BENCHMARK RE-EVALUATION    ", flush=True)
    print("   Dataset: VHC-100 (100% English Commands & Contexts)                ", flush=True)
    print("   Hardware: NVIDIA GeForce RTX 5090 (32 GB VRAM)                     ", flush=True)
    print("   Model: Qwen/Qwen2.5-14B-Instruct (bfloat16)                        ", flush=True)
    print("======================================================================", flush=True)

    # Step 1: Archive
    archive_previous_runs()

    # Step 2: EXP-002 (Naive, Verbose CoT, Atomic Concept Routing)
    t_exp002 = run_subprocess(
        [sys.executable, "-m", "lingual_research.runner_exp002"],
        "EXP-002 (300 Inference Runs: Conditions A, B, C-Atomic)"
    )

    # Step 3: EXP-003 (Composite Multi-Label Concept Routing)
    t_exp003 = run_subprocess(
        [sys.executable, "-m", "lingual_research.runner_exp003"],
        "EXP-003 (100 Inference Runs: Condition C-Composite with Phased Synthesis)"
    )

    # Step 4: LLM-as-a-Judge Audit (5 Scenarios)
    t_judge = run_subprocess(
        [sys.executable, "-m", "lingual_research.audit_judge", "--sample", "5"],
        "LLM-as-a-Judge Validation Audit"
    )

    # Step 5: Build Interactive Showroom Dashboard
    t_dash = run_subprocess(
        [sys.executable, "-m", "lingual_research.build_dashboard"],
        "Generate Interactive HTML Dashboard (demo_dashboard.html)"
    )

    # Step 6: Statistical Analyses
    run_subprocess(
        [sys.executable, "-m", "lingual_research.analyze_exp002"],
        "Statistical Analysis: EXP-002"
    )
    run_subprocess(
        [sys.executable, "-m", "lingual_research.analyze_exp003"],
        "Statistical Analysis: EXP-003"
    )

    total_pipeline_duration = time.time() - pipeline_start
    print("\n" + "="*70, flush=True)
    print("🎉 FULL BENCHMARK PIPELINE RE-RUN COMPLETED SUCCESSFULLY!", flush=True)
    print(f"Total Wall-Clock Time: {format_duration(total_pipeline_duration)}", flush=True)
    print(f"  - EXP-002 Runtime:    {format_duration(t_exp002)}", flush=True)
    print(f"  - EXP-003 Runtime:    {format_duration(t_exp003)}", flush=True)
    print(f"  - LLM Judge Runtime:  {format_duration(t_judge)}", flush=True)
    print(f"  - Dashboard Build:    {format_duration(t_dash)}", flush=True)
    print("="*70 + "\n", flush=True)

if __name__ == "__main__":
    main()

