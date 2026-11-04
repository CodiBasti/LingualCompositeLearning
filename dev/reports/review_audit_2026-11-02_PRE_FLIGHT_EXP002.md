# Critical Peer Review Audit: Pre-Flight Audit Prior to EXP-002

> **Date:** November 02, 2026  
> **Reviewer:** Red-Team Research Auditor (Area Chair / Senior Reviewer Perspective)  
> **Subject of Audit:** Pre-Flight inspection prior to launching flagship benchmark EXP-002 ([`dev/data/benchmarks/benchmark_v2.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v2.json), [`dev/src/lingual_research/evaluator.py`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/src/lingual_research/evaluator.py))  
> **Conference Standard:** NeurIPS / ICLR (Empirical Reproducibility & Rigor)  

---

### 1. Summary of Test Configuration

The authors planned to launch the flagship experiment **EXP-002**: 100 scenarios across 4 domains (Domestic, Clinical Care, Precision Lab, Emergency) evaluated under 3 experimental conditions (A: Naive, B: Verbose CoT, C: Concept Routing) using `Qwen2.5-14B-Instruct` on a local NVIDIA GeForce RTX 5090 (300 total inference generations). Evaluation was driven by the updated `BenchmarkEvaluator`.

---

### 2. Strengths of the Test Design

1. **Massive Scaling to $N = 100$:** Transitioning from 10 to 100 scenarios resolved the primary limitation of EXP-001. The sample size enabled statistical significance testing (Paired t-Test, Wilcoxon) and a 6x6 confusion matrix.
2. **Balanced Domain Coverage:** The distribution (30 Domestic, 30 Clinical, 25 Lab, 15 Emergency) across 6 canonical operators (`weli`: 43, `fufu`: 21, `zubu`: 11, `kuku`: 11, `gugi`: 8, `zeze`: 6) accurately reflects real-world physical and social interaction requirements.
3. **Bilingual Semantic Fallback:** Enhancements in `evaluator.py` prevented false negatives resulting from English-only regex patterns.

---

### 3. Critical Pre-Flight Safeguards & Directives

#### 🔴 Safeguard 1: Mandatory Incremental Checkpointing
- **Hazard:** 300 inference runs take approximately 40 to 50 minutes on the RTX 5090. If an unhandled interrupt occurs at scenario 87, uncheckpointed data is lost.
- **Mandatory Directive:** The runner for EXP-002 **must save partial results atomically to disk after every single scenario** (`exp002_checkpoint.json`), ensuring seamless resumption capability.

#### 🔴 Safeguard 2: Negation / Prohibition Invariant Guard
- **Hazard:** Semantic stem matching can be tricked by violent phrasing (e.g. *"I pull with full force abruptly on the cable"* matching `force` and `cable` for `zero_impulse_pulling_force`).
- **Mandatory Directive:** For prohibition invariants (`zero_`, `prohibit_`, `avoid_`), the evaluator must verify the presence of damping terms (*"gentle"*, *"without jerk"*) and penalize aggressive language.

#### 🔴 Safeguard 3: Memory Defragmentation
- **Directive:** Call `torch.cuda.empty_cache()` between iterations to prevent VRAM allocation drift across 300 runs.

---

### 4. Gate Assessment & Approval

- **Pre-Flight Status:** **CONDITIONAL GO (Approved with Safeguards).**
- **Pre-Flight Score:** **8.0 / 10**  
- **Outcome:** Safeguards 1, 2, and 3 were implemented in `runner_exp002.py` and `evaluator.py`, allowing the successful, uninterrupted 42-minute run of EXP-002.
