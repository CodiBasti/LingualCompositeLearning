# LCL-AUDIT-2026-11-05

Audit des Git-Stands `58df587fd9e74580e0c5a5cd7adcf8616e25b536`. Neue Dateien stehen ausschließlich in diesem Ordner und im späteren Abschlussbericht daneben. Originalquellen, Forschungsdokumente, Benchmark und bestehende Runs werden nicht geändert.

**Arbeitsstatus:** Abgeschlossen mit den im [Abschlussbericht](../review_audit_2026-11-05_FULL_PROJECT.md) und [new_metrics.json](new_metrics.json) ausgewiesenen Replikations- und Budgetgrenzen. Alle 40 neuen Szenarien sind in allen fünf Bedingungen vorhanden und inhaltlich bewertet; nicht abgeschlossene ursprüngliche Vergleichsblöcke werden ausdrücklich ausgewiesen.

## Beweis- und Methodenartefakte

- [source_manifest.json](source_manifest.json): SHA-256 aller 72 vorgefundenen getrackten Dateien, Git-Stand und Arbeitsbaumstatus.
- [protocol.json](protocol.json), [holdout.json](holdout.json): vor neuer Inferenz eingefrorenes Prüfprotokoll und 40 neue textuelle Szenarien, zehn je Domäne.
- [execution_freeze.json](execution_freeze.json): ursprüngliche Prompts und Quellcodeprüfsummen vor Ausführung. Die entsprechende Runnerfassung ist als [gpu_audit_v1.py](gpu_audit_v1.py) erhalten.
- [protocol_addendum.json](protocol_addendum.json), [execution_freeze_v2.json](execution_freeze_v2.json): dokumentierte technische Korrektur der Speicherbereinigung, konservative Anrechnung des angehaltenen Prozesses und zusätzlicher historischer deutscher EXP-001-Eingabestand. Inhalte und Vergleichspaare des Holdouts bleiben unverändert.
- [protocol_addendum_v3.json](protocol_addendum_v3.json), [execution_freeze_v3.json](execution_freeze_v3.json): endgültige Kontrollprompts vor dem ersten Kontrolllauf. Beide Baselines erhalten außer dem Routerkatalog auch alle atomaren Vertragsdetails und vier spezielle Phasenverträge. [information_matching_check.json](information_matching_check.json) bestätigt die unveränderten LCL-Router/Verträge und die vollständige Baselineinformation. Die zweite Runnerfassung ist als `gpu_audit_v2.py` erhalten.
- [review_method_freeze.json](review_method_freeze.json), [review_method_freeze_v2.json](review_method_freeze_v2.json): Auswertungsmethoden, Bewertungsregeln und Berichtsentwürfe vor neuer Kontrollinferenz; Änderungen der Narration und Nachweismatrix sind erhalten, statistische Methoden und Ratingguide unverändert.
- [supplement_freeze_v2.json](supplement_freeze_v2.json): feste Reihenfolge zum Ergänzen fehlender Vergleichsblöcke aus unverbrauchtem globalen Zeitbudget; keine Auswahl nach gemessenen Scores.
- [supplement_freeze_v3.json](supplement_freeze_v3.json), [gpu_watchdog.py](gpu_watchdog.py): gleiche Ergänzungsreihenfolge mit separater harter Zeitkontrolle. Nur registrierte Auditprozesse werden anhand PID und exakter Prozesserzeugungszeit überwacht; andere Anwendungen bleiben unangetastet. Die Zeitkontrolle greift konservativ vor acht Stunden, auch falls ein einzelner Generierungsaufruf länger als erwartet dauert.
- [supplement_freeze_v4.json](supplement_freeze_v4.json): offen dokumentierte Machbarkeitsänderung nach Primäranalyse, vor Judge-/Laufzeitinferenz. Der Ergänzungsprozess vervollständigt feste3×5-Laufzeitblöcke vor weiteren alten VHC-Fällen. Auswahl der20 Szenarien, drei Wiederholungen, Armrotation und Prompts bleiben gleich. Die vorherige V3-Fassung ist als `complete_remaining_v3.py` erhalten. Primäre Bewertungen und Tests ändern sich nicht.
- [semantic_rating_guide.md](semantic_rating_guide.md): Kriterien der inhaltlichen Einzelbewertung; kein menschlicher Goldstandard.
- [original_integrity_check.json](original_integrity_check.json): erneute Prüfung, ob Originaldateien unverändert geblieben sind.

## Ergebnisse und Nachweise

