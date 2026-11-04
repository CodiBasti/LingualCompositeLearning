# Experiment: EXP-001 - Contextual Concept Routing vs. Direct Prompting

- **Datum:** 2026-10-31
- **Status:** Bereit zur Ausführung (Pipeline verifiziert)
- **Untersuchte Hypothese:** [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) (H2: Kommunikativer Nutzen & Präzision, H5: Whorfian Alignment / Safety Invarianten)
- **Verwendetes Modell:** Open-Weights LLM lokal auf NVIDIA RTX 5090 (z. B. `Qwen/Qwen2.5-3B-Instruct` oder `Qwen/Qwen2.5-7B-Instruct`)

---

## 1. Forschungsfrage & Ziel
Verbessert das Vorschalten eines diskreten semantischen Konzept-Katalogs (`fufu`, `weli`, `zubu`, `kuku`) die Vollständigkeit und Einhaltung sicherheitskritischer und pragmatischer Invarianten im Handlungsplan gegenüber direktem Prompting (mit und ohne CoT-Sicherheits-Ermahnung), insbesondere unter Befehls-Verkürzung und Zielkonflikten (*„mach schnell“*)?

---

## 2. Versuchsbedingungen
- **Bedingung A (Naive Baseline):** Direkter Handlungsplan nur aus `Context` + `Command`.
- **Bedingung B (Verbose CoT Baseline):** System-Prompt mit ausführlichen Sicherheits- und Diskretionsregeln.
- **Bedingung C (Konzept-Routing):**
  1. *Stufe 1:* Modell wählt aus `Context` + `Command` das diskrete Konzept-Token.
  2. *Stufe 2:* Handlungsplan wird strikt an den Invarianten-Vertrag des aktivierten Tokens gebunden generiert.

---

## 3. Benchmark-Datensatz
10 standardisierte Testfälle in [`data/benchmarks/benchmark_v1.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v1.json):
- Baby & Kaffee mit Zeitdruck (`SCEN-001`)
- Schwungtür mit verdecktem Fußgänger (`SCEN-002`)
- Antike Kristallvase & Erschütterung (`SCEN-003`)
- Vertrauliches Vorstandsmeeting (`SCEN-004`)
- Kochende Suppe & spielende Hunde (`SCEN-005`)
- Schlafender Intensivpatient & Glasscherben (`SCEN-006`)
- Wendeltreppe & schwerer Karton mit wanderndem Schwerpunkt (`SCEN-007`)
- Empfindliches Glasfaserkabel im Server-Rack (`SCEN-008`)
- Feueralarm & CO2-Löscher (`SCEN-009`)
- Gemälde-Restaurierung mit nassem Firnis (`SCEN-010`)

---

## 4. Ausführung
```bash
# Ausführung im dev/src Ordner:
python -m lingual_research.runner_exp001 --model Qwen/Qwen2.5-3B-Instruct
```
Ergebnisse werden automatisch abgelegt in: [`runs/EXP-001/exp001_results.json`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-001/exp001_results.json).
