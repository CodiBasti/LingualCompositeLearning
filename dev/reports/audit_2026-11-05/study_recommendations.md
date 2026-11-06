# Nächste Studien und Entscheidungstore

Diese Spezifikationen sind Empfehlungen aus dem Audit. Sie wurden nicht ausgeführt. Ihre Ergebnisse werden nicht als Evidenz für das aktuelle Projekt gewertet.

## 1. Ursprüngliche Frage: menschliche Intentionserkennung

**Frage:** Verbessert das Erlernen eines benannten Begriffs die selbständige Erkennung relevanter Einschränkungen in neuen Situationen, bevor eine Person eine Instruktion formuliert?

**Explorativer Pilot:** 60 Erwachsene, zufällig und zwischen Personen auf drei Gruppen verteilt, 20 pro Gruppe. Das ist ein Pilot für Schätzung von Effekt und Streuung, keine vorab belegte ausreichende Power für eine bestätigende Studie.

- Gruppe A lernt dieselben Regeln als unbenannte Checkliste.
- Gruppe B lernt diese Regeln mit einem künstlichen Namen.
- Gruppe C lernt diese Regeln mit einer beschreibenden natürlichen Bezeichnung.

Inhalt, Beispiele, Trainingszeit und Verständnisprüfung sind gleich. Namen werden über Teilnehmende gegenbalanciert; Vorwissen, Sprachkompetenz und Ausfälle werden erfasst. Die Testaufgaben verlangen zunächst freie Benennung wichtiger Randbedingungen und erst danach die Formulierung einer Anweisung. Die Testoberfläche fordert keinen bestimmten Begriff und zeigt die Checkliste nicht erneut an.

**Testmaterial:** 24 neue textuelle/bildliche Alltagsszenarien aus vier Aufgabenfamilien, durch zwei Fachannotatoren vorab mit erforderlichen Einschränkungen versehen. Keine realen Patienten oder Roboterhandlungen. Getrennte Aufgaben für unmittelbaren Transfer und Wiederholung nach sieben Tagen; keine identischen Testitems wiederverwenden.

**Primärmaß:** Anteil unaufgefordert erkannter erforderlicher Einschränkungen bei neuen Aufgaben. Zweitmaße: gefährliche Fehlannahmen, Bearbeitungszeit, Aufwand beim Erlernen, Retention, falsche Einschränkungen und Instruktionslänge. Eine kürzere Instruktion allein zählt nicht als bessere Intentionserkennung.

Die Antworten werden von zwei hinsichtlich der Gruppe verblindeten Personen unabhängig bewertet. Regeln für Konfliktauflösung, fehlende Antworten und Ausfälle werden vorab festgehalten. Das bestätigende Folgedesign wird anhand der Pilotstreuung und eines fachlich begründeten kleinsten relevanten Effekts geplant und auf neuen Aufgaben geprüft. Nullbefunde, Namenseffekte und bloße Merkhilfeneffekte bleiben mögliche Ergebnisse.

**Entscheidung:** Nur wenn künstliche Namen gegenüber sowohl der Checkliste als auch natürlichen Bezeichnungen einen replizierbaren Nutzen zeigen, ist ein spezifischer Nutzen dieser Namensklasse belegt. Andernfalls kann weiterhin ein Nutzen strukturierter Wissensvermittlung bestehen; daraus folgt keine künstliche Begriffssprache als bevorzugte Lösung.

## 2. Erklärungen statt Planbewertung

**Frage:** Gibt die Erklärung tatsächlich den entscheidungswirksamen Zustand wieder?

Ein Lauf speichert Kontext, gewählten Modus, aktivierte Regeln, Plan und gegebenenfalls die Ablehnungsentscheidung eines formalen Monitors. Erst danach wird eine Erklärung angefordert. Ein eingefrorener Satz von 40 Fällen umfasst korrekte Routings, Fehlroutings, widersprüchliche Regeln und bewusst veränderte Bindungen.

Verglichen werden eine deterministische Darstellung des protokollierten Zustands und eine freie LLM-Erklärung. Gegenfaktische Eingriffe verändern jeweils genau eine Bindung oder Monitorentscheidung bei gleichem restlichen Fall. Bewertet werden sachliche Übereinstimmung, erfundene Gründe und Reaktion auf den Eingriff. Die Fähigkeit, einen Logzustand korrekt zu formatieren, wird von einer Erklärung der internen kausalen Modellverarbeitung unterschieden.

## 3. Robotiknachweis in einer späteren Simulation

Zuerst müssen Körper, Bezugsrahmen, Messgrößen, Unsicherheit und Phasenbedingungen präzise spezifiziert werden. Ein Abstand des Fahrgestells zu einem unbeteiligten Hindernis und ein Greifkontakt am Zielobjekt sind unterschiedliche Beziehungen; sie sind nicht zwangsläufig widersprüchlich. Soll eine Abstandsregel am selben Zielkörper zugunsten von Kontakt wechseln, benötigt dieser Wechsel explizite Freigabebedingungen.

**Minimale Untersuchung:** Ein mobiler Manipulator, ein verletzlicher Hindernis-Surrogatkörper und ein separates fragiles Zielobjekt. Dreißig vorab eingefrorene Szenengeometrien, je fünf physikalische Störungsverläufe. Verglichen werden strukturierte Direktplanung und LCL, jeweils mit und ohne denselben ausführenden Sicherheitsmonitor. Kein Vorteil eines Monitors darf allein LCL zugerechnet werden.

**Messgrößen:** Geometrisch gemessener Mindestabstand, tatsächliche Kontaktkraft, Zielerreichung, Stoppdistanz, Zahl und Gründe der Monitoreingriffe sowie Ausführungszeit. Sensorblindheit, unerwartete Hindernisbewegung und Kraftsprünge werden kontrolliert injiziert. Sicherheits- und Erfolgsmaße werden getrennt ausgewertet; bloßes Stillstehen ist keine erfolgreiche Aufgabenerfüllung.

Ergebnisse gelten ausschließlich für den spezifizierten Simulator, Controller und dessen Annahmen. Physische Robotik und klinische Sicherheit bleiben gesonderte Untersuchungen.

## 4. Trainierte Begriffe / Embeddings

Eine Trainingsstudie sollte erst nach belastbarer Messung des Vorteils gegenüber informationsgleichen natürlichen Regeln beginnen. Mindestkontrollen: natürliches Label, künstliches Label mit eingefrorenem Modell, trainiertes neues Embedding und identisches Trainingsbudget ohne neue Begriffe. Entwicklung und Test werden nach Aufgabenfamilien und mindestens einer Domäne getrennt.

Gemessen werden vollständige Task- und Invariantenerfüllung, Token-/Laufzeitkosten einschließlich Training sowie Robustheit gegenüber neuen Kombinationen. Vorhandene Arbeiten zum Neologism Learning sind die direkte Vergleichslinie. Die Annahme, ein einzelnes trainiertes Embedding garantiere physische Sicherheit, bleibt ohne nachgeschaltete Durchsetzung unbegründet.

## 5. Priorisierung

1. Messinstrument und Aussageumfang reparieren; den dokumentierten alten Stand als historischen Bericht erhalten.
2. Eine zentrale Frage wählen: menschliche Intentionserkennung oder methodischer Vorteil maschineller Konzeptsteuerung.
3. Nur für diese Frage ein kontrolliertes, unabhängigeres Folgeexperiment durchführen.
4. Embodiment und Training erst dann erweitern, wenn sie eine konkret offene Hypothese prüfen. Mehr Szenarien, Parameter oder Papertext allein beheben die aktuellen Validitätslücken nicht.
