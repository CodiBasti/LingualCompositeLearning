# Sachlicher Red-Team-Audit: Lingual Composite Learning

**Auditdatum:** 5. November 2026 · **Quellstand:** `58df587fd9e74580e0c5a5cd7adcf8616e25b536` · **Bericht erzeugt:** `2026-11-05T22:23:38.120694+00:00`

**Reviewer:** Codex-Assistent als einzelner technischer Auditor. Keine externe Peer-Review-Kommission, kein unabhängiger menschlicher Goldstandard. Die Neuberechnung wurde separat von den ursprünglichen Analyseskripten implementiert.

## 1. Urteil

| Perspektive | Urteil |
|---|---|
| Wissenschaftliche Belastbarkeit | Vorhanden sind überprüfbare Daten eines textuellen Prompting-Experiments. Die zentralen Schlussfolgerungen über latentes Lernen, garantierte Robotersicherheit, allgemeine CoT-Überlegenheit und Erklärungstreue werden dadurch nicht getragen. |
| Projektentscheidung | **Neuausrichten.** Die bisherige Gesamterzählung trägt nicht. Einzelne Fragen zur Regelstruktur und menschlichen Begriffsbildung bleiben untersuchbar; sie müssen voneinander getrennt und gegen einfachere Erklärungen geprüft werden. |
| Publikationsreife des geprüften Manuskripts | **2/10 — Strong Reject** auf der im Repository verwendeten Review-Skala. Zentrale Validitätsprobleme und nicht belegte Beiträge erfordern neue Evidenz und substanzielle Neufassung. Maßstab: [Review-Skill](../../.agents/skills/critical-peer-reviewer/SKILL.md), 2 = zentraler methodischer Fehler. Keine Annahmeprognose. |

Die Bewertung betrifft die belegten Aussagen und die aktuelle Implementierung. Ein fehlender Nachweis widerlegt nicht jede zukünftige Ausgestaltung der Idee. Umgekehrt kann eine zukünftige Vision keinen fehlenden Nachweis der aktuellen Arbeit ersetzen.

Hohe Sicherheit besteht bei Quellcodebefunden, Datenzuordnung und rekonstruierten Zahlen. Die semantische Einzelbewertung und deren Übertragbarkeit sind eingeschränkter belastbar. Aus diesem Audit lassen sich keine tatsächlichen Verletzungs-, Kollisions- oder klinischen Sicherheitsraten ableiten.

## 2. Datengrundlage, Unabhängigkeit und Vollständigkeit

Alle **72 ursprünglichen getrackten Dateien** wurden per SHA-256 gesichert und am Ende unverändert vorgefunden. Forschungsdokumente und Originalresultate wurden entsprechend dem Auftrag nicht automatisch korrigiert. Manifest: [source_manifest.json](audit_2026-11-05/source_manifest.json); Abschlussprüfung: [original_integrity_check.json](audit_2026-11-05/original_integrity_check.json).

Die Rekonstruktion umfasst **830 vorhandene Szenario-Bedingungsdatensätze**: 30 Pilotdatensätze sowie je 400 aktive und archivierte EXP-002/003-Datensätze. Aktive englische und ältere deutsche Ergebnisse wurden getrennt ausgewertet. Quelle: [historical_rows.csv](audit_2026-11-05/historical_rows.csv).

Neue lokale Inferenz: Qwen2.5-14B-Instruct, Snapshot `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`, RTX 5090, bfloat16 und greedy Decoding (`do_sample=False`), ohne Netzdownload. Python 3.12.10, PyTorch 2.11.0+cu128, Transformers 5.22.1. Aufrufparameter, Prompts und vollständige Plannertexte stehen im Generierungstrace; Umgebungsnachweis: [environment.json](audit_2026-11-05/environment.json). Dies beschreibt die Auditläufe und ersetzt keine fehlenden historischen Umgebungsdaten.

Das ursprüngliche Protokoll, die 40 neuen Szenarien und sämtliche neuen Planner-Prompts wurden vor der entsprechenden Inferenz eingefroren. Der Auditor kannte die bisherigen Projektergebnisse; dies ist keine nachträgliche Präregistrierung der historischen Forschung. Der neue Holdout wurde vom selben Auditor entworfen und ist keine unabhängige externe Benchmarkvalidierung.

Protokoll und Änderungen vor Kontrollinferenz: [protocol.json](audit_2026-11-05/protocol.json), [protocol_addendum.json](audit_2026-11-05/protocol_addendum.json), [protocol_addendum_v3.json](audit_2026-11-05/protocol_addendum_v3.json), [execution_freeze.json](audit_2026-11-05/execution_freeze.json), [execution_freeze_v2.json](audit_2026-11-05/execution_freeze_v2.json), [execution_freeze_v3.json](audit_2026-11-05/execution_freeze_v3.json). Nach dem ersten Pilotlauf wurde die Cachebereinigung des isolierten Adapters ergänzt. Vor jeder neuen Kontrollinferenz wurden beide Baselines zusätzlich um sämtliche atomaren Vertragsdetails und vier besonderen Phasenvorlagen erweitert. Der Routerkatalog allein enthielt nicht alle später eingefügten Regeln. Router, LCL-Verträge, Modell, Präzision, Holdout, Ausgabelimits und Hauptvergleiche blieben unverändert. Angehaltene Prozesse, Quellfassungen und konservativ angerechnete Zeiten sind erhalten. Bis zu diesen Änderungen wurden keine neuen Kontroll- oder Holdout-Ergebnisse erzeugt oder gesichtet.

Beide Baselines sehen die gesamte mögliche Policyinformation, LCL setzt selektierte Verträge ein; identische Eingabetokenzahlen werden nicht behauptet. Alle Tokens werden mitgemessen. Der Abgleich steht in [information_matching_check.json](audit_2026-11-05/information_matching_check.json). Ungenutzte Zeit der weichen Stufenbudgets wird nur anhand fehlender IDs und verfügbarer Zeit verteilt. Die anfängliche Ergänzungsreihenfolge steht in [supplement_freeze_v2.json](audit_2026-11-05/supplement_freeze_v2.json). Nach der eingefrorenen Primäranalyse, aber vor jeder neuen Judge-/Laufzeitinferenz wurde sie aus Machbarkeitsgründen geändert: Angefangene 3×5-Laufzeitblöcke werden im Ergänzungsprozess vor weiteren alten VHC-Fällen vervollständigt. Szenarioauswahl, Armrotation, Prompts und Haupttests bleiben gleich. Die im Hauptprozess geladene Schleife bleibt unverändert; die abweichende Ergänzungsreihenfolge und ihre Grenzen stehen in [supplement_freeze_v4.json](audit_2026-11-05/supplement_freeze_v4.json). Dies ist ausdrücklich keine vor der Primäranalyse festgelegte Ablaufentscheidung. Das harte Gesamtmaximum bleibt acht Stunden.

