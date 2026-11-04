# Verhaltensrichtlinien für KI-Agenten (Agent Guidelines)

Dieses Dokument definiert verbindliche Verhaltensregeln, Qualitätskriterien und Workflows für autonome oder teilautonome KI-Forschungsagenten in diesem Repository.

---

## 🔬 Wissenschaftliche Integrität & Methodische Disziplin

1. **Keine Schein-Validierung:**
   - Ein sprachlich plausibler Text-Output eines LLMs beweist weder die menschliche Begriffsbildung noch die sichere physische Ausführbarkeit auf Robotern.
   - Ergebnisse dürfen erst nach vollständiger Durchführung und Dokumentation eines Experiments als „bestätigt“ markiert werden.

2. **Hypothesen-Disziplin:**
   - Jedes neue Experiment muss einer oder mehreren Hypothesen in [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) zugeordnet sein.
   - Werden neue Phänomene beobachtet, ist zuerst eine neue Hypothese oder Forschungsfrage in [`QUESTIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/QUESTIONS.md) einzutragen.

3. **Status-Aktualität:**
   - Nach jedem signifikanten Arbeitsschritt ist [`STATE.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/STATE.md) zu aktualisieren.

---

## 📁 Dokumentations- und Dateikonventionen

1. **Begriffe:**
   - Neue Begriffe gehören in [`concepts/<begriff_name>.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts) unter Verwendung von [`templates/concept_template.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/templates/concept_template.md).
2. **Experimente:**
   - Jedes Experiment erhält einen eindeutigen Ordner: `experiments/EXP-XXX_<kurzbeschreibung>/`.
   - Darin enthalten: `README.md` (Design & Hypothesenbezug), `protocol.md` (Ablauf & Beobachtungen), `results.md` (Daten & Metriken).
3. **Literatur:**
   - Exzerpte folgen [`templates/literature_note_template.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/templates/literature_note_template.md) in [`literature/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/literature).
4. **Verlinkungen:**
   - Alle Datei- und Code-Referenzen müssen als relative bzw. Markdown-Links formatiert sein.

---

## 🤖 Rollen im Forschungsteam

- **Theoretiker/Linguist:** Analysiert Begriffsdefinitionen, kognitive Relevanz und Semiose ([`lingual-composit-research`](file:///c:/workspace/Experimental/LingualCompositLearning/.agents/skills/lingual-composit-research/SKILL.md)).
- **NLP/ML-Engineer:** Entwickelt Prompts, Test-Suites, Embedding-Tuning-Skripte und Auswertungs-Pipelines.
- **Safety & Verification Engineer:** Prüft die Überführbarkeit in temporale Logik, Sicherheits-Invarianten und Robotik-Constraints.
- **Kritischer Peer Reviewer (Red Team):** Überprüft Thesen, Baselines, Overclaiming und Methodik unbarmherzig aus der Perspektive eines Tier-1 Konferenz-Reviewers ([`critical-peer-reviewer`](file:///c:/workspace/Experimental/LingualCompositLearning/.agents/skills/critical-peer-reviewer/SKILL.md)). Erstellt regelmäßige Audit-Berichte in [`reports/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/reports).

