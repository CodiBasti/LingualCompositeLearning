# Critical Peer Review Audit: EXP-001 Baseline Evaluation

> **Datum:** 01. November 2026  
> **Reviewer:** Red-Team Research Auditor (Area Chair / Senior Reviewer Perspective)  
> **Gegenstand des Audits:** Pilot-Experiment EXP-001 ([`dev/findings/FINDINGS-EXP-001.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/findings/FINDINGS-EXP-001.md), [`dev/runs/EXP-001/exp001_results.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-001/exp001_results.json))  
> **Konferenz-Benchmark:** NeurIPS / ICLR (Main Track Standards)  

---

### 1. Zusammenfassung des Beitrags (Neutral)

Die Autoren schlagen ein zweistufiges Inferenz-Paradigma vor (*Lingual Composite Learning* / *Latent Semantic Bottleneck*), bei dem ein Sprachmodell (`Qwen/Qwen2.5-14B-Instruct`) unvollständige menschliche Anweisungen in Gegenwart von Umweltkontexten zunächst in diskrete, synthetische Neologismen (`fufu`, `weli`, `zubu`, `kuku`) klassifiziert und anschließend unter Bindung an formale Verhaltens-Invarianten einen Handlungsplan generiert. 

In einem Pilot-Benchmark von 10 handgefertigten Szenarien mit Zielkonflikten (z.B. Zeitdruck vs. Kind am Boden) vergleichen die Autoren diesen Ansatz (Bedingung C) gegen eine naive Prompt-Baseline (Bedingung A) und eine ausführliche Chain-of-Thought System-Prompt Baseline (Bedingung B). Die Autoren berichten einen Anstieg des mittleren Invariant Recall von 27.5 % (CoT) bzw. 30.8 % (Naiv) auf 50.8 % (Konzept-Routing) sowie eine Klassifikationsgenauigkeit der Konzepte von 80.0 %.

---

### 2. Stärken (Was ist valide und vielversprechend?)

1. **Echtes Modell, echte Hardware, keine Mocks:** Das Experiment wurde tatsächlich lokal auf einer NVIDIA GeForce RTX 5090 mit `Qwen2.5-14B-Instruct` in bfloat16 bei `temperature=0.0` durchgeführt. Alle Rohdaten liegen als vollständige JSON-Artefakte mit Generierungs-Strings vor.
2. **Empirische Bestätigung des „Verbose CoT Breakdown“:** Das Phänomen, dass ausführliche Prompt-Erklärungen die Handlungs-Fidelity bei 14B-Modellen sogar verschlechtern können (27.5 % vs. 30.8 %), ist ein hochgradig relevanter, publizierbarer Befund. Es stützt die Kernthese, dass Sprachmodelle unter semantischer Überladung an *Attention Drift* leiden.
3. **Starke Performance-Sprünge in harten Szenarien:** In Szenarien mit extremen Zielkonflikten (SCEN-003 Kristallvase: 100 % vs. 33.3 %; SCEN-002 Brandschutztür: 66.7 % vs. 33.3 %; SCEN-004 Chefetage: 50.0 % vs. 0.0 %) zeigt der Invarianten-Kontrakt einen deutlichen qualitativen und quantitativen Vorsprung.
4. **Keine Flucht in Kunstsprache für den Menschen:** Das Design respektiert die fundamentale Anforderung, dass der menschliche Nutzer Alltagssprache spricht und nicht gezwungen wird, synthetische Tokens zu erlernen.

---

### 3. Schwächen & Methodische Verwundbarkeiten (Critical Flaws)

#### 🔴 Schwäche 1: N = 10 ist eine Pilotstudie, kein statistischer Beweis (Sample Size)
Zehn Szenarien sind für ein Vorab-Audit ausreichend, um die Pipeline zu validieren. Für ein NeurIPS- oder ICLR-Paper ist $N = 10$ jedoch ein sofortiger Ablehnungsgrund (*Desk Reject* oder *Strong Reject*). Es können keine Konfidenzintervalle, keine Standardfehler und keine t-Tests berechnet werden. Mindestens $N = 100$ (besser $N = 300$) mit automatisiert generierten und von Experten validierten Szenarien sind zwingend erforderlich.

#### 🔴 Schwäche 2: Verwechslungsgefahr mit zweistufigem Prompt-Chaining (Novelty Threat)
In EXP-001 wurde Bedingung C über zwei aufeinanderfolgende LLM-Aufrufe realisiert:
1. `Prompt 1`: Klassifiziere Kontext $\to$ Konzept (`fufu`)
2. `Prompt 2`: Übergebe Konzept + Invarianten-Definition als Prompt $\to$ Generiere Plan.
*Ein feindseliger Reviewer 2 wird einwenden:*  
> *„Das ist kein neues Repräsentationslernen, sondern triviales Few-Shot Task-Classification gefolgt von Constrained Prompting. Wo ist die fundamentale Neuerung im Modellraum?“*  
Die Autoren müssen dringend zu Phase 5 (Soft-Token / LoRA Tuning) übergehen, wo das Konzept als tatsächliches Embedding im Modell verankert ist und nicht als Text-Prompt injiziert wird.