| Prüfteil | Dokumentierter Ausgang |
|---|---|
| Bestandsdaten, Code, Aussagen, Quellen | Rekonstruktion, Gegenbeispiele und Literaturabgleich ausgeführt; zentrale Aussagen einzeln in der Nachweismatrix bewertet. |
| EXP-001 | Aktueller englischer Eingabestand und historischer deutscher Eingabestand separat gerechnet; siehe neue Replikationsdaten. |
| EXP-002/003-Replikation | 48/400 neue Bedingungsdatensätze; gleiche vorab geordnete Szenarioblöcke. Teilumfang wird nicht als Vollreplikation bezeichnet. |
| Kontrollvergleich | 425/700 Datensätze; 40/40 vollständige neue Szenarien, 45/100 vollständige bestehende Szenarien über alle fünf Bedingungen. |
| Inhaltliche Einzelbewertung | 200 Pläne, 600 Einzelanforderungen, 130 unklare Entscheidungen. |
| Lokaler Original-Judge | 600/600 Anforderungsprüfungen; gleicher Checkpoint wie Generator, ohne Anspruch auf unabhängige Referenzwahrheit. |
| Wiederholte Laufzeitmessung | 140/300 Durchläufe; 4/20 Szenarien vollständig mit allen Bedingungen und drei Wiederholungen. Wiederholungen erhöhen das Genauigkeits-N nicht. |
| Neue Humanstudie / Simulation / physischer Roboter / Training | Vereinbarungsgemäß nicht durchgeführt; verbleibende Nachweislücken und Folgestudien explizit spezifiziert. |

**Zeitbilanz:** 7.992 konservativ verbuchte lokale GPU-Prozessstunden von maximal 8. Die Bilanz enthält Laden, Mess-/Dateiverwaltungsanteile und den angehaltenen Prozess; sie ist keine Messung reiner GPU-Kernelzeit. Vollständige Stufen-, Fehler- und Budgetbilanz: [new_metrics.json](audit_2026-11-05/new_metrics.json).

Der Ergänzungsprozess wurde durch die unabhängige Zeitkontrolle an der harten Budgetgrenze beendet. Ein danach noch laufender unvollständiger Wiederholungsblock wurde nicht in die gepaarten Statistiken aufgenommen; bereits protokollierte Einzelaufrufe bleiben im Generierungstrace erhalten und ihre Zeit ist mitgerechnet. Die fehlenden Originalreplikationen, VHC-Kontrollen und Wiederholungen werden nicht als durchgeführt ausgegeben.

Die Laufzeiten wurden auf einem Windows-Desktop mit weiteren GPU-Anwendungen gemessen. Rotierende Reihenfolge und Wiederholungen reduzieren Reihenfolgeeffekte, stellen aber keine vollständig isolierte Hardwaremessung her. Historische Software- und Modellrevisionen fehlen; ein heutiger Lauf rekonstruiert diese Angaben nicht rückwirkend.

Es wurden erhebliche zeitliche Schwankungen beobachtet. Bei 100 mehrfach ausgeführten Gruppen mit exakt gleichen Prompt-/Outputtexten und gleichen Tokenzahlen beträgt das mediane Verhältnis längster zu kürzester Dauer 3.93; das größte Verhältnis 19.7. Ursache und Anteile von Fremdlast, Paging, Takt-/Temperatur- und Cacheeffekten sind nicht identifiziert. Diese nachträgliche deskriptive Diagnostik begrenzt allgemeine Latenzbehauptungen: [runtime_drift.json](audit_2026-11-05/runtime_drift.json).

Der lokale Python-Hauptlauf hat seinen Abschlussmarker `finished` und eine geschlossene Zeitbilanz geschrieben. Die äußere PowerShell-/Tee-Toolsitzung meldete beim nachträglichen Abholen Exitcode 1, ohne protokollierten Pythonfehler; dessen genaue Ursache ist nicht rekonstruiert. Ein separat nachgewiesener Python-Exitcode 0 wird nicht behauptet. Vollständigkeit wird anhand der tatsächlichen Datensätze geprüft. Prozessbeobachtungen: [process_exit_observations.json](audit_2026-11-05/process_exit_observations.json).

## 3. Unabhängige Rekonstruktion der bisherigen Ergebnisse

Die folgenden Werte sind aus den einzelnen gespeicherten Invariantenzuordnungen berechnet. Sie sind **textuelle Evaluatorscores**, keine gemessene Ausführungssicherheit.

| Aktiver VHC-100-Stand | Recall | Alle vier Invarianten bestanden | Routingmetrik | Gespeicherte mittlere Zeit |
|---|---:|---:|---:|---:|
| Naive A | 35,00 % | 3,00 % | nicht verfügbar | 6.739 s |
| Verbose CoT B | 50,25 % | 8,00 % | nicht verfügbar | 10.130 s |
| Atomar C | 46,25 % | 7,00 % | 47,00 % | 8.542 s |
| Composite D | 47,25 % | 7,00 % | 72,00 % | 8.674 s |

| Gepaarter Vergleich | Differenz | 95-%-Bootstrapintervall | Tatsächliches zweiseitiges t-Test-p |
|---|---:|---|---:|
| D-A | +12.25 Prozentpunkte | [+7.25, +17.50] Prozentpunkte | 1.12201e-05 |
| D-B | -3.00 Prozentpunkte | [-7.75, +2.00] Prozentpunkte | 0.22723 |
| D-C | +1.00 Prozentpunkte | [-3.25, +5.25] Prozentpunkte | 0.644266 |

Notfalldomäne D−B: **+11,67 Prozentpunkte**, N=15, t-Test-p=0.06842, exakter Sign-Flip-p=0.12109. Der Mittelwertvorteil ist vorhanden, eine signifikante Überlegenheit auf 5-%-Niveau schon vor Mehrfachkorrektur nicht belegt. Die Domänenauswahl ist explorativ.

Gesamte Sign-Flip-Tests, Holm-Korrektur, Domänen und heuristische Cluster-Sensitivität: [historical_metrics.json](audit_2026-11-05/historical_metrics.json). Die Familiengruppen beruhen auf Domäne und erwartetem Konzept, nicht auf nachgewiesenen identischen Templates. Der Benchmark hat 100 verschiedene Kontexte und 100 verschiedene Invariantensätze; eine Behauptung bloßer Datenduplikation wäre hier unbelegt. Bei nur drei Notfall-Familien sind Clusterintervalle besonders instabil.

### Datenherkunft und Versionsmischung

EXP-001 verwendete ursprünglich deutsche Befehle. Sein Ergebnis-JSON blieb unverändert, während der zugehörige Benchmark ins Englische übersetzt wurde. Die aktive Ablage macht diesen Lauf nicht zu einem frischen englischen Versuch. Gegenüber dem heutigen Evaluator ändern sich bei 11 der 30 Pilotpläne die Invariantenzuordnungen; die damalige vollständige Evaluatorfassung ist nicht versioniert verfügbar.

Die erneute Ausführung auf den rekonstruierten deutschen Pilot-Eingaben reproduziert alle **30/30 gespeicherten Plantexte exakt**. Mit dem heutigen Evaluator ändern sich dennoch 11/30 Invariantenzuordnungen. Das stützt die Reproduzierbarkeit der Pilottexte und grenzt das Problem auf die nicht versionierte damalige Bewertung ein; es authentifiziert nicht automatisch jede historische Ausführungsbehauptung. Nachweis: [pilot_replay.json](audit_2026-11-05/pilot_replay.json).

