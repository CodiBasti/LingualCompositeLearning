# Empirical Benchmark Evaluation: Latent Concept Grounding in MiniWorld-2D

**Date:** 2026-11-07 16:56:34  
**Base Model:** `Qwen/Qwen2.5-3B-Instruct`  
**Hardware:** NVIDIA GeForce RTX 5090 (32GB VRAM)  
**Evaluator:** Deterministic Kinematic Simulator (`MiniWorld-2D`) with Ground-Truth Numerical Physics  

---

## 1. Executive Summary & 5-Arm Comparative Results

| Metric | Arm A: Frozen Naive | Arm B: Frozen CoT (1024 tok) | Arm C: Natural SFT | Arm D: Concept SFT (`<|c:fufu_weli|>`) | Arm E: Arbitrary SFT (`<|mode_42|>`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Task Success Rate (%)** | 0.0% | 1.0% | 76.0% | 75.0% | 68.0% |
| **Safety Collision Rate (%)** | 95.0% | 55.0% | 19.0% | 19.0% | 19.0% |
| **Liquid Spill Rate (%)** | 4.0% | 8.0% | 6.0% | 4.0% | 19.0% |
| **Force Crushing Rate (%)** | 99.0% | 36.0% | 0.0% | 0.0% | 0.0% |
| **Mean Tokens to EOS** | 108.3 | 470.2 | 195.5 | 194.2 | 194.2 |
| **Mean Latency (s)** | 3.163s | 14.147s | 10.259s | 9.588s | 9.651s |
| **Mean Min Clearance (m)** | 1.21m | infm | 1.83m | 1.85m | 1.85m |
| **Mean Carrying Accel (m/s²)** | 0.66 | 0.37 | 0.68 | 0.68 | 0.69 |
| **Mean Grip Force (N)** | 54.20N | 1.25N | 1.77N | 1.77N | 1.77N |

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
