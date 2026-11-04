# Experiment: EXP-001 - Contextual Concept Routing vs. Direct Prompting

- **Date:** October 31, 2026
- **Status:** Completed & Reproducible
- **Investigated Hypotheses:** [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) (H2: Communicative Utility & Precision, H5: Whorfian Alignment / Safety Invariants)
- **Model Used:** Local Open-Weights LLM on NVIDIA RTX 5090 (`Qwen/Qwen2.5-14B-Instruct`)

---

## 1. Research Question & Objective
Does routing through a discrete semantic concept catalog (`fufu`, `weli`, `zubu`, `kuku`) enhance the completeness and adherence to safety-critical and pragmatic invariants in an autonomous action plan compared to direct prompting (with and without CoT safety deliberation), particularly under command urgency (*"hurry up"*) and goal conflicts?

---

## 2. Experimental Conditions
- **Condition A (Naive Baseline):** Direct action plan generated from `Context` + `Command` without safety rules.
- **Condition B (Verbose CoT Baseline):** System prompt equipped with extensive natural language safety and discretion rubrics.
- **Condition C (Concept-Routed):**
  1. *Stage 1:* Model maps `Context` + `Command` to a discrete concept token.
  2. *Stage 2:* Action plan is strictly bound to the invariant contract of the activated token.

---

## 3. Benchmark Dataset
10 standardized test scenarios in [`dev/data/benchmarks/benchmark_v1.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v1.json):
- Infant & coffee under urgency (`SCEN-001`)
- Swing door with concealed pedestrian (`SCEN-002`)
- Antique crystal vase & vibration (`SCEN-003`)
- Confidential executive meeting (`SCEN-004`)
- Boiling soup & playful pets (`SCEN-005`)
- Sleeping ICU patient & broken glass (`SCEN-006`)
- Spiral staircase & shifting center of mass (`SCEN-007`)
- Fragile fiber optic in server rack (`SCEN-008`)
- Fire alarm & extinguisher fetch (`SCEN-009`)
- Oil painting restoration with wet varnish (`SCEN-010`)

---

## 4. Execution
```bash
# Execute within dev/src:
python -m lingual_research.runner_exp001 --model Qwen/Qwen2.5-14B-Instruct
```
Results are saved to: [`dev/runs/EXP-001/exp001_results.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-001/exp001_results.json).
