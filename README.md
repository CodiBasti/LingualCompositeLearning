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

## 🚀 The Active Frontier: Phase 5 (PEFT/LoRA Latent Anchoring)

Surface-level prompt engineering has been conclusively evaluated and its limits documented. The project is actively pivoting to the core scientific question:

> **"Are deeply anchored concept-composite tokens superior to verbose Chain-of-Thought in agent-to-robot coordination?"**

### Phase 5 Technical Architecture:
1. **Tokenizer Extension:** Register dedicated soft tokens (`<|c:fufu|>`, `<|c:weli|>`, `<|c:kuku|>`, `<|c:fufu_weli|>`) directly in the embedding matrix of `Qwen/Qwen2.5-14B-Instruct`.
2. **PEFT / LoRA Fine-Tuning:** Train attention projection layers on a local RTX 5090 using synthetic grounding pairs, encoding the physical invariants directly into the model's latent geometry—**with zero in-context prompt text**.
3. **Numerical Constraint Evaluator:** Discard regex keyword matching entirely; validate motor outputs against numerical bounds (Cartesian distance, contact force, velocity).
4. **Fair CoT Baseline:** Benchmark against an unconstrained Chain-of-Thought baseline with **1024 tokens**.

---

## 📁 Repository Structure

```
LingualCompositLearning/
├── README.md                           # Master Open-Science Post-Mortem & Roadmap
├── dev/
│   ├── concepts/                       # Formal Linguistic & Mathematical Specs
│   │   ├── SEMANTIC_DIMENSIONS.md      # The 5D Coordinate System
│   │   ├── MORPHOLOGY_AND_SYNTAX.md    # CVCV Morphology & Conflict Algebra
│   │   └── VOCABULARY_V1.md            # Canonical Operator Catalog
│   ├── data/benchmarks/
│   │   ├── benchmark_v2.json           # VHC-100 Dataset (100 Scenarios)
│   │   └── BENCHMARK_V2_SPEC.md        # Formal Dataset Specification
│   ├── findings/                       # Empirical Benchmark Reports
│   │   ├── FINDINGS-EXP-002.md         # EXP-002 Raw Metrics Analysis
│   │   └── FINDINGS-EXP-003.md         # EXP-003 Raw Metrics Analysis
│   ├── papers/neurips_2026/            # Research Manuscripts
│   │   ├── PAPER_MANUSCRIPT.md         # Master Empirical Dissection Manuscript
│   │   ├── main.tex                    # Compile-ready LaTeX Source
│   │   └── references.bib              # BibTeX Bibliography
│   ├── reports/                        # Audit Reports
│   │   └── review_audit_2026-11-05_*.md# The 8-Hour Adversarial Audit (Score 2/10)
│   └── src/lingual_research/           # Python Pipeline (Inference & Evaluation)
│       ├── build_benchmark_v2.py       # Benchmark Generator
│       ├── evaluator.py                # Regex Invariant Checker (Audited for Fragility)
│       ├── runner_exp002.py            # EXP-002 Benchmark Runner
│       ├── runner_exp003.py            # EXP-003 Composite Runner
│       └── audit_judge.py              # LLM-as-a-Judge Pipeline
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
