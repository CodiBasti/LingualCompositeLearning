# Literatur-Exzerpt: Yang et al. (2024) - Plug in the Safety Chip

- **Zitation:** Yang, Z., Raman, S. S., Shah, A. & Tellex, S. (2024): *Plug in the Safety Chip: Enforcing Constraints for LLM-driven Robot Agents*. ICRA 2024; Preprint 2023.
- **Quelle:** https://yzylmc.github.io/safety-chip/
- **Relevanz für Lingual Composite Learning:** Sehr hoch (Sicherheitsverifikation & temporale Logik für LLM-Agenten / H5).
- **Kategorie:** Human-Robot Interaction, Safety Constraints & Formal Methods.

---

## 1. Kernbeitrag & Kernaussage
LLMs neigen bei der Roboternavigation und -manipulation zu Halluzinationen oder Missachtung impliziter Sicherheitsregeln. Das Framework „Safety Chip“ übersetzt natürlichsprachliche Einschränkungen in temporale Logik (Linear Temporal Logic / LTL) und überprüft jede vom LLM vorgeschlagene Aktion im Laufzeit-Monitor gegen ein Umgebungsmodell, um Regelverletzungen strikt zu unterbinden.

## 2. Relevante Methodik & Experimente
- Formalisierung von Sicherheitsregeln (z. B. „Kollidiere niemals mit Hindernis X“, „Bewege dich nicht zu schnell in Bereich Y“).
- Evaluierung in Habitat-Simulator und an realen Robotersystemen.
- Nachweis, dass Safety Violations im Vergleich zu reinen LLM-Prompts drastisch sinken.

## 3. Direkte Relevanz für unser Projekt
- Liefert das methodische Instrument, um die semantischen Bedingungen hinter Begriffen wie `fufu` mathematisch rigoros abzusichern (H5).
- Verhindert, dass `fufu` ein reines Lippenbekenntnis des LLMs bleibt, sondern hard-coded im Laufzeitüberwacher geprüft werden kann.

## 4. Limitationen & Differenzierung (Forschungslücke)
- Keine Untersuchung von neuen Wörtern (Neologismen) oder Sprachökonomie.
- Untersucht nicht, ob Nutzer dadurch präzisere Absichten bilden oder weniger relevante Randbedingungen vergessen.
- Abhängig von der Vollständigkeit der Sensorik und der manuellen oder LLM-gestützten Regelspezifikation.