- [historical_metrics.json](historical_metrics.json), [historical_rows.csv](historical_rows.csv): unabhängige Rekonstruktion von 830 vorhandenen Datensätzen einschließlich deutscher Archive. `active` bezeichnet den Speicherort; EXP-001 stammt trotz aktuellem Speicherort aus deutschen Eingaben.
- [historical_evaluator_discrepancies.json](historical_evaluator_discrepancies.json): Abweichungen zwischen gespeicherten Invariantenzuordnungen und heutigem Evaluator.
- [pilot_replay.json](pilot_replay.json): alle 30 historischen Pilottexte werden auf wiederhergestellten deutschen Eingaben exakt neu erzeugt; ihre Bewertung unterscheidet sich trotzdem bei 11 Datensätzen vom gespeicherten alten Score.
- [conditional_routing.json](conditional_routing.json): explorative Prüfung der Aussage über korrekt geroutete Fälle; CoT und Concept Routing werden auf denselben 47 IDs verglichen, nicht auf verschiedenen Teilpopulationen.
- [historical_judge_provenance.json](historical_judge_provenance.json): Stichproben- und Bedingungszuordnung des bisherigen Judges.
- [evaluator_probes.json](evaluator_probes.json), [routing_structure_probes.json](routing_structure_probes.json): gezielte Gegenbeispiele und reine Strukturtests. Die Fehlerraten dieser konstruierten Fälle sind keine Populationsschätzungen.
- [git_provenance.json](git_provenance.json), [archive_identity.json](archive_identity.json): Datenversionen und Abgleich mit früheren Git-Ständen.
- [historical_token_audit.json](historical_token_audit.json): CPU-Retokenisierung gespeicherter Outputs; ursprüngliche Token-IDs sind nicht vorhanden.
- [manuscript_numbers.md](manuscript_numbers.md), [manuscript_numbers.json](manuscript_numbers.json): Abgleich wesentlicher Manuskriptzahlen und der Konfusionsmatrix mit dem rekonstruierten Bestand, einschließlich nicht rekonstruierbarer technischer Angaben.
- [research_process.md](research_process.md): dokumentierte Änderungen der H3-Schwellen/Messgrößen und Prüfung, ob die angegebenen Bestätigungen überhaupt zum ursprünglichen Endpunkt gehören.
- [judge_parser_probes.json](judge_parser_probes.json): zusätzliche konstruierte Fehlerfälle des originalen PASS-Parsers; keine Schätzung ihrer Häufigkeit in Modellläufen.
- [literature_audit.md](literature_audit.md), [citation_key_check.json](citation_key_check.json): verifizierte Primärquellen, Abgrenzung und Zitierkonsistenz.
- [contribution_matrix.md](contribution_matrix.md): für jeden beanspruchten Beitrag Vorarbeit, eigene Implementierung, isolierender Versuch und offene Neuheitsfrage.
- [claims.json](claims.json), `claim_matrix.csv`: Nachweismatrix zentraler Aussagen. Status vor Abschluss neuer Kontrollen beschreibt jeweils den explizit angegebenen vorhandenen Nachweis.
- `generation_trace.jsonl`, `replication.jsonl`, `controls.jsonl`, `judge.jsonl`, `latency.jsonl`: neue lokale Inferenzdaten, soweit bereits ausgeführt. Jeder Generierungsaufruf im Auditadapter protokolliert Prompts, Ausgabelimits und Tokenkosten. Der originale Judge liefert wie im Quellcode boolesches Urteil und Begründung; seine vollständige Rohantwort wird von der Originalmethode nicht zurückgegeben.
- `environment.json`, `environment_v1.json`, `gpu_sessions.jsonl`, `stage_status.jsonl`, `gpu_completion.json`: aktuelle Umgebung, Prozesszeit und Vollständigkeit. Die früheren historischen Softwareversionen sind damit nicht nachträglich rekonstruiert.
- `blinded_plans.json`, `blind_mapping.json`, `semantic_ratings.json`, `semantic_rows.json`: Ausgaben für die inhaltliche Einzelbewertung und ihre Zuordnung; werden erst bei Vorliegen neuer Kontrollpläne erzeugt.
- [semantic_rating_freeze.json](semantic_rating_freeze.json): alle200 Pläne/600 Anforderungen vor Offenlegung der Bedingungszuordnung einzeln bewertet und eingefroren. [primary_holdout_results.json](primary_holdout_results.json) erhält die primären Resultate unverändert, während die übrigen GPU-Stufen weiterlaufen.
- [rating_limitations.md](rating_limitations.md), [family_sensitivity.json](family_sensitivity.json), [routing_diagnostics.json](routing_diagnostics.json), [control_integrity_check.json](control_integrity_check.json): Grenzen des Audit-Holdouts, explorative Familien- und Routingdiagnostik sowie beobachtete Adapter-Parität.
- [runtime_drift.json](runtime_drift.json): ausdrücklich nachträgliche Zeitdiagnostik für exakt gleiche Prompts, Ausgaben und Tokenzahlen. Sie zeigt Zeitvariation, identifiziert aber deren Ursache nicht; kein zusätzlicher bestätigender Test.
- [claim_uncertainty.json](claim_uncertainty.json): Unsicherheit und Reichweite jedes zentralen Befunds; [claim_location_corrections.json](claim_location_corrections.json) dokumentiert korrigierte Zeilennummern der Auditnachweise bei unveränderten Aussagen/Statuswerten.
- [study_recommendations.md](study_recommendations.md): konkretisierte, nicht ausgeführte Folgeuntersuchungen für Menschen, Erklärungen, Robotik und Embeddings.