Die archivierten EXP-002/003-Bedingungsdatensätze entsprechen dem ersten Git-Stand. Bei EXP-003 wurde ausschließlich ein Teil der Laufzeitzusammenfassung verändert: Die Gesamtzeit steht im Archiv auf null. Das ist mit dem Verhalten eines bereits vollständig gefüllten Resume-Laufs vereinbar, der eine neue Nullzeit-Zusammenfassung schreibt; der historische Vorgang selbst ist nicht protokolliert.

Mehrere Texte mischen ältere und aktuelle Zahlen: 44/68 % und 84 Paaraktivierungen stehen neben 47/72 % und tatsächlich 85 aktuellen `fufu-weli`-Aktivierungen. Der LaTeX-Abstract nennt noch ältere Domänenvorteile, während seine Tabellen aktuelle Ergebnisse enthalten. Der Composite-t-Wert 4,882 stimmt mit dem aus den aktuellen Rohdaten rekonstruierten Wert 4,62777 nicht überein. Der p-Bereich gegenüber Naive bleibt in dieser Neuberechnung tatsächlich unter 0,0001; ein fehlerhafter t-Wert macht nicht automatisch jede p-Aussage falsch.

Nachweise: [git_provenance.json](audit_2026-11-05/git_provenance.json), [archive_identity.json](audit_2026-11-05/archive_identity.json), [historical_evaluator_discrepancies.json](audit_2026-11-05/historical_evaluator_discrepancies.json). Ein gesonderter Abgleich wesentlicher Manuskriptzahlen einschließlich Tabellen, Konfusionsmatrix, Zählungseinheiten und nicht rekonstruierbarer VRAM-Angabe steht in [manuscript_numbers.md](audit_2026-11-05/manuscript_numbers.md). Zwei wörtlich gesetzte illustrative CoT-Beispiele wurden in den erhaltenen Plänen nicht gefunden; sie benötigen eine genaue Quelle oder eine Kennzeichnung als Illustration. Daraus folgt nicht, dass ähnliche Fehlplanungen unmöglich sind.

## 4. Zentrale methodische Befunde

### F1 — Der Evaluator misst die behauptete Sicherheit nicht zuverlässig · zentral

Unter anderem werden „0,2m Abstand“ für eine geforderte 1,5m-Grenze und eine ausdrückliche Beschleunigung neben einem Kind als Erfüllung gewertet. Eine richtige Regel im Vorspann kann einen widersprechenden Aktionsschritt überdecken. Auch falsche Kraftwerte und unzulässige Phasenwechsel passieren die Prüfung; eine korrekte Abstandsparaphrase fällt dagegen durch. Sieben von neun konstruierten negativen Fällen werden akzeptiert, eine von drei positiven Paraphrasen wird abgelehnt. Diese kleine adversariale Sammlung beweist konkrete Fehlertypen, schätzt aber keine globale Fehlerrate.

Konsequenz: Wiederholbare Regexwerte sind vorhanden; ihre Verwendung als Sicherheits- oder Garantiebeleg ist nicht zulässig. Vollständige Texte und erwartete/erhaltene Entscheidungen: [evaluator_probes.json](audit_2026-11-05/evaluator_probes.json).

### F2 — Der behauptete latente Lern- und Durchsetzungsmechanismus fehlt · zentral

Die Implementierung wählt durch einen Prompt ein oder zwei Namen, schlägt dazu Python-Texttemplates nach und erzeugt mit einem unveränderten Instruct-Modell einen weiteren Text. Es gibt weder Training neuer Embeddings noch eine Aktionsgraphenprüfung, einen constrained Aktionsdecoder oder einen ausführenden Sicherheitsmonitor. Dass ein Sprachmodell intern Aktivierungen besitzt, belegt keine gesondert gelernte LCL-Geometrie. Die mathematische Forderung nach Wahrscheinlichkeit null für verbotene Aktionen ist eine Spezifikation, kein Implementierungsnachweis.

Konsequenz: Zulässig ist die Beschreibung als zweistufiges textuelles Routing mit Vertragsvorlagen. Aussagen über strukturell unmögliche gefährliche Trajektorien, reale Wahrnehmung oder garantierte Motoraktionen sind damit nicht belegt. Quelle: [EXP-002](../src/lingual_research/runner_exp002.py), [EXP-003](../src/lingual_research/runner_exp003.py).

### F3 — Kompositionsmetrik und Grammatik tragen die Schlussfolgerung nicht · zentral

Atomar wird ein einzelnes erwartetes Label exakt verglichen. Bei Composite genügt, dass dieses Label in bis zu zwei Vorhersagen enthalten ist; vollständige mehrteilige Ziellabels fehlen. Das konstante Paar `fufu-weli` würde bereits 64 % Abdeckung erreichen. Aktuell wird dieses Paar in 85/100 Fällen gewählt. Der gemessene downstream Recallgewinn gegenüber atomar beträgt nur einen Prozentpunkt und ist nicht signifikant.

Der Parser ordnet Namen nach festem Katalog, nicht nach generierter Reihenfolge. Die Synthese bildet eine Menge; `fufu-weli` und `weli-fufu` ergeben identische Verträge. Die behauptete nichtkommutative Sprache ist so nicht implementiert. Auch rekursive Vererbung an `gugi` wird für `zubu` nicht berechnet. Dies widerlegt die entsprechende Behauptung zur aktuellen Implementierung, nicht jede denkbare spätere Grammatik.

Nachweise: [routing_structure_probes.json](audit_2026-11-05/routing_structure_probes.json), [historical_metrics.json](audit_2026-11-05/historical_metrics.json). Auf den 47 korrekt atomar gerouteten Szenarien erreicht atomar 52,13 %, CoT auf denselben IDs 51,06 %. Die kleine Differenz ist unsicher (95-%-Intervall etwa −4,79 bis +6,91 Prozentpunkte; t-Test-p=0,728). Die nach dem Routing ausgewählte Teilmenge ist explorativ und kein End-to-End-Erfolgsnachweis: [conditional_routing.json](audit_2026-11-05/conditional_routing.json).

### F4 — Der alte Judge wurde falsch zugeschrieben und überinterpretiert · zentral

Die 60 Checks stammen aus den ersten fünf VHC-Szenarien, sämtlich domestic: 5 Szenarien × 4 Invarianten × 3 Bedingungen. Der Judge verwendet denselben Qwen-Checkpoint. Seine dritte Bedingung sind **atomare EXP-002-Ausgaben**; die Manuskripttabelle bezeichnet sie als Composite. Die 71,4 % sind korrekt als 10 abgelehnte von 14 Regex-Pässen in genau dieser CoT-Stichprobe berechnet. Sie sind keine Gesamtfehlerrate und keine unabhängig validierte Wahrheit. Für atomar verwirft derselbe Judge 6/14 Regex-Pässe.

Der Judge prüft außerdem keine menschlich angeforderte Erklärung und keine kausale Erklärungstreue. H5 wird durch diesen Versuch nicht untersucht. Zuordnung und Auszüge stimmen mit den jeweiligen atomaren Daten überein: [historical_judge_provenance.json](audit_2026-11-05/historical_judge_provenance.json).

Auch sein Antwortparser ist fehleranfällig: Die erste Zeile wird auf die Teilzeichenfolge „PASS“ geprüft. Konstruierte Antworten wie „DECISION: NOT PASS“ oder „DECISION: FAIL (not PASS)“ werden als bestanden gewertet. Das belegt einen möglichen Parserfehler, keine beobachtete Häufigkeit in den Modellläufen. Weil die Originalmethode nur Urteil und Begründung zurückgibt, ist ihre vollständige Rohantwort auch im originalgetreu aufgerufenen neuen Judge nicht erhalten. Proben: [judge_parser_probes.json](audit_2026-11-05/judge_parser_probes.json).

