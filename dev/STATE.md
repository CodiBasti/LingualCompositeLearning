# Project State: Lingual Composite Learning

> **Last Updated:** November 06, 2026  
> **Status:** Phase 1–4 Concluded with an Adversarial Red-Team Audit (Score: 2/10 — Strong Reject). In-context prompt-routing retracted from conference submission and transitioned to an **Open-Science Negative Results Post-Mortem** (Option A). Research frontier pivoted to **Phase 5: Deep Latent Concept Anchoring via PEFT/LoRA** for Agent/Robot Coordination.  
> **Dataset:** [`dev/data/benchmarks/benchmark_v2.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v2.json)  
> **Audit Report:** [`dev/reports/review_audit_2026-11-05_FULL_PROJECT.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/reports/review_audit_2026-11-05_FULL_PROJECT.md) (8 GPU hours, blinded controls, ablation studies)  
> **Active Focus:** Transparent Open-Source Re-framing (Option A) & Phase 5 PEFT/LoRA Latent Concept Engineering.

---

## 📍 Milestone Status

- [x] **Theoretical Foundation:** Formalized in [`dev/concepts/SEMANTIC_DIMENSIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/SEMANTIC_DIMENSIONS.md) and [`dev/concepts/MORPHOLOGY_AND_SYNTAX.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/MORPHOLOGY_AND_SYNTAX.md).
- [x] **Benchmark Suite v2.0 (VHC-100):** 100 standardized scenarios generated across Domestic (30), Clinical Care (30), Precision Lab (25), and Emergency (15).
- [x] **Phase 4 In-Context GPU Experiments (RTX 5090):**
  - EXP-001 (Pilot, 30 runs), EXP-002 (Flagship, 300 runs), EXP-003 (Composite, 100 runs).
  - Initial headline metrics: Naive 35.0%, Verbose CoT 50.25%, Atomic 46.25%, Composite 47.25%.
- [x] **Adversarial Red-Team Audit (Nov 05, 2026 — 8 GPU Hours):**
  - Independent verification executed with blinded ratings, holdout sets, and control conditions.
  - **Audit Verdict: 2/10 (Strong Reject) — Publication Readiness Retracted.**
  - **F1 (Evaluator Blindness):** Regex evaluator approved severe safety violations (e.g. 0.2m passed a 1.5m clearance rule; speed increases next to children passed due to keyword presence).
  - **F2 (Missing Latent Grounding):** In-context routing is pure prompt engineering, not latent representation learning.
  - **F3 (Grammar & Commutativity Defect):** Synthesizer mapped `fufu-weli` and `weli-fufu` to identical sets.
  - **F5 (Token-Budget Confound):** 97/100 CoT runs hit the 300-token limit mid-sentence; "attention drift" was largely token truncation.
  - **Control Finding:** Plain structured natural English (`structured_direct`) outperformed LCL on holdouts (71.7% vs. 65.8%), proving surface-level neologisms add no zero-shot benefit over clear English.
  - **F8 (Sycophancy Reversal):** Prior reviews (8.2/10 and 8.5/10) invalidated as sycophantic LLM praise.
- [x] **Full English Internationalization:** 100% of benchmark scenarios, concept definitions, findings, manuscripts, and dashboard traces translated into standard academic English.
- [ ] **Option A: Transparent Open-Source Re-framing (In Progress):**
  - Convert `README.md` and paper into an honest post-mortem of prompt-based routing and evaluator fragility.
- [ ] **Phase 5: Deep Latent Concept Anchoring via PEFT/LoRA (Active Frontier):**
  - Test the true core question: *Can deeply anchored composite concept tokens (trained into model weights) enforce physical invariants more robustly and efficiently than verbose Chain-of-Thought in robot/agent execution?*

---

## 🎯 Next Steps

1. **Execute Option A Plan:**
   - Update `README.md` with the full Red-Team Audit results, post-mortem narrative, and evaluator limitations.
   - Update `dev/papers/neurips_2026/PAPER_MANUSCRIPT.md` to reflect the post-mortem scope and retract ungrounded claims.
2. **Phase 5 Technical Architecture:**
   - Extend Qwen2.5-14B tokenizer with dedicated concept tokens (`<|c:fufu|>`, `<|c:weli|>`, `<|c:kuku|>`).
   - Construct synthetic invariant-grounded fine-tuning dataset.
   - Implement LoRA fine-tuning on local RTX 5090.
   - Build a rigorous numerical constraint evaluator (no regex keyword matching!).
   - Benchmark against an unconstrained, fair Chain-of-Thought baseline (1024 tokens).
