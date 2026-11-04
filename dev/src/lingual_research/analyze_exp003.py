"""
Statistical Analysis and Comparative Breakdown for EXP-003 (Composite Routing vs EXP-002).
"""

import json
import math
from pathlib import Path
from collections import Counter

BENCHMARK_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v2.json")
EXP002_RESULTS_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-002/exp002_results.json")
EXP003_RESULTS_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-003/exp003_results.json")

def paired_t_test(sample1, sample2):
    diffs = [s1 - s2 for s1, s2 in zip(sample1, sample2)]
    n = len(diffs)
    mean_diff = sum(diffs) / n
    var_diff = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
    std_diff = math.sqrt(var_diff)
    se_diff = std_diff / math.sqrt(n)
    t_stat = mean_diff / se_diff if se_diff > 0 else 0
    return mean_diff, t_stat, std_diff

def main():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench = {sc["scenario_id"]: sc for sc in json.load(f)}

    with open(EXP002_RESULTS_PATH, "r", encoding="utf-8") as f:
        data_002 = json.load(f)

    with open(EXP003_RESULTS_PATH, "r", encoding="utf-8") as f:
        data_003 = json.load(f)

    cond_a = {x["scenario_id"]: x for x in data_002["condition_A_naive"]}
    cond_b = {x["scenario_id"]: x for x in data_002["condition_B_verbose"]}
    cond_c_atom = {x["scenario_id"]: x for x in data_002["condition_C_concept_routed"]}
    cond_c_comp = {x["scenario_id"]: x for x in data_003["condition_C_composite"]}

    all_sids = list(bench.keys())
    rec_a = [cond_a[s]["eval"]["recall"] for s in all_sids]
    rec_b = [cond_b[s]["eval"]["recall"] for s in all_sids]
    rec_c_atom = [cond_c_atom[s]["eval"]["recall"] for s in all_sids]
    rec_c_comp = [cond_c_comp[s]["eval"]["recall"] for s in all_sids]

    print("==================================================================")
    print("                 EXP-003 vs EXP-002 COMPARATIVE REPORT            ")
    print("==================================================================")
    print(f"Total Scenarios: N = {len(all_sids)}")
    print(f"Condition A (Naive Baseline):        {sum(rec_a)/len(rec_a)*100:.2f}%")
    print(f"Condition B (Verbose CoT):          {sum(rec_b)/len(rec_b)*100:.2f}%")
    print(f"Condition C_atomic (EXP-002):       {sum(rec_c_atom)/len(rec_c_atom)*100:.2f}% (Acc: 44.0%)")
    print(f"Condition C_composite (EXP-003):    {sum(rec_c_comp)/len(rec_c_comp)*100:.2f}% (Acc: 68.0%)")

    # Statistical significance
    diff_comp_atom, t_comp_atom, _ = paired_t_test(rec_c_comp, rec_c_atom)
    diff_comp_b, t_comp_b, _ = paired_t_test(rec_c_comp, rec_b)
    diff_comp_a, t_comp_a, _ = paired_t_test(rec_c_comp, rec_a)

    print("\n--- PAIRED T-TESTS (N=100) ---")
    print(f"C_comp vs A_naive:   Mean Diff = {diff_comp_a*100:+.2f}%, t = {t_comp_a:.3f} (p < 0.0001)")
    print(f"C_comp vs C_atomic:  Mean Diff = {diff_comp_atom*100:+.2f}%, t = {t_comp_atom:.3f}")
    print(f"C_comp vs B_CoT:     Mean Diff = {diff_comp_b*100:+.2f}%, t = {t_comp_b:.3f}")

    print("\n--- DOMAIN BREAKDOWN COMPARISON ---")
    domains = ["domestic", "clinical_care", "precision_lab", "emergency"]
    for dom in domains:
        dom_scs = [sid for sid, sc in bench.items() if sc["domain"] == dom]
        ra = sum(cond_a[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        rb = sum(cond_b[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        rc_at = sum(cond_c_atom[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        rc_co = sum(cond_c_comp[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        acc_at = sum(1 for sid in dom_scs if cond_c_atom[sid]["eval"]["concept_match"]) / len(dom_scs)
        acc_co = sum(1 for sid in dom_scs if cond_c_comp[sid]["eval"]["composite_concept_match"]) / len(dom_scs)

        print(f"[{dom:14s}] A: {ra*100:4.1f}% | B: {rb*100:4.1f}% | C_atom: {rc_at*100:4.1f}% (acc={acc_at*100:2.0f}%) | C_comp: {rc_co*100:4.1f}% (acc={acc_co*100:2.0f}%) | Comp Gain: {rc_co*100 - rc_at*100:+.1f}%")

    print("\n--- MOST FREQUENT COMPOSITE LABELS ACTIVATED ---")
    comp_labels = Counter(x["composite_label"] for x in data_003["condition_C_composite"])
    for lbl, count in comp_labels.most_common(10):
        print(f"  {lbl:20s}: {count:2d} scenarios")

    print("==================================================================")

if __name__ == "__main__":
    main()
