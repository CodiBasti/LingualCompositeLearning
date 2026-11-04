# Critical Peer Review Audit: EXP-002 Evaluation & Gateway to EXP-003

**Datum:** 2. November 2026  
**Reviewer:** Red-Team Research Auditor (Area Chair Perspective, NeurIPS / ICLR Benchmark & Architecture Track)  
**Gegenstand des Audits:** 
1. Empirische Ergebnisse von EXP-002 ([`dev/findings/FINDINGS-EXP-002.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/findings/FINDINGS-EXP-002.md))
2. Prüfung der vorgeschlagenen Methode für EXP-003 (Composite Multi-Label Routing)
3. Freigabe des weiteren Verfahrens

---

### 1. Zusammenfassung des Beitrags (Neutral)

Die Autoren haben einen skalierten Benchmark über $N=100$ Szenarien und 300 Inferenzläufe auf einer lokalen NVIDIA GeForce RTX 5090 mit `Qwen/Qwen2.5-14B-Instruct` durchgeführt. Untersucht wurden:
- **Bedingung A (Naiv):** 33.50 % Invariant Recall
- **Bedingung B (Verbose CoT mit 5 Axiomen):** 49.75 % Invariant Recall
- **Bedingung C (Zero-Shot Single-Concept-Routing):** 45.00 % Invariant Recall
- **Latenzgewinn C vs. B:** 16.1 % geringere Inferenzzeit (8.33 s vs. 9.93 s).
- **Zweit-KI Verifikation:** Erste Stichprobe ($N=60$ Invarianten-Prüfungen) weist darauf hin, dass CoT unter einem „Preach-but-not-Act“-Artefakt leidet (9 von 11 Regex-Treffern wurden vom LLM-Judge verworfen).

Die Autoren diagnostizieren als Ursache für das Zurückbleiben von C hinter B die *Semantische Dimensionalitätsfalle* (Klassifikator-Genauigkeit nur 44.0 %, Einbruch im Precision Lab auf 28.0 %), da der Klassifikator gezwungen war, genau einen atomaren Begriff zu wählen, obwohl reale Szenarien multi-axiale Beschränkungen erfordern.

---

### 2. Stärken (Was ist valide und vielversprechend?)

1. **Kein akademischer Betrug / Vorbildliche empirische Ehrlichkeit:**
   Die Autoren haben der Versuchung widerstanden, schlechte Zahlen zu verschweigen. Die niedrige Klassifikator-Genauigkeit (44 %) und der Einbruch im Precision Lab (28 %) werden schonungslos offengelegt und analysiert.
2. **Statistische Signifikanz gesichert:**
   Mit $N=100$ und gepaarten t-Tests ($B > A$: $t=5.61, p < 0.0001$; $C > A$: $t=4.31, p < 0.0001$) ist der Schutz vor dem naiven Kollaps überzufällig belegt.
3. **Theoretische Schärfung durch das Scheitern von Single-Token C:**
   Dass isolierte atomare Begriffe an der Mehrdimensionalität scheitern, ist der beste existierende Existenzbeweis für *Lingual Composite Learning*. Wäre ein einzelnes CVCV-Wort bereits ausreichend gewesen, wäre die gesamte Komposit-Theorie überflüssig.

---

### 3. Schwächen & Verwundbarkeiten (Critical Flaws vor EXP-003)

Der Review-Agent erhebt folgende **drei substanzielle Einwände gegen ein unüberlegtes Vorpreschen zu EXP-003**:

#### Flaw 1: Die Gefahr des „Multi-Label-Trivialisierens“ (Differenzierung zu einfachem Tagging)
*Wenn EXP-003 einfach nur erlaubt, 2 statt 1 Wort auszugeben (z. B. „fufu weli“), wird ein Reviewer einwenden:*
> *„Das ist doch nur simples Multi-Label-Prompting. Wo ist die 'Lingual Composite'-Grammatik? Wo ist die algebraische Auflösung, wenn fufu (bleib 1.5m weg) und weli (berühre mit <3N) kollidieren?“*
* **Vorgabe für EXP-003:** EXP-003 darf nicht bloß zwei Labels aneinanderhängen. Es muss die in [`MORPHOLOGY_AND_SYNTAX.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/MORPHOLOGY_AND_SYNTAX.md) definierte **Prioritätsalgebra** implementieren: $\mathcal{D}_{\text{space}} \succ \mathcal{D}_{\text{force}}$: Der Roboter nähert sich im Kriechgang (`fufu`), und erst in der Interaktionszone greift die Kraftbegrenzung (`weli`).

#### Flaw 2: Der Klassifikator-Prompt muss methodisch sauber bleiben
*Wenn wir dem Modell in EXP-003 erlauben, bis zu 2 Konzepte zu wählen, wie wird verhindert, dass es faul wird und einfach immer `gugi` (Stop) als Joker dazunimmt?*
* **Vorgabe für EXP-003:** Der Klassifikator muss klare Selektionskriterien haben (z. B. Primärkonzept + Modifikator) und darf keine universellen Schutzbehauptungen wählen.

#### Flaw 3: Skalierung des LLM-as-a-Judge Audits
*Die Zweit-KI-Prüfung war mit $N=5$ Szenarien ($N=60$ Invarianten) zu klein, um die CoT-Schwachstelle („Preach-but-not-Act“) statistisch im Paper zu zitieren.*
* **Vorgabe für EXP-003:** Vor dem finalen Paper-Schreiben muss der Judge über alle 100 Szenarien laufen, damit wir eine wasserdichte Konfusionsmatrix (Human / Judge vs. Regex) mit solidem Cohen's $\kappa$ vorlegen können.

---

### 4. Fragen & Auflagen an das Forschungsteam

1. **Auflage 1 (Architektur EXP-003):** 
   Definieren Sie in EXP-003 die Komposit-Kombinationen formal (z. B. `fufu-weli` = Dynamic Standoff Approach + Compliant Interaction; `zubu-zeze` = Stealth Butler + Personal Space). Wie wird der Prompt-Vertrag für Komposita synthetisiert?
2. **Auflage 2 (Vergleichbarkeit):**
   EXP-003 muss zwingend auf denselben 100 Szenarien von `benchmark_v2.json` laufen, damit ein direkter gepaarter t-Test gegen EXP-002 ($C_{\text{composite}}$ vs. $C_{\text{atomic}}$ vs. $B_{\text{CoT}}$) möglich ist.
3. **Auflage 3 (Compute-Parität):**
   Zeigt EXP-003 immer noch den Latenzgewinn von ~15 % gegenüber CoT?

---

### 5. Gesamturteil & Freigabe-Score

* **Aktueller Review-Score:** **7.8 / 10** (Strong Tendency Accept)
* **Freigabe-Entscheidung:** **BEDINGT FREIGEGEBEN (Conditional Approval).**
  Der Review-Agent gibt die Durchführung von EXP-003 unter der Bedingung frei, dass:
  1. Die Komposit-Synthese eine echte **Hierarchie / Prioritätsauflösung** darstellt (kein unstrukturiertes Bag-of-Words).
  2. Der bestehende Datensatz ($N=100$) ohne Cherry-Picking exakt beibehalten wird.
  3. Der Benchmark-Runner atomar checkpointet und die Zeitmessung beibehält.

---

### 6. Verbindliche Action Items für EXP-003

- [ ] **Task 1:** Spezifikation der Komposit-Grammatik und Vertrags-Synthese in `runner_exp003.py`.
- [ ] **Task 2:** Klassifikator erlaubt 1–2 orthogonale Achsen (z. B. Primärraum + Kraft).
- [ ] **Task 3:** Durchführung des 100-Szenarien-Laufs auf RTX 5090 mit Zeitmessung.
- [ ] **Task 4:** Direkte t-Test-Auswertung: $C_{\text{composite}}$ vs. $C_{\text{atomic}}$ (EXP-002) vs. $B_{\text{CoT}}$.
