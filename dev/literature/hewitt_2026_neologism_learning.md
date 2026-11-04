# Literatur-Exzerpt: Hewitt et al. (2026) - Neologism Learning for Controllability and Self-Verbalization

- **Zitation:** Hewitt, J., Tafjord, O., Geirhos, R. & Kim, B. (2026): *Neologism Learning for Controllability and Self-Verbalization*. ICLR 2026; Preprint 2025.
- **Quelle:** https://arxiv.org/abs/2510.08506 | https://proceedings.iclr.cc/paper_files/paper/2026/hash/90463e84605a7ac8d45cdd334cd93316-Abstract-Conference.html
- **Relevanz für Lingual Composite Learning:** Extrem hoch (Technischer State-of-the-Art für Neologismen-Training).
- **Kategorie:** Representation Learning & Soft Prompts.

---

## 1. Kernbeitrag & Kernaussage
Neue Wörter werden in ein bestehendes LLM eingeführt, indem ausschließlich neue Token-Embeddings anhand von wenigen Beispielen trainiert werden, während sämtliche übrigen Modellgewichte eingefroren bleiben. Diese Neologismen erlauben sowohl Verhaltenssteuerung als auch sprachliche Selbst-Erklärung (Self-Verbalization) der erlernten Wortbedeutung durch das Modell.

## 2. Relevante Methodik & Experimente
- Training neuer Embedding-Vektoren für Neologismen.
- Steuerung komplexerer Verhaltensmuster (z. B. Schmeichelei, Tonalität, Antwortlänge).
- Evaluation, ob das Modell auf Aufforderung die Bedeutung des Wortes korrekt in natürlicher Sprache paraphrasieren kann.

## 3. Direkte Relevanz für unser Projekt
- Liefert das konkrete technische Blueprint für Phase 3 unseres Projekts: Ein neues Wort (z. B. `fufu`) kann als Token im Vokabular verankert werden, ohne das gesamte Modell finetunen zu müssen.
- Self-Verbalization ist ein Schlüsselmechanismus, um Scheinverständnis aufzudecken.

## 4. Limitationen & Differenzierung (Forschungslücke)
- Keine Anwendung auf physische Agenten, Robotik-Simulationen oder temporale Sicherheitsregeln.
- Kein Nachweis, ob menschliche Nutzer durch solche Begriffe kognitiv profitieren (Absichtsbildung).