### F5 — Outputlimits sind eine konkrete alternative Erklärung · zentral

CoT darf in EXP-002 300 neue Tokens erzeugen, atomare/composite Planung 250; Routing benötigt weitere Aufrufe und Tokens. Bei Retokenisierung liegen 97/100 CoT-Ausgaben nahe dem 300er-Limit und alle 100 Composite-Ausgaben am 250er-Limit. In geprüften CoT-Beispielen endet der Text vor oder direkt am Beginn des Aktionsplans. Das ist mit Abschneiden vereinbar. Mangels gespeicherter ursprünglicher Token-IDs/EOS ist es kein vollständiges historisches Abbruchprotokoll.

Damit sind Evaluatorartefakte und unzureichendes Ausgabeformat/-budget konkrete Alternativen zur behaupteten Ursache „Attention Drift“. Es liegen keine Attentionmessung und keine kausale Intervention dazu vor. Ein bestimmter CoT-Prompt mit engem Limit ist auch kein Stellvertreter für alle trainierten Reasoning- oder VLA-Verfahren.

Wortzählung ist keine Tokenmessung. Einzelne Begriffe haben hier 2–3 Tokens, `fufu-weli` fünf. Daraus folgen keine 98 % Kompression des gesamten zweistufigen Prompts. Die vorhandenen EXP-002-Ausgaben retokenisieren im Mittel auf 299,89 Tokens für CoT und 199,45 für Naive: etwa +50,36 %, nicht die behaupteten +200–300 %. Retokenisierung: [historical_token_audit.json](audit_2026-11-05/historical_token_audit.json); neue vollständige Aufrufkosten: [generation_trace.jsonl](audit_2026-11-05/generation_trace.jsonl).

### F6 — Formale Definitionen und physikalische Bedeutung sind uneinheitlich · wesentlich

Die Dokumente verwenden unterschiedliche Prioritätsrelationen und Kraftanstiegsgrenzen von 1,0 beziehungsweise 1,5N/s. Ein pauschaler 3N-Vertrag impliziert beispielsweise keine aufgabenspezifische Grenze unter 0,5N oder 0,2N, die der Benchmark ebenfalls verlangt. Abstand zum Fahrgestell, Abstand zu einem unbeteiligten Menschen und Greifkontakt am Ziel werden nicht sauber als verschiedene Relationen/Phasenbedingungen typisiert.

