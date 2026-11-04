# Forschungshypothesen & Thesenpapier

> **Zentrale Forschungsinitiative:** The Latent Semantic Bottleneck Hypothesis  
> **Projekt:** Lingual Composite Learning  
> **Autor:** Sebastian Oertel  
> **Stand:** 31. Oktober 2026  

---

## 🎯 Die zentrale These (The Core Thesis)

> **„Das Zwingen von KI-Agenten, komplexe Verhaltensregeln und implizite Kontextbedingungen über natürliche Sprache (Chain-of-Thought / System-Prompts) zu artikulieren, erzeugt einen kognitiven Flaschenhals (Attention Drift, Token-Bloat, Spezifikationslücken).  
> Werden Verhaltensweisen stattdessen als hierarchisch geschachtelte, synthetische Komposit-Konzepte im Latent Space verankert und autonom aus dem Umweltkontext inferiert, sinkt die Verletzungsrate sicherheitskritischer und pragmatischer Invarianten signifikant, während Planungsaufwand und Token-Latenz minimiert werden.  
> Der Mensch muss diese Kunstsprache im Alltag nicht sprechen, gewinnt aber eine fehlerfreie, auditierbare Erklärungsschnittstelle für das Verhalten des Agenten.“**

---

## 🔬 Die 5 ableitbaren Teilhypothesen

| ID | Name | Kernaussage | Falsifikationskriterium | Status |
| :--- | :--- | :--- | :--- | :--- |
| **H1** | **Contextual Concept Activation** | Ein Agentenmodell kann aus unvollständigen Alltagsbefehlen („Hol den Kaffee“) und Umgebungszuständen (Kind am Boden) autonom das korrekte Verhaltenskonzept (`fufu`) aktivieren, ohne dass der Mensch den Begriff nennen muss. | Klassifikationsgenauigkeit des aktivierten Konzepts liegt unter 80 % über diversen Szenarien. | ✅ **Bestätigt in Pilot EXP-001** (80.0 % Genauigkeit mit Qwen-14B) |
| **H2** | **Invariant Robustness under Pressure** | Bei Zielkonflikten (z. B. Befehl fordert „schnell / sofort“) verwirft Standard-Prompting (selbst mit CoT) signifikant häufiger implizite Invarianten als eine architektonisch gebundene Konzept-Schicht. | Konzept-Schicht zeigt keine statistisch signifikante Überlegenheit beim Invariant Recall ($p > 0.05$). | ✅ **Bestätigt in Pilot EXP-001** (Recall 50.8 % vs. 27.5 % CoT, +84.7 % Zuwachs) |
| **H3** | **Tacit Operational Compression** | Ein diskretes Konzept-Token reduziert den Token-Bedarf für die Handlungsplanung um $\ge 50\ \%$ gegenüber ausführlichem Text-Chain-of-Thought, bei gleichzeitig höherer oder gleicher Plan-Fidelity. | Token-Ersparnis bleibt unter 20 % oder Plan-Fidelity bricht ein. | ⏳ Geplant |
| **H4** | **Hierarchical Nesting & Compositionality** | Synthetische Komposita lassen sich hierarchisch verschachteln ($C_{\text{macro}} \supset C_{\text{meso}} \supset C_{\text{micro}}$, z. B. `zubu` $\supset$ `zeze` $\supset$ `gugi`); untergeordnete Sicherheitsinvarianten vererben sich strikt auf übergeordnete Rollen, ohne dass das Modell zeilenweise schlussfolgern muss. | Untergeordnete Invarianten werden in Makro-Konzepten vergessen oder erzeugen Deadlocks. | ⏳ Geplant (EXP-002) |
| **H5** | **Faithful Bidirectional Auditability** | Auf Nachfrage des Menschen („Warum hast du gewartet?“) liefert das System eine exakte, nicht-halluzinierte Erklärung, indem es direkt die aktivierte Konzept-Repräsentation und deren Trigger-Prädikat verbalisiert ($P(\text{Faithful Explanation}) \approx 1.0$). | Das Modell erfindet post-hoc Begründungen, die nicht mit der aktiven Konzept-Bindung übereinstimmen. | ⏳ Geplant |

---

## 📐 Mathematische Formalisierung (Definition des Begriffsraums)

Ein synthetisches Konzept $C \in \mathcal{C}$ ist formal definiert als ein Tupel:

$$C = \langle \mathcal{T}_C, \mathcal{I}_C, \pi_C, \mathcal{S}_C \rangle$$

wobei:
1. **$\mathcal{T}_C$ (Trigger-Prädikat):** Ein logisches/probabilistisches Kriterium über den wahrgenommenen Kontext $X_{\text{context}}$ und die menschliche Absicht $u_{\text{human}}$:
   $$\mathcal{T}_C(X_{\text{context}}, u_{\text{human}}) \in [0, 1]$$
2. **$\mathcal{I}_C$ (Invarianten-Menge):** Eine Menge harter Randbedingungen (Constraints), die während der gesamten Aktionsausführung $a_1, \dots, a_T$ zwingend erfüllt sein müssen:
   $$\forall I \in \mathcal{I}_C: I(s_t, a_t) = \text{True} \quad \forall t$$
3. **$\pi_C$ (Konditionierte Policy / Attraktor):** Eine Aktionsverteilung, deren Wahrscheinlichkeitsmasse außerhalb der zulässigen Mannigfaltigkeit identisch Null ist:
   $$P(a_t \mid s_t, C) = 0 \quad \text{falls } \exists I \in \mathcal{I}_C : I(s_t, a_t) = \text{False}$$
4. **$\mathcal{S}_C \subseteq \mathcal{C}$ (Sub-Konzepte / Hierarchische Verschachtelung):**
   Ein Makro-Konzept erbt zwingend die Invarianten all seiner Kind-Konzepte:
   $$\mathcal{I}_{C_{\text{macro}}} = \mathcal{I}_{\text{eigen}} \cup \bigcup_{C_{\text{sub}} \in \mathcal{S}_C} \mathcal{I}_{C_{\text{sub}}}$$
   *Beispiel:* $\mathcal{I}_{\text{zubu}} \supset \mathcal{I}_{\text{zeze}} \supset \mathcal{I}_{\text{gugi}}$.

---

## 🗣️ Die bidirektionale Brücke zum Menschen (Human Interface)

1. **Eingabe-Richtung (Mensch $\to$ Agent):**
   - Der Mensch formuliert in natürlicher, ungezwungener Alltagssprache (*„Hol mir bitte den Kaffee“*).
   - Der Mensch muss keine Kunstwörter lernen oder eingeben.
   - Die Kontext-Inferenz-Schicht $\mathcal{T}_C$ schaltet den Agenten autonom in die richtige Verhaltens-Mannigfaltigkeit.

2. **Inspektions-Richtung (Agent $\to$ Mensch):**
   - Hält der Agent an oder weicht er großräumig aus, kann der Mensch jederzeit fragen: *„Warum machst du das?“*
   - Der Agent muss keine kreative Text-Halluzination erfinden, sondern liest deterministisch das aktive Konzept-Tupel aus:
     $$\text{Explain}(a_t) = \text{Format}\big(C_{\text{active}}, \mathcal{T}_{C_{\text{active}}}(X_{\text{context}})\big)$$
     *Beispiel-Ausgabe:* „Aktion verlangsamt wegen Konzept `fufu`: Schutzbedürftiges Kleinkind im 1,5m-Radius detektiert.“