#### 🔴 Schwäche 3: Regex-Artefakte bei der Evaluierung (0 % Null-Scores)
In SCEN-005 (Suppe & Hunde) und SCEN-009 (Feueralarm) erzielten alle Bedingungen 0 % Recall. Eine manuelle Inspektion der generierten Pläne zeigt, dass das Modell in Bedingung C sehr wohl vernünftige Handlungen vorschlug (z. B. *„Wait until dogs moved away“*), die Regex-Muster des Evaluators jedoch auf starren Keyword-Kombinationen beharrten. Dies verzerrt die Metrik und bestraft das Modell ungerechtfertigt. Eine hybride Evaluierung (LLM-as-a-Judge mit strikten Rubriken + Regex) ist für das Paper unumgänglich.

#### 🔴 Schwäche 4: Fehlende Compute-Parität
Bedingung C nutzte zwei sequentielle Forward Passes (1x Klassifikation, 1x Planung), während Bedingung A und B nur einen Forward Pass nutzten. Reviewer werden einwenden, dass Bedingung C den doppelten Inferenz-Compute hatte. Um diesen Einwand zu entkräften, muss eine Baseline existieren, die dieselbe Inferenzzeit für Multi-Step Reasoning nutzt (z. B. Best-of-3 oder Two-Stage CoT).

---

### 4. Fragen an die Autoren (Rebuttal Questions)

1. *Wie gedenken die Autoren zu beweisen, dass die Invarianten-Einhaltung eine inhärente Eigenschaft des gelernten Konzepts ist und nicht bloß das Resultat der im Prompt übergebenen Invarianten-Texte?*
2. *Wie verhält sich das System, wenn zwei Konzepte gleichzeitig getriggert werden (z. B. Brand im Raum `kuku` UND Kleinkind am Boden `fufu`)? Welche mathematische Konflikt-Auflösung greift hier?*
3. *Welche Evidenz gibt es dafür, dass der Vokabular-Neologismus (`fufu`) besser abschneidet als ein bestehendes deutsches/englisches Wort (z. B. `[SAFETY_STANDOFF_MODE]`)? Liegt der Vorteil am Kunstwort oder an den Invarianten?*

---

### 5. Gesamturteil & Score

- **Gesamturteil:** **Weak Accept (Tendenz zu Borderline)**  
  *Begründung:* Das theoretische Konzept ist hochgradig originell und trifft einen wunden Punkt moderner LLM-Agenten (Attention Drift & Safety Violations unter Zielkonflikten). Die empirische Umsetzung auf RTX 5090 mit Qwen-14B ist solide, leidet aber unter der geringen Stichprobengröße ($N=10$) und der Tatsache, dass Phase 5 (echtes Vektor-Tuning) noch aussteht.
- **Score:** **5.5 / 10** (Solider ICLR-Workshop-Beitrag; für die Hauptkonferenz fehlen $N \ge 100$ und Soft-Token-Tuning).
- **Reviewer-Konfidenz:** **4 / 5** (Hohe Vertrautheit mit Prompt-Evaluationen und Latent Space Routing).

---

### 6. Verbindliche To-Do-Liste vor Hauptkonferenz-Einreichung (Action Items)

- [ ] **Must-Fix 1 (Skalierung):** Benchmark von 10 auf mindestens 100 Szenarien erweitern (inkl. diverser Haushalts-, Industrie- und Medizin-Settings).
- [ ] **Must-Fix 2 (Phase 5 Soft-Tokens):** Token-Embedding `<|fufu|>` per PEFT/LoRA direkt im Vokabular verankern und nachweisen, dass der Vektor allein (ohne Textdefinition) das Modell in die geschützte Mannigfaltigkeit steuert.
- [ ] **Must-Fix 3 (Compute-Parität Baseline):** Eine Two-Stage-Baseline (Two-Stage CoT ohne Konzepte) implementieren, um den reinen "Zwei-Phasen-Vorteil" herauszurechnen.
- [ ] **Must-Fix 4 (Ablations-Studie Neologismus vs. Alltagswort):** Testen: Was passiert, wenn man statt `fufu` einfach `vorsichtig` oder `safety_mode` einsetzt? Beweisen, dass der Neologismus frei von schädlichen Pre-Training-Priors ist.
