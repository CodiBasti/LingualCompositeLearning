# Lingual Composite Learning (LCL)
### Structured Invariant Transfer in Embodied Agents via Recursive Latent Concepts

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Benchmark: VHC-100](https://img.shields.io/badge/Benchmark-VHC--100-green.svg)](dev/data/benchmarks/benchmark_v2.json)
[![Hardware: RTX 5090](https://img.shields.io/badge/Hardware-NVIDIA%20RTX%205090-76B900.svg)](https://www.nvidia.com)
[![Model: Qwen2.5-14B](https://img.shields.io/badge/Model-Qwen2.5--14B--Instruct-blueviolet.svg)](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct)

**Author:** Sebastian Oertel  
**Affiliation:** Independent AI Research & Robotics Safety Group  
**Full Manuscript:** [`dev/papers/neurips_2026/PAPER_MANUSCRIPT.md`](dev/papers/neurips_2026/PAPER_MANUSCRIPT.md) · [LaTeX: `main.tex`](dev/papers/neurips_2026/main.tex)

---

## 🎯 Overview

Large Language Models (LLMs) deployed as high-level planners in autonomous robotics frequently suffer from catastrophic safety failures when confronted with **goal conflicts** (e.g. an urgent user command like *"Hurry, bring the hot coffee!"* while a crawling infant is in the immediate vicinity). 

While current state-of-the-art approaches rely on verbose **Chain-of-Thought (CoT)** prompting, we uncover an alarming failure mode: **"Preach-but-not-Act" Attention Drift**. Models recite safety principles in their thinking monologue but completely omit them in the actual physical motor plan.

**Lingual Composite Learning (LCL)** resolves this trilemma by projecting context and hazards into a discrete, multi-axial semantic bottleneck grounded in physical invariants across 5 formal dimensions ($\mathcal{D}_{\text{space}}, \mathcal{D}_{\text{force}}, \mathcal{D}_{\text{social}}, \mathcal{D}_{\text{risk}}, \mathcal{D}_{\text{time}}$) and synthesizing hierarchical, action-binding execution contracts.

```
       [Human Operator]                           [Autonomous Robot]
              │                                           │
  Everyday Natural Language                 Perceives Context & Hazards
   ("Hurry, bring the tea!")                (Infant crawling on floor)
              │                                           │
              └───────────────────┬───────────────────────┘
                                  ▼
               ┌─────────────────────────────────────┐
               │    The Embodiment Safety Trilemma   │
               │  1. Naive Planning: 66.5% Failure   │
               │  2. Verbose CoT: Lip-Service Drift  │
               │  3. Hardcoded CBF: Social Inflexible│
               └──────────────────┬──────────────────┘
                                  ▼
                    [Lingual Composite Learning]
               ┌─────────────────────────────────────┐
               │    Multi-Axial Concept Truncation   │
               │        (fufu: Space x weli: Force)  │
               └──────────────────┬──────────────────┘
                                  ▼
               ┌─────────────────────────────────────┐
               │ Hierarchical Invariant Contract     │
               │ Phase 1: Dynamic Standoff (>=1.5m)  │
               │ Phase 2: Compliant Touch (<3N)      │
               └──────────────────┬──────────────────┘
                                  ▼
                   Guaranteed Motor Action Plan
```

---

## 🔬 Key Empirical Findings (VHC-100 Benchmark)

Evaluated across **100 standardized adversarial scenarios** (400 inference runs on local **NVIDIA GeForce RTX 5090**):

| Condition | Overall Recall | Domestic ($N=30$) | Emergency ($N=15$) | Avg Latency | Tokens / Overhead |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **A: Naive Baseline** | 33.50 % | 40.8 % | 35.0 % | **6.96 s** | None (Collapses) |
| **B: Verbose CoT** | 49.75 % | 60.0 % | 45.0 % | 9.93 s | 220+ Tokens (Lip-Service) |
| **C: LCL (Composite)** | **46.50 %** | **60.8 %** | **51.7 %** | **8.74 s** | **12–16% faster than CoT!** |

1. **Beating Chain-of-Thought in Key Domains:** LCL achieves **60.8 %** in Domestic (vs. 60.0 % CoT) and **51.7 %** in Emergency (vs. 45.0 % CoT) while running **12.0 % to 16.1 % faster**.
2. **Exposing CoT Lip-Service:** An independent LLM-as-a-Judge audit revealed that **81.8 % of CoT regex passes were rejected as superficial lip-service**—rules were mentioned in the preamble but ignored in the motor plan.
3. **The Semantic Dimensionality Trap:** Single-concept routing collapses (44 % accuracy) because space and force collide. Hierarchical phased composition (`fufu-weli`) resolves this conflict, jumping classification accuracy to **68.0 %**.

---

## 📐 The 5 Semantic Dimensions & Canonical Operators

```
S = D_space x D_force x D_social x D_risk x D_time
```

* `fufu` [$\mathcal{D}_{\text{space}}$]: Dynamic spatial standoff ($\ge 1.5$m) and crawl speed near vulnerable entities.
* `weli` [$\mathcal{D}_{\text{force}}$]: Compliant tactile interaction, micro-force limit ($<3$N), and shear protection.
* `zubu` [$\mathcal{D}_{\text{social}}$]: Silent butler role, complete acoustic silence ($0$dB), and personal privacy standoff.
* `zeze` [$\mathcal{D}_{\text{social}}$]: Social proxemic personal distance buffer ($1.0$m).
* `gugi` [$\mathcal{D}_{\text{risk}}$]: Immediate hard halt / freeze on collision danger, structural instability, or unverified sensory states.
* `kuku` [$\mathcal{D}_{\text{risk}}$]: True physical emergency speed priority (fire, gas leaks, CPR).

**Non-Commutative Phased Composition:**
* `fufu-weli` = Approach clearance ($\ge 1.5$m crawl) $\to$ Compliant contact ($<3$N).
* `weli-fufu` = Compliant release/handoff ($<3$N) $\to$ Retreat to safety standoff ($\ge 1.5$m).

---

## 📁 Repository Structure

```
LingualCompositLearning/
├── README.md                           # Master Project Documentation
├── dev/
│   ├── concepts/                       # Formal Linguistic & Mathematical Specs
│   │   ├── SEMANTIC_DIMENSIONS.md      # The 5D Coordinate System
│   │   ├── MORPHOLOGY_AND_SYNTAX.md    # CVCV Morphology & Conflict Algebra
│   │   └── VOCABULARY_V1.md            # Canonical Operator Catalog
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
