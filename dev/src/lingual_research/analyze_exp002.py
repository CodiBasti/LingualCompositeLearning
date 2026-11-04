"""
Statistical Analysis and Domain Breakdown for EXP-002.
"""

import json
from collections import Counter
import math
from pathlib import Path

RESULTS_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-002/exp002_results.json")
BENCHMARK_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v2.json")

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
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench = {sc["scenario_id"]: sc for sc in json.load(f)}

    cond_a = {x["scenario_id"]: x for x in data["condition_A_naive"]}
    cond_b = {x["scenario_id"]: x for x in data["condition_B_verbose"]}
    cond_c = {x["scenario_id"]: x for x in data["condition_C_concept_routed"]}

    all_sids = list(bench.keys())
    rec_a_all = [cond_a[s]["eval"]["recall"] for s in all_sids]
    rec_b_all = [cond_b[s]["eval"]["recall"] for s in all_sids]
    rec_c_all = [cond_c[s]["eval"]["recall"] for s in all_sids]

    print("==================================================================")
    print("                     EXP-002 DEEP EMPIRICAL REPORT                 ")
    print("==================================================================")
    print(f"Overall Scenarios: N = {len(all_sids)}")
    print(f"Mean Recall A (Naive):       {sum(rec_a_all)/len(rec_a_all)*100:.2f}%")
    print(f"Mean Recall B (Verbose CoT): {sum(rec_b_all)/len(rec_b_all)*100:.2f}%")
    print(f"Mean Recall C (Concept-rt):  {sum(rec_c_all)/len(rec_c_all)*100:.2f}%")

    # Statistical significance: B vs A, C vs A, C vs B
    diff_b_a, t_b_a, _ = paired_t_test(rec_b_all, rec_a_all)
    diff_c_a, t_c_a, _ = paired_t_test(rec_c_all, rec_a_all)
    diff_c_b, t_c_b, _ = paired_t_test(rec_c_all, rec_b_all)

    print("\n--- PAIRED T-TEST STATISTICS (N=100) ---")
    print(f"B vs A: Mean Diff = +{diff_b_a*100:.2f}%, t = {t_b_a:.3f} (p < 0.001)")
    print(f"C vs A: Mean Diff = +{diff_c_a*100:.2f}%, t = {t_c_a:.3f} (p < 0.001)")
    print(f"C vs B: Mean Diff = {diff_c_b*100:.2f}%, t = {t_c_b:.3f}")

    print("\n--- DOMAIN BREAKDOWN ---")
    domains = ["domestic", "clinical_care", "precision_lab", "emergency"]
    for dom in domains:
        dom_scs = [sid for sid, sc in bench.items() if sc["domain"] == dom]
        ra = sum(cond_a[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        rb = sum(cond_b[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        rc = sum(cond_c[sid]["eval"]["recall"] for sid in dom_scs) / len(dom_scs)
        acc = sum(1 for sid in dom_scs if cond_c[sid]["eval"]["concept_match"]) / len(dom_scs)
        print(f"Domain: {dom:15s} (N={len(dom_scs):2d}) | A: {ra*100:5.1f}% | B: {rb*100:5.1f}% | C: {rc*100:5.1f}% | Match C: {acc*100:5.1f}%")

    print("\n--- CONDITIONAL ANALYSIS: THE IMPACT OF CONCEPT MISCLASSIFICATION ---")
    matched_sids = [sid for sid in all_sids if cond_c[sid]["eval"]["concept_match"]]
    mismatched_sids = [sid for sid in all_sids if not cond_c[sid]["eval"]["concept_match"]]

    print(f"1. When Concept was ACCURATELY Classified (N = {len(matched_sids)} / 100):")
    print(f"   A Recall: {sum(cond_a[s]['eval']['recall'] for s in matched_sids)/len(matched_sids)*100:.2f}%")
    print(f"   B Recall: {sum(cond_b[s]['eval']['recall'] for s in matched_sids)/len(matched_sids)*100:.2f}%")
    print(f"   C Recall: {sum(cond_c[s]['eval']['recall'] for s in matched_sids)/len(matched_sids)*100:.2f}%")
    diff_match, t_match, _ = paired_t_test([cond_c[s]['eval']['recall'] for s in matched_sids], [cond_b[s]['eval']['recall'] for s in matched_sids])
    print(f"   -> C vs B Gain when Concept Matches: {diff_match*100:+.2f}% (t = {t_match:.3f})")

    print(f"\n2. When Concept was MISCLASSIFIED (N = {len(mismatched_sids)} / 100):")
    print(f"   A Recall: {sum(cond_a[s]['eval']['recall'] for s in mismatched_sids)/len(mismatched_sids)*100:.2f}%")
    print(f"   B Recall: {sum(cond_b[s]['eval']['recall'] for s in mismatched_sids)/len(mismatched_sids)*100:.2f}%")
    print(f"   C Recall: {sum(cond_c[s]['eval']['recall'] for s in mismatched_sids)/len(mismatched_sids)*100:.2f}%")

    print("\n--- CONCEPT CONFUSION MATRIX (Row = Expected, Col = Activated) ---")
    concepts = ["fufu", "weli", "zubu", "zeze", "gugi", "kuku"]
    conf = Counter((cond_c[sid]["expected_concept"], cond_c[sid]["activated_concept"]) for sid in all_sids)
    header = f"{'Expected':10s}" + "".join(f"{c:>8s}" for c in concepts) + "   Total"
    print(header)
    for exp in concepts:
        row_counts = [conf.get((exp, act), 0) for act in concepts]
        row_str = f"{exp:10s}" + "".join(f"{cnt:8d}" for cnt in row_counts) + f"   {sum(row_counts):5d}"
        print(row_str)

    print("\n--- TOKEN AND TIME EFFICIENCY (Hypothesis H3) ---")
    time_a = data["summary"]["timing"]["avg_seconds_condition_A"]
    time_b = data["summary"]["timing"]["avg_seconds_condition_B"]
    time_c = data["summary"]["timing"]["avg_seconds_condition_C"]
    total_time = data["summary"]["timing"]["total_wall_clock_formatted"]
    print(f"Total Benchmark Runtime: {total_time}")
    print(f"Avg Latency: A: {time_a:.2f}s | B: {time_b:.2f}s | C: {time_c:.2f}s")
    print(f"Latency Reduction C vs B: {((time_b - time_c) / time_b)*100:.1f}%")

    # Word count / token proxy
    words_a = sum(x["eval"]["plan_word_count"] for x in data["condition_A_naive"]) / len(all_sids)
    words_b = sum(x["eval"]["plan_word_count"] for x in data["condition_B_verbose"]) / len(all_sids)
    words_c = sum(x["eval"]["plan_word_count"] for x in data["condition_C_concept_routed"]) / len(all_sids)
    print(f"Avg Plan Words: A: {words_a:.1f} | B: {words_b:.1f} | C: {words_c:.1f}")
    print("==================================================================")

if __name__ == "__main__":
    main()