## Rechenmethoden

Es werden Einzelszenarien über IDs gepaart. Primär ist der Mittelwert szenarioweiser inhaltlicher Invariantenerfüllung auf dem neuen Holdout. Unklare Erfüllung zählt primär als nicht nachgewiesen und wird zusätzlich großzügig ausgewertet. Modelljudge und Regex sind Vergleichsinstrumente, keine Referenzwahrheit.

10.000 gepaarte Bootstrap-Wiederholungen, Seed `20261105`, zweiseitige gepaarte Sign-Flip-Tests und Holm-Korrektur der vier vorab definierten neuen Hauptvergleiche. Bei höchstens 18 nichtnull Differenzen werden alle Vorzeichenkombinationen exakt aufgezählt; sonst 10.000 Ziehungen mit Add-one-Korrektur. Zusätzliche gepaarte t-Tests verwenden eine unabhängige Berechnung über die unvollständige Betafunktion. Historische Befunde sind retrospektiv, Domänenanalysen explorativ. Heuristische Familiencluster werden als Sensitivitätsanalyse, nicht als erwiesene Abhängigkeitsstruktur behandelt. Wenige Cluster ergeben instabile Intervalle.

## Lokale Neuberechnung

Python 3.12 und NumPy sind in der geprüften Umgebung vorhanden. Alle Befehle vom Repositorywurzelverzeichnis aus:

```powershell
python -X utf8 -m unittest discover -s dev/reports/audit_2026-11-05 -p 'test_*.py' -v
python -X utf8 dev/reports/audit_2026-11-05/analyze.py historical
python -X utf8 dev/reports/audit_2026-11-05/structural_checks.py
python -X utf8 dev/reports/audit_2026-11-05/token_counts.py
python -X utf8 dev/reports/audit_2026-11-05/summarize_new.py
python -X utf8 dev/reports/audit_2026-11-05/analyze.py verify
```

`prepare.py` und die Freeze-Funktion sind absichtlich gegen erneutes Überschreiben ihrer eingefrorenen Dateien geschützt. `gpu_audit.py` nutzt ausschließlich den lokal gecachten Qwen-14B-Snapshot `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`, bfloat16, `do_sample=False`, ohne Netzdownload. Historische und neue Aufrufe schreiben niemals in die ursprünglichen Runverzeichnisse.

Ein GPU-Neustart ist keine kostenlose Neuwiederholung: Das gemeinsame Maximum beträgt acht Stunden, einschließlich Modellladen und bereits verbuchter angehaltener Prozesse. Teilweise abgeschlossene Arbeit darf nicht durch Löschen der Zeitbilanz als neuer Audit ausgegeben werden. Für eine unabhängige vollständige Wiederholung einen neuen Auditordner mit neuem Zeitbudget und Quellenmanifest anlegen; diesen Evidenzstand erhalten.

Die hier gemessenen Laufzeiten stammen von einem Windows-Desktop mit weiteren GPU-Anwendungen. Die Bedingungen sind ausgeglichen angeordnet, aber nicht vollständig gegen Fremdlast isoliert. Absolute Hardware-/Echtzeitaussagen sind daraus nicht zulässig.

## Abschlussprüfung und Artefaktintegrität

[validation_results.json](validation_results.json) dokumentiert erfolgreiche Neuberechnung und elf bestandene Methodentests. [final_checks.json](final_checks.json) prüft Datenformate, Bewertungsabdeckung, unveränderte Originaldateien, eingefrorene Primärresultate, lokale Links und das GPU-Zeitbudget. [process_exit_observations.json](process_exit_observations.json) unterscheidet Python-Abschlussmarker, äußere Shell-Rückgabecodes und den erwarteten Budgetstopp.

`release_manifest.json` enthält SHA-256-Prüfsummen aller abgelegten Auditartefakte und des Abschlussberichts. Ausgenommen sind das Manifest selbst und Python-Bytecodecaches. Nachprüfen mit:

```powershell
python -X utf8 dev/reports/audit_2026-11-05/release.py --verify
```

Die CPU-Neuberechnung und Berichterzeugung ist in [finish_audit.py](finish_audit.py) gebündelt. Das bestehende GPU-Zeitbudget ist ausgeschöpft; diese Abschlussprüfung startet keine Modellinferenz.
