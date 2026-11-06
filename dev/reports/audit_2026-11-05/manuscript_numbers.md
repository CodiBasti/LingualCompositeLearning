# Abgleich wesentlicher Manuskriptzahlen

Quellstand wie im Auditmanifest. Prozentangaben unterscheiden relative Änderung und Prozentpunkte. Diese Prüfung ist retrospektiv; technische Hyperparameter und definierte Grenzwerte sind keine gemessenen Ergebnisse.

| Fundstelle | Größe | Behauptet | Rekonstruiert | Befund |
|---|---|---|---|---|
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | A: recall | 35 | 35.0 | reconstructed |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | A: latency seconds | 6.74 | 6.7392900000000004 | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | B: recall | 50.25 | 50.24999999999999 | reconstructed |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | B: latency seconds | 10.13 | 10.13022 | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | C: recall | 46.25 | 46.25 | reconstructed |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | C: latency seconds | 8.54 | 8.54228 | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | D: recall | 47.25 | 47.25 | reconstructed |
| PAPER_MANUSCRIPT.md:204-207; main.tex:107-110 | D: latency seconds | 8.67 | 8.674180000000002 | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:205-207; main.tex:108-110 | B-A: paired t | 5.846 | 5.845991725932527 | reconstructed_to_reported_rounding |
| main.tex:108-110 | B-A: two-sided p | <0.0001 | 6.480591708719518e-08 | reconstructed |
| PAPER_MANUSCRIPT.md:205-207; main.tex:108-110 | C-A: paired t | 4.753 | 4.752760502525474 | reconstructed_to_reported_rounding |
| main.tex:108-110 | C-A: two-sided p | <0.0001 | 6.8089332251975025e-06 | reconstructed |
| PAPER_MANUSCRIPT.md:205-207; main.tex:108-110 | D-A: paired t | 4.882 | 4.627769842651106 | mismatch |
| main.tex:108-110 | D-A: two-sided p | <0.0001 | 1.1220117700859436e-05 | reconstructed |
| PAPER_MANUSCRIPT.md:219-222; main.tex:122-125 | domestic four recalls A/B/C/D | [39.2, 63.3, 62.5, 58.3] | [39.166666666666664, 63.33333333333333, 62.5, 58.333333333333336] | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:219-222; main.tex:122-125 | emergency four recalls A/B/C/D | [43.3, 41.7, 45, 53.3] | [43.333333333333336, 41.66666666666667, 45.0, 53.333333333333336] | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:219-222; main.tex:122-125 | precision_lab four recalls A/B/C/D | [28, 41, 31, 30] | [28.000000000000004, 41.0, 31.0, 30.0] | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:219-222; main.tex:122-125 | clinical_care four recalls A/B/C/D | [32.5, 49.2, 43.3, 47.5] | [32.5, 49.166666666666664, 43.333333333333336, 47.5] | reconstructed_to_reported_rounding |
| PAPER_MANUSCRIPT.md:16 | Composite-naive gain | 12.25 | 12.25 | reconstructed |
| main.tex:39 | Composite-naive gain | 13 | 12.25 | archive_only |
| PAPER_MANUSCRIPT.md:227 | Emergency relative gain | 27.8 | 28.000000000000004 | rounding_mismatch |
| PAPER_MANUSCRIPT.md:228 | Latency reduction %: composite/atomic | [14.4, 15.7] | [14.37323177581531, 15.675276548781758] | approximately_reconstructed |
| PAPER_MANUSCRIPT.md:228 | Seconds saved versus CoT | >1.45 | [1.456039999999998, 1.5879399999999997] | reconstructed |
| PAPER_MANUSCRIPT.md:59; main.tex:50 | CoT latency increase versus naive % | 30-50 | 50.31583445733896 | approximately_reconstructed |
| PAPER_MANUSCRIPT.md:59; main.tex:50 | CoT generated-token increase % | 200-300 | 50.35848583604914 | mismatch |
| PAPER_MANUSCRIPT.md:36,58; main.tex:49 | Failure percentage | 66.5 | 65.0 | archive_only_and_construct_mismatch |
| PAPER_MANUSCRIPT.md:70; main.tex:91-94 | Domain scenario counts | [30, 30, 25, 15] | [30, 30, 25, 15] | reconstructed |
| PAPER_MANUSCRIPT.md:16,186; main.tex:39,98 | Inference runs | 400 | {'scenario_condition_records': 400, 'generation_calls_required_by_code': 600, 'distinct_scenarios': 100} | unit_ambiguity |
| PAPER_MANUSCRIPT.md:71-72 | Atomic/composite routing old figures | [44, 68] | [47.0, 72.0] | archive_only |
| PAPER_MANUSCRIPT.md:254; main.tex:131 | Precision composite label coverage | 88 | 88.0 | reconstructed |
| PAPER_MANUSCRIPT.md:243-250 | 6x6 atomic confusion matrix | [[10, 1, 0, 0, 9, 1], [10, 24, 0, 0, 8, 1], [6, 1, 3, 0, 1, 0], [5, 1, 0, 0, 0, 0], [3, 2, 0, 0, 3, 0], [0, 0, 0, 0, 4, 7]] | [[10, 1, 0, 0, 9, 1], [10, 24, 0, 0, 8, 1], [6, 1, 3, 0, 1, 0], [5, 1, 0, 0, 0, 0], [3, 2, 0, 0, 3, 0], [0, 0, 0, 0, 4, 7]] | reconstructed |
| PAPER_MANUSCRIPT.md:288 | fufu-weli activation count | 84 | 85 | archive_only |
| PAPER_MANUSCRIPT.md:268-270 | Judge regex passes/rejections A/B/C | [[12, 5], [14, 10], [14, 6]] | [[12, 5], [14, 10], [14, 6]] | counts_reconstructed_condition_misattributed |
| PAPER_MANUSCRIPT.md:186; main.tex:98 | Historical VRAM allocation GB | 27.65 | None | not_reconstructible |
| PAPER_MANUSCRIPT.md:119-128; main.tex:66-78 | 1/1.5m, <3N, 1.5N/s,0dB | chosen policy definitions | None | definitions_not_empirical_findings |
| PAPER_MANUSCRIPT.md:275-279 | Purported quotation | Axiom 1: I must maintain a wide standoff and crawl speed near the infant | 0 | not_located_in_preserved_plans |
| PAPER_MANUSCRIPT.md:275-279 | Purported quotation | Step 1: Move directly across the room. Step 2: Grasp the cup. | 0 | not_located_in_preserved_plans |

Vollständige Interpretationsgrenzen pro Zeile: [manuscript_numbers.json](manuscript_numbers.json). Tabellenwerte sind aus Einzelzeilen rekonstruiert; Rohtexte wurden für die beiden wörtlich markierten Beispiele durchsucht. Fehlendes wörtliches Zitat widerlegt nicht die Möglichkeit ähnlicher Fehler.
