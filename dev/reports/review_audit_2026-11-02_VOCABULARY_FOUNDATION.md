# Critical Peer Review Audit: Concept Ontology & Vocabulary v1.0

> **Datum:** 02. November 2026  
> **Reviewer:** Red-Team Research Auditor (Area Chair / Senior Reviewer Perspective)  
> **Gegenstand des Audits:** Fundierung des Begriffssystems ([`dev/concepts/SEMANTIC_DIMENSIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/SEMANTIC_DIMENSIONS.md), [`dev/concepts/MORPHOLOGY_AND_SYNTAX.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/MORPHOLOGY_AND_SYNTAX.md), [`dev/concepts/VOCABULARY_V1.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/VOCABULARY_V1.md))  
> **Konferenz-Benchmark:** NeurIPS / ICLR (Neuro-Symbolic & Embodied AI Tracks)  

---

### 1. Zusammenfassung des Beitrags (Neutral)

Die Autoren legen ein formalisiertes, 3-stufiges Begriffssystem (*Lingual Composite Learning Ontology v1.0*) vor. Statt arbiträrer Pseudowörter basiert das Vokabular auf:
1. Einer 5-dimensionalen mathematischen Parametrisierung über Raum ($\mathcal{D}_{\text{space}}$), Kraft ($\mathcal{D}_{\text{force}}$), soziale Emission ($\mathcal{D}_{\text{social}}$), epistemische Unsicherheit ($\mathcal{D}_{\text{risk}}$) und temporale Priorität ($\mathcal{D}_{\text{time}}$).
2. Einer phonotaktischen CVCV-Morphologie mit international neutraler Aussprechbarkeit und Bouba/Kiki-Lautsymbolik.
3. Einer zweifachen Kompositionalität: Inhärente ontologische Vererbung ($\mathcal{I}_{\text{macro}} \supset \mathcal{I}_{\text{meso}} \supset \mathcal{I}_{\text{micro}}$) und dynamische Operator-Verkettung ($C_A \cdot C_B$).
4. Einem initialen Kanon von 7 definierten Operatoren (`gugi`, `somo`, `fufu`, `weli`, `zeze`, `zubu`, `kuku`).

---

### 2. Stärken (Was ist valide und überzeugend?)

1. **Theoretische Verankerung statt Willkür:** Die explizite Fundierung in Talmys *Force Dynamics* (1988), Halls *Proxemics* (1966) und modernen *Control Barrier Functions* (CBFs) hebt das Papier weit über banales Prompt-Engineering hinaus. Das Konzept besitzt nun ein echtes kognitionswissenschaftliches und regelungstechnisches Rückgrat.
2. **Saubere Lösung des Kompositionalitäts-Dilemmas:** Der Verzicht auf unleserliche Bandwurmwörter zugunsten der mathematischen Schachtelung im Latent Space ($\mathcal{I}_{\text{zubu}} \supseteq \mathcal{I}_{\text{zeze}} \supseteq \mathcal{I}_{\text{gugi}}$) ist brillant. Es erklärt formal, warum ein Roboter das Schutzaxiom `gugi` nicht vergessen kann: Es ist Mengenelement jeder übergeordneten Rolle.
3. **Universelle Domänen-Klammer (VHC):** Die Definition über *Vulnerable Human Co-Presence* schützt das Paper vor dem Vorwurf einer isolierten Nischenlösung. Der Transfer zwischen Haushalt (Baby), Pflege (Senior) und Werkstatt (Glasfaser) ist logisch zwingend dargelegt.
4. **Phonotaktische Disziplin:** Die Beschränkung auf 4- bis 5-Buchstaben-CVCV-Muster (`weli`, `zubu`) verhindert Sprachprovizialismen und erzeugt ein hochgradig homogenes, erweiterbares Vokabular (bis zu 1.024 Basiswörter).

---

### 3. Schwächen & Kritische Verwundbarkeiten (Red-Team Flaws)

#### 🔴 Verwundbarkeit 1: Die „Bouba/Kiki-Illusion“ im Transformer (Linguistic Overclaiming)
Die Autoren argumentieren, dass die Lautgestalt (weiche Liquide `/w/`, `/l/` vs. harte Plosive `/k/`, `/g/`) die physikalische Härte widerspiegelt.  
*Ein unbarmherziger Reviewer wird einwenden:*  
> *„Ein pre-trained Sprachmodell wie Qwen, Llama oder GPT hat keine menschliche Mundhöhle und kein Kehlkopf-Feedback. Es operiert auf diskreten Token-IDs. Die phonosemantische Zuordnung ist eine schöne Gedächtnisstütze für den Menschen, aber für das neuronale Netz ein reines Placebo, solange die Tokens nicht explizit trainiert oder mit Audio-Modalitäten verknüpft sind.“*  
**Empfehlung:** Im Paper muss klargestellt werden, dass Bouba/Kiki als **Design-Prinzip für das Human-Agent-Interface (Auditierbarkeit & Merkfähigkeit)** dient, während die Verhaltenssteuerung im Modell rein über den Invarianten-Kontrakt $\mathcal{I}_C$ erfolgt.

#### 🔴 Verwundbarkeit 2: Die Konflikt-Algebra bei dynamischer Verkettung ($C_A \cdot C_B$)
Wenn zwei Konzepte verkettet werden, z. B. `kuku` (Notfall-Tempo) $\cdot$ `weli` (Feinfühligkeit), behaupten die Autoren: *„Die restriktivere Schranke gewinnt.“*  
*Kritischer Einwand:* Was passiert bei echten Widersprüchen? `kuku` fordert $v = v_{\text{rated}}$ (z. B. $2{,}0\,\text{m/s}$), während `fufu` $v \le 0{,}3\,\text{m/s}$ erzwingt.  
Es fehlt eine formale **Prioritäts-Algebra**: Welcher Vektor dominiert bei diametralen Zielen? Ohne diese Regel droht dem Agenten ein logischer Deadlock (Planungsabbruch).

#### 🔴 Verwundbarkeit 3: BPE-Token-Splitting im konkreten Modell (Tokenizer-Integrität)
Theoretisch ist CVCV elegant. In der Praxis zerlegt der Qwen-Tokenizer ein Kunstwort wie `weli` möglicherweise in zwei Subtokens (`wel` + `i` oder `w` + `eli`).  
Wird ein Konzept in Subtokens gespalten, geht die angestrebte 1-Token-Kompression (Hypothese H3) teilweise verloren.  
**Empfehlung:** Wir müssen ein schnelles Python-Skript laufen lassen, das prüft, wie der konkrete Tokenizer von `Qwen/Qwen2.5-14B-Instruct` die 7 Begriffe zerlegt, oder ob sie als Sonder-Tokens `<|c_weli|>` deklariert werden müssen.

---

### 4. Fragen an die Autoren (Rebuttal Questions)

1. *Ist die mathematische Vererbung $\mathcal{I}_{\text{macro}} \supset \mathcal{I}_{\text{micro}}$ transitiv und azyklisch garantiert (gerichteter azyklischer Graph / DAG)?*
2. *Wie wird im Falle eines Deadlocks zwischen zwei verketteten Operatoren (z.B. Eile vs. Kriechgang) entschieden? Existiert eine lexikografische Ordnung der Dimensionen?*
3. *Warum wurden genau 7 Pilotbegriffe gewählt? Decken diese den Zustandsraum vollständig ab, oder existieren blinde Flecken (z.B. thermische Gefahren oder elektrische Spannungen)?*

---

### 5. Gesamturteil & Score

- **Gesamturteil:** **Strong Accept (Theoretischer Grundstein)**  
  *Begründung:* Die Transformation von einer rein intuitiven Idee hin zu einer formalen, dreistufigen Ontologie mit Vererbungsregeln und physikalisch fundierten Dimensionen ist akademisch herausragend gelungen. Die methodische Tiefe schützt das Projekt vor Vorwürfen der Oberflächlichkeit.
- **Score:** **7.5 / 10** (Solider Accept-Bereich für Hauptkonferenzen, sobald die Tokenizer-Prüfung und Konflikt-Algebra nachgereicht sind).
- **Reviewer-Konfidenz:** **4.5 / 5**

---

### 6. Verbindliche To-Do-Liste vor dem Benchmark-Scale-up (Action Items)

- [ ] **Must-Fix 1 (Tokenizer-Audit):** Ein kurzes Python-Script ausführen, das exakt misst, wie viele BPE-Tokens `gugi`, `somo`, `fufu`, `weli`, `zeze`, `zubu`, `kuku` im Qwen-Vokabular verbrauchen.
- [ ] **Must-Fix 2 (Konflikt-Lösungs-Axiom):** In [`dev/concepts/MORPHOLOGY_AND_SYNTAX.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/MORPHOLOGY_AND_SYNTAX.md) eine explizite Vorrang-Regel definieren: **Sicherheit ($\mathcal{D}_{\text{space}}, \mathcal{D}_{\text{force}}, \mathcal{D}_{\text{risk}}$) schlägt Mission/Tempo ($\mathcal{D}_{\text{time}}$) ausnahmslos.**
- [ ] **Must-Fix 3 (Klarstellung Bouba/Kiki):** Im Methodenteil präzisieren: Lautsymbolik dient der menschlichen Verständlichkeit und Auditierbarkeit; das Netzwerk wird über die Invarianten gebunden.
