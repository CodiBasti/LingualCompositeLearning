# Entscheidungsdokumentation (Methodological & Architectural Decisions)

Dieses Dokument erfasst wegweisende methodische und architektonische Entscheidungen (MDR/ADR) des Forschungsprojekts.

---

## Übersicht

| ID | Datum | Titel | Status |
| :--- | :--- | :--- | :--- |
| **MDR-001** | 31.10.2026 | Trennung von In-Context-Definitionen und Repräsentationslernen | Akzeptiert |
| **MDR-002** | 31.10.2026 | Etablierung von „fufu“ als primäres Pilot-Konzept | Akzeptiert |
| **MDR-003** | 31.10.2026 | Strikte Trennung von theoretischem Nutzen und empirischem Nachweis | Akzeptiert |
| **MDR-004** | 31.10.2026 | Dreistufiger Evaluierungsansatz (Text-Planung -> Simulation -> HRI) | Akzeptiert |
| **MDR-005** | 31.10.2026 | Whorfian Alignment: Strukturelle Unkonstruierbarkeit gefährlicher Zustände | Akzeptiert |
| **MDR-006** | 01.11.2026 | Cross-Domain Vulnerability Transfer als Leitparadigma des Begriffssystems | Akzeptiert |

---

## MDR-001: Trennung von In-Context-Definitionen und Repräsentationslernen

- **Kontext:** Es gibt zwei grundlegende technische Wege, einer KI einen neuen Begriff beizubringen:
  1. *In-Context:* Definition im System-Prompt oder Kontextfenster.
  2. *Representation Learning / Neologism Learning:* Training neuer Token-Embeddings (z. B. Hewitt et al. 2026) oder LoRA-Adapter.
- **Entscheidung:** Beide Wege werden in getrennten Forschungsphasen untersucht. Zuerst wird eine reine In-Context-Baseline etabliert (schnell, modellagnostisch), gefolgt von gezieltem Neologism-Embedding-Tuning (robust, token-sparend).
- **Konsequenzen:** Klare Vergleichbarkeit; es wird verhindert, dass In-Context-Artefakte mit fundamentalen Modellfähigkeiten verwechselt werden.

---

## MDR-002: Etablierung von „fufu“ als primäres Pilot-Konzept

- **Kontext:** Um Forschungsmethoden und Experiment-Pipelines zu validieren, wird ein konkreter Beispielbegriff benötigt.
- **Entscheidung:** Das im Briefing vorgeschlagene Wort `fufu` wird als primäres Referenzkonzept formalisiert ([`concepts/fufu.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/fufu.md)).
- **Semantischer Kern:** Vorsichtige Handlungsdurchführung, permanente Umfeldbeobachtung, Minimierung von Personen- und Sachgefährdung sowie zwingender Handlungsverzicht bei erkannter Schadensgefahr.
- **Konsequenzen:** `fufu` dient als Benchmark über drei verschiedene Test-Domänen (Tür öffnen, Vase greifen, Paket tragen).

---

## MDR-003: Strikte Trennung von Behauptungen und empirischem Nachweis

- **Kontext:** In der KI-Forschung besteht die Gefahr, dass ein gut formulierter Prompt als "erfolgreiches Sprachverständnis" deklariert wird, obwohl keine physikalische oder kausale Validierung stattgefunden hat.
- **Entscheidung:** Aussagen gelten im Projekt erst dann als "Befund", wenn sie durch ein reproduzierbares Experiment gestützt und in [`findings/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/findings) dokumentiert sind. Vorher sind sie in [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) als offen gekennzeichnet.
- **Konsequenzen:** Wissenschaftliche Integrität und Belastbarkeit künftiger Publikationen.

---

## MDR-004: Dreistufiger Evaluierungsansatz

- **Kontext:** Der Transfer auf reale Roboter ist ressourcenintensiv.
- **Entscheidung:**
  1. *Stufe 1:* Textbasierte Handlungsplanung & Constraint-Extraktion mit LLMs.
  2. *Stufe 2:* Physik-Simulation (z. B. PyBullet / Isaac Sim) mit Safety-Chip-Architektur.
  3. *Stufe 3:* HRI-Probandenstudien zur Absichtsbildung.
- **Konsequenzen:** Frühe Fehlertrennung und schnelle Iterationszyklen.

---

## MDR-005: Whorfian Alignment (Strukturelle Unkonstruierbarkeit gefährlicher Zustände)

- **Kontext:** Traditionelles Alignment (RLHF, DPO, System-Prompts) operiert rein probabilistisch. Das Modell „weiß“, wie schädliche Aktionen ausgeführt werden, und wird lediglich statistisch bestraft oder ermahnt. Unter Störung oder OOD-Bedingungen (z. B. unerwartetes Kleinkind im Raum) kann dieser Schutz versagen.
- **Entscheidung:** Das Projekt verfolgt den Ansatz des *Whorfian Alignment*: Durch gezielte Verankerung synthetischer Verhaltens-Neologismen (wie `fufu`) als diskrete Attraktoren/Konzepte im Latent Space werden gefährliche Handlungstrajektorien in der aktiven Konzept-Mannigfaltigkeit strukturell unrepräsentierbar gemacht. Der Roboter muss nicht ermahnt werden – er *kann* die kollidierende Handlung kognitiv nicht als Lösung konstruieren.
- **Konsequenzen:** Fokus der Forschung liegt auf der Verknüpfung von Umgebungs-Kontext mit der automatischen Aktivierung dieser Latent-Space-Konzepte.

---

## MDR-006: Cross-Domain Vulnerability Transfer als Leitparadigma des Begriffssystems

- **Kontext:** Die Fokussierung auf eine isolierte Nische (nur Haushalt oder nur Pflege) schwächt die Generalisierbarkeit des Papers ab und setzt das Projekt dem Vorwurf aus, eine Ad-hoc-Lösung für einen Einzelfall zu sein.
- **Entscheidung:** Das Begriffssystem wird nicht anwendungsfallspezifisch entworfen, sondern basiert auf der fundamentalen Schnittmenge: **Vulnerable Human Co-Presence (VHC)**. Die Begriffe kodieren universelle Gesetze von Schutzräumen, Kraftgrenzen und Diskretionsmustern, die gleichermaßen im Haushalt (Baby/Hund), in der Pflege (immobiler Patient/Hautfragilität) und in der Werkstatt (Mikromanipulation/Passanten) gelten.
- **Konsequenzen:** Der wissenschaftliche Hauptbeitrag des Papers wird der empirische Nachweis des **Zero-Shot Cross-Domain Transfers** (Out-of-Distribution Invariant Recall) sein. Keine Startup-Pitch-Rhetorik, sondern harte Transfermetriken.
