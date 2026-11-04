# Lingual Composite Learning: Erweiterbare Begriffssprache für Mensch, KI und Roboter

> **Forschungsinitiative** zur Untersuchung einer gemeinsamen Begriffssprache (z. B. Kunstwörter / Neologismen wie „fufu“), die als präzise Verhaltensspezifikation dient, die menschliche Absichtsbildung schärft und maschinelles Handeln absichert.

---

## 🎯 Kernvision & Leitidee

Natürliche Sprache ist oft mehrdeutig oder erfordert wiederkehrende, langatmige Umschreibungen, um Verhaltensnuancen, Sicherheitsanforderungen und Kontextbedingungen abzubilden. Wer eine Unterscheidung nicht im aktiven Begriffsrepertoire hat, vergisst sie oft bereits bei der **Absichtsbildung** (vor dem Formulieren eines Prompts).

Dieses Forschungsprojekt untersucht:
1. **Menschlicher Nutzen:** Hilft das Erlernen definierter Begriffe (Neologismen/Symbole), Bedingungen zuverlässiger zu erinnern und präziser zu formulieren?
2. **Maschineller Nutzen:** Können KI- und Robotersysteme diese Begriffe erlernen (in-context oder per Repräsentationslernen/Embedding-Tuning) und zuverlässig auf neue Aufgaben übertragen?
3. **Kompositionalität & Verifikation:** Lassen sich Begriffe kombinieren und ihre Einhaltung formal prüfen (z. B. temporale Logik, Safety Constraints)?

Referenzdokument: [`ref/Briefing_Begriffssprache_Mensch_KI.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/ref/Briefing_Begriffssprache_Mensch_KI.md).

---

## 🧭 Repository-Navigation

| Verzeichnis / Datei | Zweck & Inhalt |
| :--- | :--- |
| [`STATE.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/STATE.md) | **Single Source of Truth** für aktuellen Projektfortschritt, Phase und nächste Schritte. |
| [`RESEARCH_MAP.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/RESEARCH_MAP.md) | Phasenplan und Forschungslandkarte von Theorie bis Robotik-Transfer. |
| [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) | Strukturierte Hypothesen (H1–H5), Prüfkriterien und Evidenzstatus. |
| [`QUESTIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/QUESTIONS.md) | Offene Leit- und Forschungsfragen. |
| [`DECISIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/DECISIONS.md) | Architectural & Methodological Decision Records (MDRs/ADRs). |
| [`BACKLOG.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/BACKLOG.md) | Aufgaben, To-Dos und anstehende Meilensteine. |
| [`IDEAS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/IDEAS.md) | Rohe Ideen, Erweiterungsansätze und Notizen. |
| [`AGENTS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/AGENTS.md) | Richtlinien für autonome KI-Forschungsagenten. |
| [`concepts/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts) | Katalog formaler Begriffsspezifikationen (z. B. [`concepts/fufu.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/fufu.md)). |
| [`data/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data) | Test-Szenarien, Prompt-Sammlungen, Benchmarks und Probandenstudien-Materialien. |
| [`experiments/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/experiments) | Experiment-Designs, Protokolle und Versuchsanordnungen. |
| [`findings/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/findings) | Konsolidierte, verifizierte Forschungsergebnisse. |
| [`literature/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/literature) | Exzerpte, Literaturanalysen und Paper-Reviews. |
| [`papers/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/papers) | Publikationsmanuskripte, Abstracts und Veröffentlichungsentwürfe. |
| [`ref/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/ref) | Originalbriefings, externe Referenzen und historische Dokumente. |
| [`reports/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/reports) | Periodische Forschungsberichte und Meilenstein-Zusammenfassungen. |
| [`runs/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/runs) | Rohe Test- und Modell-Ausgaben, Prompt-Logs und Evaluierungsdaten. |
| [`src/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/src) | Wiederverwendbarer Programmcode (Python-Module, Tools, Evaluatoren). |
| [`templates/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/templates) | Standardisierte Vorlagen für Experimente, Konzepte, Hypothesen und Literatur. |
| [`visualizations/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/visualizations) | Diagramme, Charts, Ablaufvisualisierungen. |

---

## ⚡ Schnellstart für Forschende & Agenten

1. Konsultiere [`STATE.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/STATE.md) für den aktiven Fokus.
2. Lies die Richtlinien in [`AGENTS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/AGENTS.md).
3. Beachte die Methodik: Vor jeder Behauptung muss eine Hypothese in [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) referenziert und durch ein Experiment in [`experiments/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/experiments) gestützt werden.
