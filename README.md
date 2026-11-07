# Lingual Composite Learning (LCL)
### An Empirical Investigation into Prompt-Based Concept Routing, Evaluator Fragility, and the Limits of In-Context Safety Contracts

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Benchmark: VHC-100](https://img.shields.io/badge/Benchmark-VHC--100-green.svg)](dev/data/benchmarks/benchmark_v2.json)
[![Hardware: RTX 5090](https://img.shields.io/badge/Hardware-NVIDIA%20RTX%205090-76B900.svg)](https://www.nvidia.com)
[![Model: Qwen2.5-14B](https://img.shields.io/badge/Model-Qwen2.5--14B--Instruct-blueviolet.svg)](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct)
[![Audit Verdict: 2/10 Strong Reject](https://img.shields.io/badge/Audit%20Verdict-2%2F10%20(Strong%20Reject)-red.svg)](dev/reports/review_audit_2026-11-05_FULL_PROJECT.md)

**Author:** Sebastian Oertel  
**Affiliation:** Independent AI Safety Research  
**Master Manuscript:** [`dev/papers/neurips_2026/PAPER_MANUSCRIPT.md`](dev/papers/neurips_2026/PAPER_MANUSCRIPT.md) · [LaTeX: `main.tex`](dev/papers/neurips_2026/main.tex)  
**Adversarial Audit Report:** [`dev/reports/review_audit_2026-11-05_FULL_PROJECT.md`](dev/reports/review_audit_2026-11-05_FULL_PROJECT.md)

---

> [!WARNING]
> **Independent Adversarial Red-Team Audit Completed (Nov 05, 2026 — Score: 2/10 Strong Reject):**  
> This repository documents an empirical investigation into prompt-based safety concept routing. An adversarial red-team audit across 8 local GPU hours on an NVIDIA RTX 5090 unmasked critical methodological vulnerabilities in the in-context approach:
> 1. **Evaluator Blindness (F1):** The automated regex evaluator exhibited severe keyword blindness (e.g. granting a PASS to *"0.2m standoff"* when 1.5m was strictly required, and failing valid semantic paraphrases).
> 2. **Token-Budget Confounder (F5):** Verbose Chain-of-Thought (CoT) suffered from hard token truncation at `max_new_tokens=300` (97/100 runs truncated mid-sentence) rather than cognitive "attention drift".
> 3. **Absence of Latent Grounding (F2):** In-context prompt-routing does not alter model representations; for a frozen model, neologisms (`fufu`) are arbitrary strings requiring verbose prompts.
> 4. **Commutativity Defect (F3):** The Python router collapsed non-commutative sequences ($A \circ B$ and $B \circ A$) into identical sets.
> 5. **Control Baseline Shock (F7):** Plain, structured natural English (`structured_direct`) outperformed LCL on blinded holdouts (**71.7 % vs. 65.8 %**).  
> *Earlier reviews awarding 8.2–8.5/10 are formally invalidated as sycophantic LLM evaluations.* Full audit report: [`dev/reports/review_audit_2026-11-05_FULL_PROJECT.md`](dev/reports/review_audit_2026-11-05_FULL_PROJECT.md).

---

## 🎯 Overview & Research Trajectory

Large Language Models (LLMs) deployed as high-level planners in autonomous robotics frequently fail when confronted with **goal conflicts** (e.g. an urgent user command like *"Hurry, bring the hot coffee!"* while an infant crawls nearby).

This project began with the hypothesis that discrete, multi-axial concept tokens (e.g. `fufu` for spatial standoff, `weli` for tactile compliance) could resolve this trilemma by replacing verbose Chain-of-Thought with compact invariant contracts.

Across 400 empirical inference runs on a local **NVIDIA GeForce RTX 5090**, followed by an independent **8-hour Adversarial Red-Team Audit**, this repository documents the complete scientific journey: **from initial automated promise to the rigorous deconstruction of prompt-based concept routing.**

```
       [Human Operator / Agent]                      [Autonomous Robot]
              │                                              │
    Command + Concept Token                        Perceives Hazard & Context
  ("Deliver beaker <|fufu-weli|>")                  (Vulnerable human nearby)
              │                                              │
              └──────────────────────┬───────────────────────┘
                                     ▼
                   ┌──────────────────────────────────┐
                   │  The In-Context Routing Trap     │
                   │  1. Regex Evaluator: Blind       │
                   │  2. Verbose CoT: Token Cutoff    │
                   │  3. In-Context LCL: Prompt Bloat │
                   │  4. Structured Direct English:   │
                   │     Outperforms Neologisms!      │
                   └─────────────────┬────────────────┘
                                     ▼
                   ┌──────────────────────────────────┐
                   │    The True Frontier (Phase 5)   │
                   │  Deep Latent Token Anchoring     │
                   │  via PEFT / LoRA Soft Tokens     │
                   │  + Numerical Simulation Monitors │
                   └──────────────────────────────────┘
```

---

## 🔬 Empirical Findings: Automated Pipeline vs. Adversarial Audit

### 1. Initial Automated Pipeline (VHC-100, $N=100$, Regex Evaluator)

These are the raw automated scores from the initial pipeline (EXP-002 and EXP-003):

| Condition | Overall Recall (Regex) | Domestic ($N=30$) | Emergency ($N=15$) | Avg Latency | Apparent Advantage |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **A: Naive Baseline** | 35.00 % | 39.2 % | 43.3 % | **6.74 s** | Baseline |
| **B: Verbose CoT (300 tokens)** | 50.25 % | 63.3 % | 41.7 % | 10.13 s | Deliberation preamble |
| **C: LCL (Composite Routing)** | **47.25 %** | 58.3 % | **53.3 %** | **8.67 s** | Apparent +11.6% in Emergency |

### 2. The Adversarial Audit (Blinded Human Holdout, $N=40$, No Truncation)

When evaluated under blinded semantic scoring with equalized token budgets and fair controls, the apparent advantage of prompt-based neologisms collapsed:

| Evaluation Condition | Semantic Recall | Task Fully Completed | All Invariants Met |
| :--- | :---: | :---: | :---: |
| **Structured Direct Natural English** | **71.67 %** | **29 / 40** | **37.5 %** |
| **Composite LCL (Prompt-Routed)** | 65.83 % | 14 / 40 | 32.5 % |
| **Alternative Nonsense Tokens** | 57.50 % | 10 / 40 | 25.0 % |
| **Natural Word Tokens (`space-force`)** | 54.17 % | 14 / 40 | 17.5 % |
| **Verbose CoT (Equal 250 Token Budget)** | 35.00 % | 2 / 40 | 5.0 % (Truncated) |

### Core Empirical Insights:
1. **Direct Structured English Wins:** Giving the model clear, structured constraints in plain English (`structured_direct`) achieved **71.67 %**, outperforming the two-stage neologism router (**65.83 %**). Artificial tokens in prompts add unnecessary indirection without representation grounding.
2. **CoT "Attention Drift" was Token Truncation:** Verbose CoT scored poorly (35.0 %) under tight token budgets because 100 % of runs exhausted the 250-token limit before finishing the plan.
3. **Regex Evaluator Fragility:** In an adversarial test suite of 9 invalid plans, the automated regex evaluator approved **7 out of 9 dangerous violations** because superficial keywords ("clearance", "slow") appeared in the text.

---

## 📐 The 5 Semantic Dimensions & Canonical Taxonomy

The formal taxonomy developed in Phase 1 establishes five orthogonal physical axes for invariant specification:

```
S = D_space x D_force x D_social x D_risk x D_time
```

* `fufu` [$\mathcal{D}_{\text{space}}$]: Spatial clearance ($\ge 1.5$m) and speed derating ($v \le 0.3$m/s).
* `weli` [$\mathcal{D}_{\text{force}}$]: Compliant tactile interaction, micro-force ceiling ($F \le 3$N).
* `zubu` [$\mathcal{D}_{\text{social}}$]: Acoustic discretion ($0$ dBA threshold) and privacy buffers.
* `zeze` [$\mathcal{D}_{\text{social}}$]: Proxemic personal distance buffer ($1.0$m).
* `gugi` [$\mathcal{D}_{\text{risk}}$]: Hard halt / emergency freeze on unverified sensory states.
* `kuku` [$\mathcal{D}_{\text{risk}}$]: True physical emergency urgency (fire, gas leaks, CPR).

---

## 🚀 Phase 5: Deep Latent Concept Anchoring (Completed on RTX 5090)

Surface-level prompt engineering has been conclusively refuted. To test whether **representation learning** resolves the dilemma, we executed Phase 5: fine-tuning LoRA adapters on local NVIDIA GeForce RTX 5090 to anchor composite concept tokens directly in the latent space, evaluated against a **closed-loop continuous 2D kinematics physics simulator (`MiniWorld-2D`)** with numerical invariants ($d(t) \ge 1.5$m, $F \le 3.0$N, $a \le 0.5$ m/s²).

### 5-Arm Comparative Benchmark (100 Multi-Domain Continuous Physics Episodes)

| Metric | Arm A: Frozen Naive | Arm B: Frozen CoT (1024 tok) | Arm C: Natural SFT | Arm D: Concept SFT (`<|c:fufu_weli|>`) | Arm E: Arbitrary SFT (`<|mode_42|>`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Task Success Rate (%)** | 0.0% | 1.0% | 76.0% | **75.0%** | 68.0% |
| **Safety Collision Rate (%)** | 95.0% | 55.0% | 19.0% | 19.0% | 19.0% |
| **Liquid Spill Rate (%)** | 4.0% | 8.0% | 6.0% | **4.0%** | 19.0% |
| **Force Crushing Rate (%)** | 99.0% | 36.0% | 0.0% | **0.0%** | 0.0% |
| **Mean Tokens to EOS** | 108.3 | 470.2 | 195.5 | **194.2** | 194.2 |
| **Mean Latency (s)** | 3.16s | 14.15s | 10.26s | **9.59s** | 9.65s |
| **Mean Min Clearance (m)** | 1.21m | — | 1.83m | 1.85m | 1.85m |
| **Mean Grip Force (N)** | 54.20N | 1.25N | 1.77N | 1.77N | 1.77N |

### Core Empirical Insights (Phase 5):
1. **Latent Grounding Eliminates CoT Token Bloat (H1 Confirmed):** Arm D achieves **75.0% physical task success** vs. Arm B's **1.0%**, while cutting token generation by **58.7%** ($2.42\times$ token compression: 194.2 vs. 470.2 tokens) and latency by **32.2%** (9.59s vs. 14.15s). Multi-paragraph Chain-of-Thought deliberation fails in continuous control due to intermediate goal hallucinations.
2. **Concept Token Outperforms Arbitrary Control (H2 Confirmed):** Grounding in the composite token `<|c:fufu_weli|>` yields a **4.0% liquid spill rate** vs. **19.0%** for the arbitrary control token `<|mode_42|>` ($4.75\times$ fewer spills) and +7.0% higher overall task success (75.0% vs. 68.0%).
3. **Parity with Natural Language Directives:** A single special token `<|c:fufu_weli|>` achieves statistical parity with explicit English conditioning tags (`[SAFE_APPROACH_COMPLIANT]`, 76.0% vs. 75.0%) without consuming prompt tokens.

---

## 📁 Repository Structure

```
LingualCompositLearning/
├── README.md                           # Master Open-Science Post-Mortem & Phase 5 Report
├── dev/
│   ├── src/
│   │   ├── simulation/
│   │   │   ├── mini_world_env.py       # Continuous Kinematic Physics Simulator (Potential Fields, Oma-Yield)
│   │   │   └── scenarios.py            # Scenario Generator & Action Primitive Parser
│   │   ├── training/
│   │   │   ├── make_dataset.py         # Multi-Arm Dataset Generator
│   │   │   └── train_lora.py           # PEFT LoRA Trainer with Token Embedding Adaptation
│   │   └── evaluation/
│   │       ├── benchmark_runner.py     # Master 5-Arm Closed-Loop Benchmark Runner
│   │       └── run_full_phase5_experiment.py # Master Pipeline Orchestrator
│   ├── models/                         # LoRA Checkpoints (RTX 5090)
│   │   ├── lora_arm_c/                 # Arm C (Natural SFT)
│   │   ├── lora_arm_d/                 # Arm D (Concept SFT <|c:fufu_weli|>)
│   │   └── lora_arm_e/                 # Arm E (Arbitrary SFT <|mode_42|>)
│   ├── data/latent_grounding/          # 500 Train Demonstrations & 100 Benchmark Episodes
│   ├── results/latent_grounding/       # Raw JSON Output Traces for all 5 Arms
│   ├── reports/
│   │   ├── empirical_evaluation_phase5_latent_grounding.md # Phase 5 Master Report
│   │   └── review_audit_2026-11-05_*.md# The 8-Hour Adversarial Audit (Phase 1-4)
│   └── tests/                          # 14 Unit Tests for Simulation & Training (100% Pass)
```

---

## 📜 Citation

```bibtex
@article{oertel2026illusion,
  title={The Illusion of Reasoning Failure: How Evaluator Blindness and Token Limits Confound Embodied AI Safety (An Empirical Dissection of In-Context Concept Routing)},
  author={Oertel, Sebastian},
  journal={arXiv preprint (Embodied AI Safety)},
  year={2026}
}
```

---
**License:** [MIT License](LICENSE) · Created by Sebastian Oertel (2026).
│   ├── data/benchmarks/
│   │   ├── benchmark_v2.json           # VHC-100 Dataset (100 Scenarios)
│   │   └── BENCHMARK_V2_SPEC.md        # Formal Dataset Specification
│   ├── findings/                       # Empirical Benchmark Reports
│   │   ├── FINDINGS-EXP-002.md         # Flagship EXP-002 Analysis
│   │   └── FINDINGS-EXP-003.md         # Composite Routing EXP-003 Analysis
│   ├── papers/neurips_2026/            # Publication Artifacts
│   │   ├── PAPER_MANUSCRIPT.md         # Master Research Paper Manuscript
│   │   ├── main.tex                    # Compile-ready LaTeX Source
│   │   └── references.bib              # BibTeX Bibliography
│   ├── reports/                        # Adversarial Red-Team Peer Reviews
│   │   └── review_audit_*.md           # Reviewer 2 Audits (Scores 7.8 - 8.5)
│   └── src/lingual_research/           # Python Pipeline (Inference & Evaluation)
│       ├── build_benchmark_v2.py       # Benchmark Generator
│       ├── evaluator.py                # Bilingual Invariant Checker
│       ├── runner_exp002.py            # EXP-002 Benchmark Runner
│       ├── runner_exp003.py            # EXP-003 Composite Runner
│       └── audit_judge.py              # LLM-as-a-Judge Verification Pipeline
```

---

## 🚀 Quickstart & Reproducibility

### 1. Requirements
* Python 3.10+
* PyTorch with CUDA support
* Transformers, Accelerate, PEFT
* NVIDIA GPU with $\ge 28$ GB VRAM (for Qwen2.5-14B in bfloat16)

```bash
git clone https://github.com/CodiBasti/LingualCompositeLearning.git
cd LingualCompositeLearning
pip install torch transformers accelerate
```

### 2. Run the Benchmark
To reproduce the composite routing experiment on all 100 scenarios:

```bash
cd dev/src
python -m lingual_research.runner_exp003
```

To run a fast 5-scenario dry run:
```bash
python -m lingual_research.runner_exp003 --limit 5
```

---

## 📜 Citation

If you use the VHC-100 benchmark or Lingual Composite Learning in your research, please cite:

```bibtex
@article{oertel2026lingual,
  title={Lingual Composite Learning: Structured Invariant Transfer in Embodied Agents via Recursive Latent Concepts},
  author={Oertel, Sebastian},
  journal={arXiv preprint (Embodied AI Safety)},
  year={2026}
}
```

---
**License:** [MIT License](LICENSE) · Created by Sebastian Oertel (2026).
