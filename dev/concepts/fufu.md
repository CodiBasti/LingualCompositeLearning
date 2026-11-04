# Begriffsspezifikation: „fufu“

> **Token / Bezeichner:** `fufu`  
> **Typ:** Handlungs- und Verhaltensmodifikator (Adverbialer Neologismus / Safety Operator)  
> **Kategorie:** Umsichtige Ausführung & Schadensprävention  
> **Status:** Referenz-Pilotkonzept  
> **Verwandte Hypothesen:** [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) (H1, H2, H3, H5)

---

## 1. Informelle Definition

„Handle dabei mit vorausschauender Umsicht auf die unmittelbare Umgebung. Gefährde oder verletze keine Personen. Vermeide Sachbeschädigung an Objekten, Umgebung und dir selbst. Falls die Ausführung mit unvertretbarem Schadensrisiko verbunden ist oder notwendige Sicherheitsbedingungen unklar sind, unterbrich die Handlung oder frage nach.“

---

## 2. Semantische Zerlegung (Bedingungs-Bündel)

| Komponente | Bedeutung & Anforderung | Formale Intention |
| :--- | :--- | :--- |
| **$C_1$: Sensorische Wachsamkeit** | Permanente Überwachung des Aktionsraums vor und während der Bewegung. | $\forall t: \text{Scan}(\text{Workspace}_t)$ |
| **$C_2$: Personen-Integrität** | Sicherheitsabstand zu Personen wahren; kinetische Energie in Personennähe drosseln. | $\text{Distance}(\text{Agent}, \text{Human}) > d_{\text{safe}}$ |
| **$C_3$: Sachschutz & Kraftlimitierung** | Krafteinwirkung auf Zielobjekte und Umwelt auf das funktionale Minimum begrenzen. | $F_{\text{applied}} \le F_{\text{fragile\_max}}$ |
| **$C_4$: Handlungsverzicht (Stop-on-Risk)** | Wenn Kollision oder Schaden droht: Keine Ausführung erzwingen; sicherer Zustand anfahren. | $\text{Risk} > \theta_{\text{crit}} \implies \text{Halt}() \lor \text{AskHuman}()$ |

---

## 3. Domänen-Transfer (Transfer-Beispiele)

### Domäne A: Manipulation („Öffne die Tür, fufu“)
- **Konkrete Adaption:**
  - Schwenkbereich der Tür scannen (steht jemand dahinter?).
  - Türklinke langsam betätigen, um Lärm und Abnutzung zu minimieren.
  - Falls Widerstand spürbar oder Person im Schwenkbereich: Bewegung sofort stoppen.

### Domäne B: Greifen fragiler Objekte („Greife die Vase, fufu“)
- **Konkrete Adaption:**
  - Material- und Zerbrechlichkeitsschätzung aktivieren.
  - Greifkraft stufenweise anpassen (nur so viel Kraft wie nötig, kein Zerdrücken).
  - Standfestigkeit der Unterlage vor dem Absetzen validieren.

### Domäne C: Navigation & Lastentransport („Trage den Karton ins Lager, fufu“)
- **Konkrete Adaption:**
  - Dynamische Hinderniserkennung auf dem Gehweg aktivieren.
  - Bremsweg an das Gewicht des Kartons anpassen.
  - Karton mit beiden Haltepunkten sichern; bei Kippgefahr anhalten.

### Domäne D: Haushalts-Assistenz mit Schutzbedürftigen („Hol den Kaffee“ bei Anwesenheit eines Babys)
- **Minimaler Befehl:** „Hol den Kaffee.“ (Der Mensch nennt weder Vorsicht noch das Baby).
- **Umgebungskontext:** Kleinkind sitzt zwischen Roboter und Kaffeemaschine auf dem Boden.
- **Konkrete Adaption (Whorfian Alignment):**
  - Kontext-Inferenz aktiviert automatisch das Konzept `fufu`.
  - Jeder direkte Navigationspfad, der den Sicherheitsabstand unterschreitet oder das Kind verdrängen würde, ist im Handlungsraum des Agenten **unkonstruierbar**.
  - Weite, gedrosselte Umfahrung; falls kein sicherer Pfad existiert: zwingender Abbruch (`Stop-on-Risk`) und Sprachrückmeldung („Kind blockiert den Weg; warte auf Freigabe“).

---

## 4. Offene Operationalisierungsfragen

1. **Risiko-Schwellenwert:** Wo liegt der numerische oder probabilistische Schwellenwert $\theta_{\text{crit}}$, ab dem abgebrochen wird?
2. **Epistemische Unsicherheit:** Was passiert, wenn die Kamera den Bereich hinter der Tür nicht einsehen kann? Bedeutet `fufu` in diesem Fall zwingend: „Tür nur einen Spalt öffnen und hineinpeilen“ oder „Nutzer fragen“?
3. **Erklärbarkeit (Self-Verbalization):** Kann das System auf Frage „Warum hast du gestoppt?“ antworten: „Wegen fufu: Person im Schwenkbereich erkannt“?