„0dB“ ohne Bezugsgröße ist keine wohldefinierte Stilleanforderung. 0dBA bezeichnet beispielsweise eine Hörschwelle, nicht das Fehlen von Schall ([Health Canada](https://www.canada.ca/en/health-canada/services/noise-your-health.html)). Ein Produkt aus fünf Kategorien beweist weder Orthogonalität noch Vollständigkeit eines physikalischen Zustandsraums. Diese Punkte verlangen präzise Spezifikationen und Validierung; es gibt im Projekt keine entsprechenden physischen Messungen.

### F7 — Generalisierung und menschlicher Nutzen bleiben offen · wesentlich

Vier thematische Domänen im selben selbst erstellten Benchmark sind ein domänenübergreifender Texttest. Es fehlen ein nachgewiesener Entwicklungs-/Testsplit und ein Test auf vorher unberührten Domänen oder Kompositionsfamilien. Eine kausale Erklärung der Klassifikationsfehler durch eine „Dimensionality Trap“ ist nicht isoliert.

Für die ursprüngliche Frage menschlicher Intentionserkennung gibt es keine eigenen Probandendaten. Universelle Aussprechbarkeit, Sprachneutralität und phonosemantischer Lernnutzen wurden ebenfalls nicht gemessen. Diese Forschungsfragen sind ungetestet; sie sind durch die vorliegenden Modellresultate weder bestätigt noch umfassend widerlegt.

### F8 — Frühere Reviews sind keine belastbare Freigabe · zentral

Die Reviews mit 8,2/8,5 Punkten behaupten vollständige Zahlengleichheit und actiongebundene Motorsicherheit, ohne die oben nachgewiesenen Unterschiede abzusichern. Ein Review empfiehlt ausdrücklich, den Gesamtvorsprung von CoT über den Judge als Artefakt zu erklären; dieser Judge prüft jedoch nur fünf domestic-Szenarien und kein Composite. Das ist eine unbelegte Verteidigungsstrategie, kein durchgeführter Gegenbeweis.

Unabhängigkeit, Identität und Prüfprotokolle dieser Reviewer sind nicht dokumentiert. Die Bezeichnung „Area Chair“ oder „independent“ schafft keine externe Begutachtung. Die vorhandenen Reviews dürfen als historische Projektartefakte erhalten bleiben; ihre Freigaben sollten nicht als Nachweis für Publikationsreife verwendet werden.

### F9 — Erfolgskriterien und Endpunkte wurden verändert · zentral

H3 verlangte im ältesten erhaltenen Hypothesenpapier mindestens 50 % weniger Planungstokens und nannte unter 20 % Ersparnis als Falsifikationsgrenze. Die aktuelle Fassung nennt 10–50 % Token-/Latenzreduktion mit einer 10-%-Grenze. H1 behält 80 % über diverse Szenarien als Kriterium, wird aber anhand eines niedrigeren Gesamtwerts und einer Teilgruppe als bestätigt geführt. Bei H2 wird ein p-Wert gegen Naive als Beleg gegenüber CoT eingesetzt; H5 ersetzt einen Erklärungstest durch Planbewertung. Der älteste Git-Stand enthält bereits Ergebnisdateien: Eine unveränderte prospektive Festlegung ist damit nicht belegt. Detaillierter Versionsvergleich und Grenzen der zeitlichen Rekonstruktion: [research_process.md](audit_2026-11-05/research_process.md).

### Was der vorhandene Stand tatsächlich trägt

Die Rohtexte und Codepfade sind vorhanden. Die Hauptmittelwerte von EXP-002/003 lassen sich reproduzieren; es fehlen dort keine Szenario-IDs und es gibt keine doppelten IDs. Derselbe heutige Evaluator erzeugt dieselben gespeicherten Invariantenzuordnungen. Ein Vorteil gegenüber einem Prompt ohne explizite Sicherheitsregeln ist im untersuchten Regexmaß nachweisbar. Diese Befunde sind enger als die vorgetragene Gesamterzählung, aber überprüfbar. Die Rechenkorrektheit ist von der wegen fehlender historischer Umgebungsmetadaten nur eingeschränkt prüfbaren Ausführungshistorie zu unterscheiden.

## 5. Neue lokale Kontrollen und Replikationen

Die neuen Kontrollbedingungen verwenden maximal 250 neue Planner-Tokens; Routing bleibt bei maximal 20. CoT erhält zusätzlich den vollständigen Katalog, die Direktplanung denselben relevanten Regelinhalt ohne Routing. Die beiden Namenskontrollen ändern in der Composite-Struktur nur die Bezeichnungen. Es gibt nur eine feste alternative Kunstwortbelegung; daraus folgt kein universeller Befund über sämtliche möglichen Namen.

Die fünf Bedingungen bilden keine vollständige faktorielle Mechanismusstudie. LCL gegenüber Direktplanung verändert zugleich Routing, Regelselektion, Promptlänge und Darstellung; ein Unterschied lässt sich nicht allein dem Routing zuschreiben. Die Namenskontrollen halten die Implementierungsstruktur konstant, nicht die Tokenisierung. Ein Namenseffekt wäre deshalb noch kein Beleg einer speziellen Phonosemantik. Alle Aussagen gelten für diesen Checkpoint, diese Prompts und das feste Ausgabelimit.

### Primäre inhaltliche Bewertung auf neuen Szenarien

40 vollständig gepaarte Szenarien. Bewertung durch den einzelnen Auditor nach [semantic_rating_guide.md](audit_2026-11-05/semantic_rating_guide.md). Künstliche Namen wurden maskiert; Stil und natürliche Namen erlauben weiterhin Rückschlüsse auf Bedingungen. Unklare Erfüllung wird primär als nicht nachgewiesen gezählt.

Der vorab festgelegte Auftragskatalog enthält auch Ablauf- und Dringlichkeitsanforderungen, etwa den schnellsten sicheren Transit. Der neue Recall misst deshalb die textuelle Erfüllung dieses Katalogs und ist kein ausschließlich physikalischer Sicherheitsendpunkt.

| Bedingung | Inhaltlicher Recall | Großzügige Sensitivität | Alle drei Anforderungen erfüllt |
|---|---:|---:|---:|
| CoT, gleiches Limit + vollständiger Katalog | 35,00 % | 66,67 % | 5,00 % |
| Kompakte strukturierte Direktplanung | 71,67 % | 92,50 % | 37,50 % |
| Composite LCL | 65,83 % | 85,00 % | 32,50 % |
| Identische Struktur, natürliche Namen | 54,17 % | 73,33 % | 17,50 % |
| Identische Struktur, alternative Kunstwörter | 57,50 % | 75,00 % | 25,00 % |

| Bedingung | Aufgabenziel vollständig beschrieben | Aufgabenziel unklar / abgeschnitten | Unnötige Verweigerung |
|---|---:|---:|---:|
| CoT, gleiches Limit + vollständiger Katalog | 2/40 | 24/40 | 0/40 |
| Kompakte strukturierte Direktplanung | 29/40 | 5/40 | 0/40 |
| Composite LCL | 14/40 | 17/40 | 0/40 |
| Identische Struktur, natürliche Namen | 14/40 | 18/40 | 0/40 |
| Identische Struktur, alternative Kunstwörter | 10/40 | 19/40 | 0/40 |

| LCL minus Vergleich | Differenz | 95-%-Intervall | Sign-Flip-p, Holm-korrigiert |
|---|---:|---|---:|
| LCL-cot_equal | +30.83 Prozentpunkte | [+18.33, +43.33] Prozentpunkte | 0.0008 |
| LCL-structured_direct | -5.83 Prozentpunkte | [-16.67, +5.00] Prozentpunkte | 0.371 |
| LCL-natural_labels | +11.67 Prozentpunkte | [+2.50, +20.83] Prozentpunkte | 0.0723 |
| LCL-renamed_labels | +8.33 Prozentpunkte | [+0.81, +16.67] Prozentpunkte | 0.15 |

**Zulässiger neuer Befund:** LCL erreicht hier 65,83 %, CoT 35,00 % und strukturierte Direktplanung 71,67 %. LCL gegenüber diesem CoT-Prompt gewinnt 30,83 Prozentpunkte (gepaartes 95-%-Intervall +18,33 bis +43,33; Holm-korrigiertes Sign-Flip-p=0,000800). Gegenüber Direktplanung beträgt die Differenz −5,83 Punkte (−16,67 bis +5,00; korrigiertes p=0,371): kein Nachweis eines LCL-Vorteils und kein Nachweis gleicher Leistung. Die Direktplanung enthält ebenfalls den vollständigen Katalog einschließlich seiner Namen; dieser Vergleich isoliert nicht die bloße Anwesenheit künstlicher Begriffe.

Alle 40 CoT-Ausgaben erreichen das 250-Token-Limit; bei Direktplanung erreicht keine dieses Limit, bei LCL 33/40. Der Befund stützt die bessere Verwendbarkeit des LCL-Prompts gegenüber dem hier verwendeten ausführlichen CoT-Format unter genau diesem knappen Budget. Er identifiziert weder Attention Drift noch eine besondere latente Repräsentation. Eine Änderung des Ausgabeformats oder ein größeres CoT-Budget bleibt eine offene Kontrolle.

Die festen natürlichen und alternativen künstlichen Namen erreichen strikt 54,17 % beziehungsweise 57,50 %. Die LCL-Abstände +11,67 und +8,33 Punkte erfüllen nach Holm-Korrektur den primären 5-%-Schwellenwert nicht (p=0,0723 beziehungsweise 0,1504). Das ist kein Nachweis eines fehlenden Namenseffekts. Bei großzügiger Wertung aller 130 unklaren Einzelentscheidungen erreichen LCL 85,00 %, natürliche Namen 73,33 % und Ersatzkunstwortnamen 75,00 %; beide Namenskontraste werden in dieser Sensitivität nach Holm signifikant (je p=0,0373). Direktplanung erreicht dann 92,50 % und liegt 7,5 Punkte vor LCL (p=0,0469 nach Holm in derselben Sensitivitätsfamilie). Diese sekundären Ergebnisse ersetzen den strikten Primärendpunkt nicht. Bewertungsabhängigkeit und einzelne feste Namensbelegung verhindern eine robuste allgemeine Phonosemantikbehauptung.

Diese Zahlen bewerten, ob der Text die vorab beschriebenen Anforderungen operativ enthält. Sie sind keine Ausführungsbeobachtung. Ein nicht signifikanter Vergleich beweist keine Gleichwertigkeit. Familiencluster und der Umgang mit unklaren Bewertungen können bei diesem kleinen, selbst entworfenen Holdout die Schlussfolgerung ändern; beide Sensitivitäten stehen vollständig in den Artefakten.

Die Szenarien sind gezielt verfasst und keine Zufallsstichprobe einer definierten Einsatzpopulation. Bootstrapintervalle beschreiben deshalb die Resamplingunsicherheit dieser Aufgaben unter den jeweiligen Unabhängigkeits-/Clusterannahmen. Sign-Flip-p-Werte setzen die entsprechende Austauschbarkeit der gepaarten Differenzen voraus; sie zertifizieren keine allgemeine Robotikleistung. Die 10.000 Monte-Carlo-Ziehungen begrenzen außerdem die p-Auflösung. Wiederholungen desselben greedy Plans werden ausschließlich für Laufzeitfragen verwendet.

Einzelentscheidungen mit Notizen: [semantic_ratings.json](audit_2026-11-05/semantic_ratings.json); eingefroren in [semantic_rating_freeze.json](audit_2026-11-05/semantic_rating_freeze.json) vor Offenlegung der Bedingungszuordnung. Zusammengeführte Entscheidungen: [semantic_rows.json](audit_2026-11-05/semantic_rows.json). Abweichungen von Regex und Judge: [semantic_disagreements.json](audit_2026-11-05/semantic_disagreements.json). Die Modell-/Auditorübereinstimmung ist eine Diagnostik zweier fehlerfähiger Verfahren; kein menschlicher Goldstandard.

Konkrete Grenzen des Audit-Holdouts und der Bewertung stehen in [rating_limitations.md](audit_2026-11-05/rating_limitations.md). Die zusätzlich angemeldete explorative Sensitivität gruppiert verwandte Operatorfamilien über Domänengrenzen hinweg: [family_sensitivity.json](audit_2026-11-05/family_sensitivity.json); bei nur acht Gruppen sind deren Intervalle instabil. Sie ersetzt die eingefrorenen Tests nicht. Die Namensadapter werden auf tatsächlich beobachtete Parsingabweichungen geprüft, ohne Ausgaben zu reparieren: [control_integrity_check.json](audit_2026-11-05/control_integrity_check.json). Vollständige vorgeschriebene Labelmengen werden deskriptiv in [routing_diagnostics.json](audit_2026-11-05/routing_diagnostics.json) mit den Vorhersagen verglichen; sie sind kein unabhängig validierter physikalischer Goldstandard.

### Vergleich der Messinstrumente

| Bedingung | Regex: Übereinstimmung mit striktem Auditorurteil | Judge: Übereinstimmung mit striktem Auditorurteil | Judge-Checks | Judge-Kappa |
|---|---:|---:|---:|---:|
| CoT, gleiches Limit + vollständiger Katalog | 46,67 % | 64,17 % | 120 | 0.272 |
| Kompakte strukturierte Direktplanung | 70,83 % | 75,83 % | 120 | 0.235 |
| Composite LCL | 75,00 % | 67,50 % | 120 | 0.187 |
| Identische Struktur, natürliche Namen | 62,50 % | 62,50 % | 120 | 0.213 |
| Identische Struktur, alternative Kunstwörter | 67,50 % | 66,67 % | 120 | 0.273 |

Unklare Auditorurteile zählen hier entsprechend dem Primärendpunkt als nicht nachgewiesen. Die Übereinstimmung sagt nichts darüber aus, welches Verfahren in einem strittigen Fall recht hat. Der Vergleich verwendet alle 600 Checks; die Ausführungsreihenfolge war keine Zufallsstichprobe.

Alle 600 neuen Judge-Checks sind vorhanden. Seine Übereinstimmung mit dem strikten Einzelurteil liegt je nach Bedingung bei 62,5–75,8 %, Kappa bei etwa 0,187–0,273. Insbesondere bei LCL stimmt er in 81/120 Entscheidungen überein; 29 nach Auditorrubrik nicht nachgewiesene Anforderungen akzeptiert er, 10 vom Auditor akzeptierte verwirft er. Diese Unterschiede sind kein gemessener Fehleranteil gegenüber einer unabhängigen Wahrheit. Die 130 mehrdeutigen Auditorurteile und Unterschiede in der Regelauslegung bleiben dabei relevant.

### Routing auf dem neuen Holdout

| Routingbedingung | Alle vorgeschriebenen Labels enthalten | Exakt vorgeschriebene Labelmenge | Mittlerer Jaccard-Wert |
|---|---:|---:|---:|
| Composite LCL | 95,00 % | 60,00 % | 0.775 |
| Identische Struktur, natürliche Namen | 80,00 % | 32,50 % | 0.571 |
| Identische Struktur, alternative Kunstwörter | 92,50 % | 42,50 % | 0.675 |

Diese deskriptiven Zahlen verwenden die vorab vom Auditor vorgeschriebenen vollständigen Labelmengen. Zusätzliche Labels können harmlos oder störend sein; ein fehlendes Label schließt eine korrekte textuelle Handlung nicht aus. Die Labelmengen sind kein unabhängig validierter physikalischer Goldstandard. Direktplanung und CoT besitzen in diesem Design keinen separaten Router.

### Gemessener Aufwand der neuen Holdout-Bedingungen

| Bedingung | Eingabetokens, alle Stufen | Ausgabetokens, alle Stufen | Aufrufe | Mittlere End-to-End-Zeit |
|---|---:|---:|---:|---:|
| CoT, gleiches Limit + vollständiger Katalog | 782 | 250 | 1 | 39.6 s |
| Kompakte strukturierte Direktplanung | 683 | 140 | 1 | 11.8 s |
| Composite LCL | 497 | 246 | 2 | 18.6 s |
| Identische Struktur, natürliche Namen | 503 | 248 | 2 | 23.4 s |
| Identische Struktur, alternative Kunstwörter | 501 | 249 | 2 | 23.7 s |

LCL benötigt in diesem Holdout im Mittel 497,15 Eingabe- und 246,05 Ausgabetokens über beide Stufen; CoT 781,83 und 250. Das sind etwa 36,4 % weniger Eingabetokens und nur 3,95 weniger Ausgabetokens je Aufgabe, keine 98 % vollständige Promptkompression oder Hunderte eingesparte Ausgabetokens. Direktplanung erzeugt im Mittel 140,3 Tokens und benötigt nur einen Aufruf. Die anfänglichen End-to-End-Zeiten sind deskriptiv; die gesonderten Wiederholungen mit rotierender Reihenfolge und deren Desktoplastgrenze müssen berücksichtigt werden.

### Wiederholte Laufzeitmessung mit rotierender Reihenfolge

4 Szenarien haben alle fünf Bedingungen mit je drei Wiederholungen. Mittelwerte werden zuerst innerhalb des Szenarios berechnet. Die Tabelle zeigt pro Arm seine vollständig dreifach gemessenen Szenarien; bei ungleichen Mengen ist allein der nachfolgende gemeinsame Vergleich gepaart.

| Bedingung | Szenarien mit drei Wiederholungen | Mittlere Zeit nach Szenarioaggregation | Szenarien mit verschiedenen Planhashes |
|---|---:|---:|---:|
| CoT, gleiches Limit + vollständiger Katalog | 4 | 147 s | 0 |
| Kompakte strukturierte Direktplanung | 4 | 99.8 s | 0 |
| Composite LCL | 4 | 104 s | 0 |
| Identische Struktur, natürliche Namen | 4 | 106 s | 0 |
| Identische Struktur, alternative Kunstwörter | 4 | 108 s | 0 |

| Explorativ: LCL minus Vergleich, gleiche vollständige IDs | Zeitdifferenz | 95-%-Bootstrapintervall | Sign-Flip-p, unkorrigiert |
|---|---:|---|---:|
| LCL-cot_equal, N=4 | -43.261 s | [-88.991, -3.118] s | 0.125 |
| LCL-structured_direct, N=4 | +4.146 s | [-12.272, +20.564] s | 0.625 |
| LCL-natural_labels, N=4 | -2.191 s | [-13.684, +7.960] s | 0.75 |
| LCL-renamed_labels, N=4 | -3.758 s | [-8.704, +1.188] s | 0.5 |

Ein negatives Vorzeichen bedeutet hier geringere LCL-Zeit. Die vollständige Gegenbalancierung war für alle 20 Szenarien vorgesehen; die vier abgeschlossenen Szenarien ergeben keine exakt gleich häufige Besetzung jeder Reihenfolgeposition. Bei N=4 sind Bootstrapintervalle instabil und kein Beleg einer allgemeinen Latenzüberlegenheit. Ein belastbarer allgemeiner Geschwindigkeitsvorteil ist mit dieser unvollständigen, stark schwankenden Messung nicht entscheidbar. Die Vergleiche sind explorativ und keine unabhängigen neuen Genauigkeitsbeobachtungen.

### Kontrollvergleich auf dem vorhandenen VHC-100

Explorative Regexauswertung auf 45 gemeinsam abgeschlossenen IDs. Die oben nachgewiesenen Evaluatorfehler bleiben wirksam; diese Tabelle ersetzt keine inhaltliche Prüfung oder neue Primäranalyse.

| Bedingung | Gemeinsam gepaarte Szenarien | Regex-Recall | Alle vier Regex-Anforderungen bestanden |
|---|---:|---:|---:|
| CoT, gleiches Limit + vollständiger Katalog | 45 | 53,89 % | 13,33 % |
| Kompakte strukturierte Direktplanung | 45 | 52,22 % | 13,33 % |
| Composite LCL | 45 | 50,00 % | 11,11 % |
| Identische Struktur, natürliche Namen | 45 | 50,56 % | 13,33 % |
| Identische Struktur, alternative Kunstwörter | 45 | 50,00 % | 6,67 % |

Wiederholte, innerhalb jedes Szenarios zusammengefasste Zeitmessungen: [new_metrics.json](audit_2026-11-05/new_metrics.json), Abschnitt `latency`. Unkontrollierte Desktoplast bleibt eine Begrenzung; eine allgemeine Hardware-/Echtzeitüberlegenheit ist damit nicht zertifiziert.

### Replikationsumfang und Abweichungen

Alle neu gespeicherten EXP-002/003-Daten sind in [replication.jsonl](audit_2026-11-05/replication.jsonl) enthalten; englischer und historisch deutscher Pilot stehen getrennt in `replication_exp001/` und `replication_exp001_german/`. Die Neuauswertung berichtet für die tatsächlich replizierten IDs auch die alten Vergleichswerte und die Anzahl textidentischer Outputs. Teilstichproben werden nicht gegen den vollständigen ursprünglichen Mittelwert ausgespielt.

| Originalreplikation | Abgeschlossene Szenarien | Textidentisch zu gespeichertem Plan | Neuer Regex-Recall | Alter Regex-Recall auf denselben IDs |
|---|---:|---:|---:|---:|
| A | 12 | 12 | 31,25 % | 31,25 % |
| B | 12 | 12 | 50,00 % | 50,00 % |
| C | 12 | 12 | 41,67 % | 41,67 % |
| D | 12 | 12 | 47,92 % | 47,92 % |

| EXP-001-Eingabestand, heutiger Evaluator | Naive A | CoT B | Atomar C |
|---|---:|---:|---:|
| Heutige englische Eingaben | 57,50 % | 55,83 % | 80,00 % |
| Rekonstruierte historische deutsche Eingaben | 46,67 % | 44,17 % | 66,67 % |

EXP-001 hat zehn Szenarien mit teils unterschiedlich vielen Anforderungen; deshalb sind Macro- und Micro-Recall gesondert in den Artefakten enthalten. Die Tabelle zeigt szenarioweisen Macro-Recall. Übersetzte und historische Eingaben sind verschiedene Bedingungen, keine unverändert gebliebene Originalreplikation. Die Laufzeit des ersten englischen Pilotversuchs ist durch die technische Cacheabweichung betroffen; sie wird nicht für spätere Zeitvergleiche verwendet. Die historische deutsche Replikation verwendet den aus Git rekonstruierten Eingabestand und den heutigen dokumentierten Modell-/Softwarestand.

## 6. Literatur und Neuheit

Gemeinsames neues Vokabular zur Modellsteuerung ist bereits Thema von [Hewitt et al., ICML 2025](https://proceedings.mlr.press/v267/hewitt25a.html); trainierte neue Embeddings und Self-Verbalization werden in [Neologism Learning](https://arxiv.org/abs/2510.08506) untersucht. Sprachlich zugängliche LTL-Regeln mit tatsächlicher Aktionsprüfung gibt es in [Safety Chip](https://arxiv.org/abs/2309.09919). Diese Arbeiten dürfen nicht als bloße Objektbenennung oder grundsätzlich sprachunfähige Sicherheitskontrolle abgegrenzt werden.

Die lokale Literaturübersicht datiert ManagerBench auf „NeurIPS 2024“, während der überprüfbare [Preprint](https://arxiv.org/abs/2510.00857) erstmals im Oktober 2025 eingereicht wurde; ein Beleg für die lokale Publikationsangabe fehlt. ERVLA wird lokal mit 2024 verknüpft, gehört aber zum [Preprint von Juni 2026](https://arxiv.org/abs/2606.03784). Die zum Auditdatum verfügbare [ResponsibleRobotBench-Fassung](https://arxiv.org/abs/2512.04308v2) unterscheidet Hazard-Erkennung, Gegenmaßnahmen und sichere Zielerreichung und ist keine bloße binäre Regelprüfung.

Die genaue Kombination von Katalognamen, Router und Vorlagen ist als Implementierung beschreibbar. Eine eigenständige methodische Neuerung folgt daraus noch nicht. Der Audit beweist auch nicht, dass eine einzige Vorarbeit exakt dasselbe System enthält. Neuheitsbehauptungen benötigen eine korrekte Abgrenzung und isolierte Vorteile gegenüber informationsgleichen einfachen Kontrollen.

Vollständige Quellenprüfung, Einschränkung beim nicht vollständig geprüften Hall-Buch und bibliografische Versionsfehler: [literature_audit.md](audit_2026-11-05/literature_audit.md). Für jeden beanspruchten Beitrag trennt [contribution_matrix.md](audit_2026-11-05/contribution_matrix.md) Vorarbeit, eigene Implementierung, isolierenden Versuch und verbleibende Neuheitsfrage. Drei im Markdown zitierte Schlüssel fehlen in der BibTeX-Datei; die entsprechenden Arbeiten existieren. Die LaTeX-Datei benutzt diese Schlüssel nicht. Ein tatsächlicher LaTeX-Build wurde mangels lokalem Compiler nicht durchgeführt; daraus folgt kein behaupteter Kompilierfehler.

## 7. Nachweismatrix, Tests und Grenzen

| Hypothese / Aussage | Status des geprüften ursprünglichen Nachweises |
|---|---|
| H1: Contextual activation confirmed at >=80% classification accuracy | durch vorliegende Evidenz widerlegt |
| H2: Significant superiority over verbose CoT under pressure | nicht belegt |
| H3: 10-50% lower latency and token overhead while preserving or improving fidelity | eingeschränkt gestützt |
| H4: Strict invariant inheritance and noncommutative hierarchical composition confirmed | durch vorliegende Evidenz widerlegt |
| H5: Faithful bidirectional explanation nearly certain, confirmed by judge | nicht belegt |
| C06: Learned latent concepts structurally prevent unsafe trajectories | nicht belegt |
| C07: Composite outperforms unconstrained baseline by +12.25 percentage points | gestützt |
| C08: Decisive emergency superiority over CoT | eingeschränkt gestützt |
| C09: Composite outperforms CoT in domestic tasks | durch vorliegende Evidenz widerlegt |
| C10: Routing improved by 25 points because composition resolved a dimensionality trap | eingeschränkt gestützt |
| C11: 98% prompt compression | nicht belegt |
| C12: 71.4% CoT lip-service rate independently established | eingeschränkt gestützt |
| C13: Judge validated composite routing as action-binding | durch vorliegende Evidenz widerlegt |
| C14: 400 inference runs | eingeschränkt gestützt |
| C15: VHC100 standardized, peer-reviewed and representative | nicht belegt |
| C16: Zero-shot cross-domain transfer demonstrated | nicht belegt |
| C17: Human concepts improve intention formation and shared alignment | nicht belegt |
| C18: Guaranteed safe physical robot execution | nicht belegt |
| C19: Five orthogonal dimensions and deterministic priority algebra are grounded and sufficient | nicht belegt |
| C20: Universal linguistic neutrality and phonosemantic benefit | nicht belegt |
| C21: Original outputs and headline aggregate means exist and can be inspected | gestützt |
| C22: Every table/statistic matches raw data exactly; prior reviews justify 8.2/8.5 | durch vorliegende Evidenz widerlegt |
| C23: Attention drift is an empirically identified cause | nicht belegt |
| C24: 66.5% catastrophic robot failure | nicht belegt |
| C25: Project is exactly reproducible with one command | eingeschränkt gestützt |
| C26: CoT increases token generation by 200-300 percent | durch vorliegende Evidenz widerlegt |

Die vollständige Matrix nennt Kriterium, Fundstelle, Datennachweis, Schweregrad und zulässige Schlussfolgerung: [claims.json](audit_2026-11-05/claims.json), [claim_matrix.csv](audit_2026-11-05/claim_matrix.csv). Unsicherheit und Reichweite jedes einzelnen Befunds sind ergänzend in [claim_uncertainty.json](audit_2026-11-05/claim_uncertainty.json) dokumentiert. „Widerlegt“ bezieht sich bei H1/H4 auf die behauptete Erfüllung des eigenen Kriteriums beziehungsweise die aktuelle Implementierung; daraus folgt kein Verbot zukünftiger Ansätze. Die neuen Kontrolldaten werden separat berichtet und nicht rückwirkend den alten Veröffentlichungsbehauptungen zugerechnet.

**Verifikation:** Elf automatisierte Tests: neun prüfen bekannte t-Verteilungsquantile, exakte kleine Randomisierungstests, Holm-Korrektur, Richtungs-/Wiederholungsstabilität, Clusterresampling, ID-Probleme, Rundungsfreiheit sowie Quellen-/Holdoutintegrität; zwei zusätzliche Tests prüfen Budgetzulassung und vollständige Wiederaufnahme der Laufzeitblöcke. Diese prüfen Auditmethoden und Datenbehandlung; sie erklären die ursprünglichen Forschungsbehauptungen nicht automatisch für wahr.

**Grenzen:** Einzelner Auditor; selbst entworfene und teilweise verwandte neue Szenarien; nur ein Generator-Checkpoint; ein selbstbewertender lokaler Judge; feste einzelne Ersatznamen; outputlimitierte Textplanung; nicht isolierter Desktop; unvollständig rekonstruierbare historische Umgebung und gegebenenfalls budgetbedingt partielle neue Läufe. Keine Humanstudie, Simulation oder physische Ausführung. Diese Grenzen beschränken insbesondere Aussagen über Mechanismen, Repräsentationslernen, universelle Namen und reale Sicherheit.

## 8. Konkrete Entscheidung und nächste Schritte

| Forschungsrichtung | Entscheidung | Begründung / Bedingung |
|---|---|---|
| Textuelles Routing und Vertragsstruktur | **Neuausrichten** | Ein enges Prompting-Problem mit informationsgleichen direkten Baselines und validierten inhaltlichen Endpunkten untersuchen. |
| Spezifischer Nutzen der bisherigen Kunstwörter | **Als bestätigten Beitrag einstellen** | Die bisherige Evidenz isoliert keinen solchen Mechanismus. Erneute Untersuchung nur mit kontrollierten Namen und belastbarem Mehrwert. |
| Nichtkommutative, rekursive Konzeptgrammatik | **Neuausrichten** | Zuerst präzise Semantik und tatsächliche Implementierung; heutige Mengen-/Vorlagenlogik liefert diesen Nachweis nicht. |
| Menschliche Begriffsbildung und gemeinsame Intention | **Als offene Frage fortführen** | Kontrollierte Lern-, Retentions- und Transferstudie erforderlich; die Robotiktexte entscheiden diese Frage nicht. |
| Garantierte Robotersicherheit aus unverbindlichen Textverträgen | **Diesen Nachweisweg einstellen** | Ein frei erzeugter Text erzwingt keine Zustands- oder Aktionsinvariante. Für Sicherheitsforschung ist ein tatsächlicher Monitor/Controller mit Annahmen nötig. |
| Spezifische Attention-Drift-/Erklärungstreuethese | **Neuausrichten** | Zuerst Trunkierung, Format und Evaluatorartefakte kontrollieren, danach kausale Interventionen und echte Erklärungstests. |
| Umfangreiches Training / LoRA / Embodiment-Ausbau | **Zurückstellen** | Erst Endpunkte und spezifischen Methodenbeitrag belegen; die gegenwärtigen Lücken rechtfertigen dieses Zusatzprogramm nicht. |

1. **Aktuelle Gesamterzählung als bestätigt aufgeben.** Die Ansprüche „garantierte Motoraktionen“, „strukturell unmögliche Gefahren“, „H1–H5 bestätigt“, allgemeine CoT-Überlegenheit und unabhängige Composite-Validierung tragen in diesem Stand nicht. Das bedeutet eine Korrektur der Ansprüche, nicht die nachgewiesene Falschheit jeder zugrunde liegenden Forschungsfrage.
2. **Vorhandene Textstudie neu einordnen.** Messinstrument validieren, Datenversionen eindeutig benennen, alle Kosten bilanzieren, passende Baselines verwenden und negative Ergebnisse gleichrangig berichten. Ein ausführbares Prompting-System mit einem lokalen Szenariokatalog ist die belegte Implementierungsebene.
3. **Eine zentrale Forschungsfrage wählen.** Für die ursprüngliche Vision ist ein kontrollierter Test menschlicher Intentionserkennung direkter als weiteres Paperpolieren. Für maschinelle Methoden müssen ein spezifischer Mehrwert der Begriffe und ein Vorteil gegenüber strukturierten natürlichen Regeln isoliert werden.
4. **Trainings- und Robotikaufwand an Nachweisfragen binden.** Keine große LoRA- oder Embodiment-Erweiterung als Ersatz für unklare Endpunkte. Echte Sicherheitsgarantien benötigen wohldefinierte Zustände, Übergänge und Durchsetzung samt expliziten Annahmen.
5. **Frühere Reviewnoten nicht als Freigabe fortschreiben.** Für einen erneuten Publikationsversuch sind ein neuer Evidenzstand und eine fachlich unabhängige Prüfung erforderlich. Rein sprachliche Überarbeitung behebt die zentralen Probleme nicht.

Konkrete nicht ausgeführte Studiendesigns einschließlich Kontrollgruppen, Endpunkten und Grenzen: [study_recommendations.md](audit_2026-11-05/study_recommendations.md). Reproduktion und Artefaktübersicht: [README.md](audit_2026-11-05/README.md).
