---
name: lingual-composit-research
description: Leitfaden und Workflows für autonome Forschung im Projekt Lingual Composite Learning (erweiterbare Begriffssprache für Mensch, KI und Roboter).
---

# Skill: Lingual Composite Research

Dieser Skill leitet KI-Agenten und Forschende an, strukturierte, wissenschaftlich belastbare Forschung im Projekt **Lingual Composite Learning** durchzuführen.

## Kernprinzipien

1. **Evidenzbasierte Aussagen:** Behauptungen dürfen erst dann als verifiziert gelten, wenn reproduzierbare experimentelle Daten vorliegen.
2. **Begriffs-Präzision:** Neue Begriffe (z. B. `fufu`) müssen formal aufgeschlüsselt werden (Bedingungsbündel, Vor-/Nachbedingungen, Invarianten).
3. **Dokumenten-Integrität:** Jeder Arbeitsschritt aktualisiert die zentralen Tracker (`STATE.md`, `HYPOTHESES.md`, `BACKLOG.md`).

## Standard-Workflows

### 1. Neuen Begriff anlegen
- Datei erstellen unter `dev/concepts/<begriff>.md` basierend auf `dev/templates/concept_template.md`.
- Definition in atomare semantische Bedingungen zerlegen.
- Mindestens 2 Transfer-Domänen spezifizieren.
- Offene Operationalisierungsfragen und Abbruchbedingungen definieren.

### 2. Experiment aufsetzen
- Eindeutigen Ordner anlegen: `dev/experiments/EXP-<Nummer>_<name>/`.
- `README.md` aus `dev/templates/experiment_template.md` erstellen.
- Zu untersuchende Hypothese aus `dev/HYPOTHESES.md` verlinken.
- Nach Abschluss: `protocol.md` und `results.md` schreiben und Status in `dev/HYPOTHESES.md` sowie `dev/STATE.md` aktualisieren.

### 3. Literatur analysieren
- Neue Quelle in `dev/literature/<autor>_<jahr>_<kurztitel>.md` nach `dev/templates/literature_note_template.md` exzerpieren.
- Spezifisch die Differenzierung zu unserem Forschungsbeitrag (Forschungslücke) herausarbeiten.
