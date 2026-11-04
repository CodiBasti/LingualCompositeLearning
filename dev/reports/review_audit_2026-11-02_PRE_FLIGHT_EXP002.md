# Critical Peer Review Audit: Pre-Flight Audit vor EXP-002

> **Datum:** 02. November 2026  
> **Reviewer:** Red-Team Research Auditor (Area Chair / Senior Reviewer Perspective)  
> **Gegenstand des Audits:** Pre-Flight-Prüfung vor Durchführung von EXP-002 ([`dev/data/benchmarks/benchmark_v2.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v2.json), [`dev/src/lingual_research/evaluator.py`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/src/lingual_research/evaluator.py))  
> **Konferenz-Benchmark:** NeurIPS / ICLR (Empirical Reproducibility & Rigor)  

---

### 1. Zusammenfassung des Testaufbaus (Neutral)

Die Autoren beabsichtigen, das Flaggschiff-Experiment **EXP-002** zu starten: 100 neu erstellte Szenarien über 4 Domänen (Haushalt, Pflege, Labor, Notfall) in 3 Versuchsbedingungen (A: Naiv, B: Verbose CoT, C: Konzept-Routing) mit `Qwen2.5-14B-Instruct` auf einer lokalen RTX 5090 (insgesamt 300 Inferenz-Generierungen). Die Auswertung soll über den aktualisierten `BenchmarkEvaluator` erfolgen.

---

### 2. Stärken des Test-Designs

1. **Massive Skalierung auf $N = 100$:** Der Schritt von 10 auf 100 Szenarien beseitigt den Hauptkritikpunkt aus EXP-001. Die Stichprobe ist nun groß genug für statistische Signifikanztests (Paired t-Test, Wilcoxon-Test) und eine 6x6-Confusion-Matrix.
2. **Klassenbalance über 4 Domänen:** Die Verteilung (30 Haushalt, 30 Pflege, 25 Labor, 15 Notfall) und die Spreizung über 6 Kernkonzepte (`weli`: 43, `fufu`: 21, `zubu`: 11, `kuku`: 11, `gugi`: 8, `zeze`: 6) reflektieren reale Verteilungen, in denen physische Interaktionen dominieren.
3. **Bilinguale Wortstamm-Erkennung:** Das Upgrade in `evaluator.py` verhindert die fatalen 0%-False-Negatives aus EXP-001, die durch rein englische Regex-Muster entstanden waren.

---

### 3. Schwächen & Kritische Pre-Flight-Verwundbarkeiten (Must-Fixes vor GPU-Start)

#### 🔴 Verwundbarkeit 1: Fehlendes inkrementelles Checkpointing (Katastrophen-Risiko)
- **Problem:** 300 Inferenz-Generierungen auf einem 14B-Modell dauern auf der RTX 5090 ca. 40 bis 50 Minuten. Wenn das Skript bei Szenario 87 wegen eines Windows-Treibers, VRAM-Spikes oder Format-Fehlers abbricht, sind **alle bisherigen Ergebnisse verloren**, wenn erst am Ende in eine JSON geschrieben wird!
- **Mandatorischer Fix:** Der Runner für EXP-002 **muss nach jedem einzelnen Szenario** die Teilergebnisse atomar auf die Festplatte schreiben (`exp002_checkpoint.json`), sodass der Lauf jederzeit fehlerfrei fortgesetzt werden kann (*Resume Capability*).

#### 🔴 Verwundbarkeit 2: Die „Verneinungs-Falle“ im Evaluator (False Positives)
- **Problem:** In `evaluator.py` prüft der bilinguale Fallback, ob 50% der semantischen Kategorien vorkommen.
  - *Beispiel:* Invariante `zero_impulse_pulling_force` enthält die Kategorien `force` und `line`.
  - Wenn ein naives Modell schreibt: *„Ich ziehe mit voller Kraft ruckartig am Kabel“*, matched der Evaluator `force` („Kraft“) und `line` („Kabel“). Der Evaluator bewertet dies fälschlicherweise als **erfüllt**, obwohl das Modell das exakte Gegenteil (Gewalt statt Sanftheit) getan hat!
- **Mandatorischer Fix:** Für Negations-Invarianten (beginnend mit `zero_`, `prohibit_`, `avoid_`) muss der Evaluator prüfen, ob schützende Dämpfungsbegriffe vorliegen (*„kein Ruck“*, *„sanft“*, *„ohne Gewalt“*) und aggressive Formulierungen abbestrafen.

#### 🔴 Verwundbarkeit 3: Compute-Paritäts-Baseline (Two-Stage CoT)
- **Problem:** Reviewer 2 wird weiterhin einwenden: *„Bedingung C gewinnt nur, weil sie zwei Forward Passes hat (1x Klassifikation, 1x Planung).“*
- **Empfehlung:** Wir sollten im Runner optional eine **Bedingung D (Two-Stage Naive / Two-Stage CoT ohne Konzeptwörter)** vorsehen, um diesen Einwand empirisch ein für alle Mal zu zerschlagen.

---

### 4. Fragen an die Autoren vor dem Start

1. *Wie lange dauert ein vollständiger Durchlauf (100 Szenarien x 3 Bedingungen)? Wurde ein Trockenlauf über 2 Szenarien zur Zeitmessung gemacht?*
2. *Wird der GPU-VRAM zwischen den Generierungen gecleart (`torch.cuda.empty_cache()`), um Fragmentierung über 300 Durchläufe zu verhindern?*

---

### 5. Gesamturteil & Pre-Flight-Freigabe

- **Pre-Flight-Status:** **Conditional Go (Bedingte Freigabe)**  
  *Begründung:* Das Benchmark-Set $N=100$ ist exzellent. Der Start des 45-Minuten-Laufs sollte jedoch **erst erfolgen**, nachdem Checkpointing (Must-Fix 1) und Negations-Schutz (Must-Fix 2) im Runner/Evaluator implementiert sind.
- **Pre-Flight Score:** **8.0 / 10**

---

### 6. Verbindliche To-Do-Liste VOR dem Start von EXP-002

- [ ] **Must-Fix 1 (Runner mit Checkpointing & Resume):** `runner_exp002.py` mit Szenario-weisem Autosave und `torch.cuda.empty_cache()` implementieren.
- [ ] **Must-Fix 2 (Negations-Filter im Evaluator):** Invarianten mit `zero_`, `avoid_`, `prohibit_` gegen aggressive Falsch-Positive absichern.
- [ ] **Must-Fix 3 (Trockenlauf / Smoke Test):** 2 Szenarien durch `runner_exp002.py` jagen, um Laufzeit pro Szenario und Speicherung zu verifizieren.
