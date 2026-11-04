# Forschungslandkarte (Research Map)

Diese Forschungslandkarte beschreibt die Phasen, Abhängigkeiten und Meilensteine des Projekts **Lingual Composite Learning**.

```mermaid
flowchart TD
    subgraph Phase0["Phase 0: Fundierung & Abgleich"]
        P0_Lit["Literaturrecherche & Abgrenzung<br/>(Hewitt, Lupyan, Yang)"]
        P0_Tax["Taxonomie & Kriterienkatalog<br/>(Wann eignet sich ein Begriff?)"]
    end

    subgraph Phase1["Phase 1: Begriffsmodellierung"]
        P1_Fufu["Spezifikation Pilotbegriff 'fufu'<br/>(Präbedingungen, Invarianten, Abbruch)"]
        P1_Scen["Entwicklung Test-Szenarien<br/>(Tür, Vase, Transport)"]
    end

    subgraph Phase2["Phase 2: Maschinelle In-Context Baselines"]
        P2_LLM["LLM In-Context Evaluation<br/>(Freitext vs. Umschreibung vs. Neologismus)"]
        P2_Comp["Kompositions-Tests<br/>(Mehrere Begriffe gleichzeitig)"]
    end

    subgraph Phase3["Phase 3: Repräsentationslernen"]
        P3_Embed["Neologism Embedding Tuning<br/>(Soft Prompt / New Token Embedding)"]
        P3_Transfer["Zero-Shot Domain Transfer<br/>(Neue Domänen ohne Nachtraining)"]
    end

    subgraph Phase4["Phase 4: Kognition & Menschliche Absichtsbildung"]
        P4_Study["Probanden-Experimente<br/>(Erinnerung, Vollständigkeit der Absicht)"]
        P4_Form["Formulierungsaufwand & Effizienz"]
    end

    subgraph Phase5["Phase 5: Embodiment & Safety Verification"]
        P5_Logic["Überführung in temporale Logik / Constraints<br/>(Safety-Chip / LTL)"]
        P5_Sim["Simulations- & Robotik-Validierung<br/>(Verhinderung von Kollision/Schaden)"]
    end

    Phase0 --> Phase1
    Phase1 --> Phase2
    Phase1 --> Phase4
    Phase2 --> Phase3
    Phase3 --> Phase5
    Phase2 --> Phase5
    Phase4 --> Phase5
```

---

## 📅 Phasenübersicht & Meilensteine

### Phase 0: Fundierung, Taxonomie & Abgrenzung (Aktuell)
- **Ziel:** Saubere Trennung von bereits publizierten Ansätzen und eigener Forschungslücke.
- **Kernfragen:**
  - Welche Aspekte sind durch *Hewitt et al. (2025/2026)* und *Yang et al. (2024)* bereits abgedeckt?
  - Was ist der spezifische Mehrwert der Kombination aus **menschlicher Absichtsbildung + maschinellem Transfer + Sicherheitsverifikation**?
- **Ergebnis:** Strukturierte Literaturberichte in [`literature/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/literature).

### Phase 1: Begriffsmodellierung & Szenariendesign
- **Ziel:** Formalisierung von Begriffen in beobachtbare Bedingungen und Handlungsregeln.
- **Arbeitspakete:**
  - Pilot-Spezifikation für `fufu` ([`concepts/fufu.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/fufu.md)).
  - Erstellung von Benchmark-Szenarien in [`data/scenarios/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data/scenarios) (z. B. Türöffnung mit Person dahinter, Transport von zerbrechlichen Objekten).
  - Definition von Negativ- und Grenzfällen (Wann muss zwingend gestoppt werden?).

### Phase 2: Maschinelle In-Context-Baselines
- **Ziel:** Messung, wie heutige SOTA-LLMs auf definierte Neologismen reagieren, wenn die Definition im Prompt / System-Prompt bereitgestellt wird.
- **Vergleichsgruppen:**
  1. Reine Basis-Anweisung („Öffne die Tür.“)
  2. Ausführliche Umschreibung („Öffne die Tür vorsichtig, achte auf Personen...“)
  3. Begriffliche Anweisung mit hinterlegter Definition („Öffne die Tür, fufu.“ + System-Definition von fufu)
- **Metriken:** Vollständigkeit der Handlungsplanung, Reaktionszeit bei Störungen, Erkennung von Abbruchbedingungen.

### Phase 3: Neologism Learning & Repräsentationslernen
- **Ziel:** Untersuchung von echtem Begriffslernen im Modell (ohne lange System-Prompts).
- **Ansatz:** Training neuer Token-Embeddings (wie Hewitt et al. 2026) oder PEFT/LoRA-Adapter.
- **Ergebnis:** Bewertung, ob trainierte Repräsentationen robuster generalisieren als In-Context-Prompts.

### Phase 4: Kognition & Menschliche Absichtsbildung
- **Ziel:** Empirische Überprüfung des psycholinguistischen Effekts (angelehnt an Lupyan et al. 2007).
- **Test:** Führt das Vorhandensein eines Begriffs dazu, dass Testpersonen in komplexen Situationsbeschreibungen signifikant seltener sicherheitsrelevante Einschränkungen vergessen?

### Phase 5: Embodiment, Robotics & Safety Verification
- **Ziel:** Physische/simulative Verifikation (in Habitat, Isaac Sim oder PyBullet).
- **Integration:** Übersetzung des Begriffs in formale Guardrails / Safety-Chips (Yang et al. 2024).
