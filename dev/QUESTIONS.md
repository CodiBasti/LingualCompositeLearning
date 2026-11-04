# Offene Forschungs- und Leitfragen

Dieses Dokument erfasst die forschungsleitenden Fragen des Projekts. Jede Frage ist einer Kategorie zugeordnet und dient als Orientierung für experimentelle Designs.

---

## 1. Menschlicher Kognitionseffekt
- **Q1.1:** Verbessert das Vorhandensein eines Begriffs wie `fufu` tatsächlich die menschliche Fähigkeit, relevante Bedingungen *von selbst* zu erkennen (Absichtsbildung), oder verkürzt er lediglich bereits bewusst gewordene Anweisungen?
- **Q1.2:** Wie hoch ist der kognitive Lernaufwand für Menschen, sich ein solches erweitertes Vokabular anzueignen?
- **Q1.3:** Wie stabil bleibt das Begriffsverständnis über die Zeit (Retention)?

---

## 2. Maschineller Effekt & Modellarchitektur
- **Q2.1:** Genügt eine einfache In-Context-Definition (z. B. im System-Prompt), oder bietet ein echtes Representation-Tuning (Neologism-Embedding, Soft-Prompting, LoRA) messbare Vorteile bei der Generalisierung?
- **Q2.2:** Neigen Modelle bei In-Context-Definitionen zu „Attention Drift“ bei langen Kontexten, während trainierte Embeddings robuster aktiviert werden?
- **Q2.3:** Kann das Modell auf Nachfrage verständlich und präzise verbalisieren, welche konkreten Schritte es aufgrund des Begriffs in einer spezifischen Situation ausführt (Self-Verbalization)?

---

## 3. Begriffsgestaltung & Semiose
- **Q3.1:** Welche Token-Repräsentationen eignen sich am besten?
  - *Fantasiewörter / Neologismen* (z. B. `fufu`): Vermeiden semantische Kollisionen mit bestehenden Bedeutungen.
  - *Transparente Komposita* (z. B. `Vorsicht-Stop`): Für Menschen intuitiver, bergen aber Vorurteile im LLM-Vorwissen.
  - *Spezielle Symbole / Tokens* (z. B. `[SAFETY_MAX]`): Eindeutig, aber unnatürlich im Sprechfluss.
- **Q3.2:** Wie granular sollten Begriffe sein? (Monolithische Bündel vs. atomare Bausteine).

---

## 4. Grenzen, Konflikte & Scheinverständnis
- **Q4.1:** Wann wird ein Begriff zu abstrakt oder überladen, sodass das Modell unvorhersehbare Halluzinationen oder übermäßige Passivität (ständiger Handlungsabbruch) zeigt?
- **Q4.2:** Wie reagiert das System auf semantische Widersprüche (z. B. `fufu` [maximale Vorsicht/Verzicht bei Gefahr] kombiniert mit `schnell` oder einer ungeduldigen Nutzeraufforderung)?
- **Q4.3:** Wie erkennen Mensch und System, wenn ihr jeweiliges Verständnis des Begriffs divergiert (Alignment-Drift)?

---

## 5. Prüfbarkeit & Formale Verifikation
- **Q5.1:** Welche Bestandteile eines Handlungsbegriffs lassen sich exakt in mathematische bzw. temporale Logik (z. B. LTL - Linear Temporal Logic) übersetzen?
- **Q5.2:** Wie geht das System mit unvollständiger Sensorik und Unsicherheit um? (Eine Definition von Vorsicht garantiert keine omnisciente Wahrnehmung).
- **Q5.3:** Lässt sich ein Begriff wie `fufu` als modulares Software-Plugin / Safety-Monitor (z. B. Safety Chip) implementieren, das als Schiedsrichter zwischen LLM-Planer und Roboter-Controller agiert?
