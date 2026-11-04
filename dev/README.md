# Lingual Composite Learning: Scalable Concept Language for Humans, AI, and Robots

> **Research Initiative** investigating a shared vocabulary of discrete semantic operators (e.g. synthetic neologisms such as `fufu`) that serve as precise behavioral specifications, sharpen human intention formation, and guarantee safe physical robot execution.

---

## 🎯 Core Vision & Foundational Concept

Natural language is inherently polysemous and often requires repetitive, lengthy descriptions to capture subtle behavioral nuances, safety envelopes, and environmental constraints. When a distinction is absent from an operator's active vocabulary, it is frequently omitted during **initial intention formation**—well before prompt drafting.

This research project investigates:
1. **Human Cognitive Utility:** Does acquiring formal concept operators (neologisms/symbols) enable humans to remember constraints more reliably and formulate instructions with greater precision?
2. **Machine Grounding & Generalization:** Can autonomous AI and robotic systems acquire these concepts (in-context or via representation learning / soft embeddings) and transfer them reliably across novel domains?
3. **Compositionality & Formal Verification:** Can operators be combined sequentially or hierarchically with verifiable adherence to temporal safety constraints?

Reference Briefing Document: [`dev/ref/Briefing_Begriffssprache_Mensch_KI.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/ref/Briefing_Begriffssprache_Mensch_KI.md).

---

## 🧭 Repository Navigation

| Directory / File | Scope & Contents |
| :--- | :--- |
| [`STATE.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/STATE.md) | **Single Source of Truth** for current progress, active phase, and immediate milestones. |
| [`RESEARCH_MAP.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/RESEARCH_MAP.md) | Phased research roadmap spanning theoretical foundations to embodied robotics. |
| [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) | Structured hypotheses (H1–H5), falsification criteria, and empirical evidence. |
| [`QUESTIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/QUESTIONS.md) | Guiding scientific and operational research questions. |
| [`DECISIONS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/DECISIONS.md) | Architectural & Methodological Decision Records (MDRs/ADRs). |
| [`BACKLOG.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/BACKLOG.md) | Work packages, pending milestones, and task backlog. |
| [`IDEAS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/IDEAS.md) | Raw research ideas, extensions, and theoretical notes. |
| [`AGENTS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/AGENTS.md) | Operational guidelines and guardrails for autonomous AI research agents. |
| [`concepts/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts) | Formal concept specifications (e.g., [`concepts/fufu.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/fufu.md)). |
| [`data/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/data) | Test scenarios, adversarial prompts, and benchmark suites. |
| [`experiments/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/experiments) | Experimental designs, protocols, and test setups. |
| [`findings/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/findings) | Consolidated, peer-reviewed empirical findings. |
| [`literature/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/literature) | Literature notes, audits, and comparative matrices. |
| [`papers/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/papers) | Research manuscripts, LaTeX sources, and camera-ready papers. |
| [`ref/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/ref) | Original vision briefing and historical references. |
| [`reports/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/reports) | Adversarial peer review audits and evaluation reports. |
| [`runs/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/runs) | Raw execution traces, model outputs, and evaluation checkpoints. |
| [`src/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/src) | Reusable Python source code (runners, evaluators, dashboards). |
| [`templates/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/templates) | Standardized markdown templates for experiments, concepts, and literature. |

---

## ⚡ Quickstart for Researchers & Autonomous Agents

1. Consult [`STATE.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/STATE.md) for the active research focus.
2. Review guidelines in [`AGENTS.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/AGENTS.md).
3. Adhere to the empirical method: every scientific claim must reference a hypothesis in [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) backed by reproducible experiment logs in [`runs/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/runs).
