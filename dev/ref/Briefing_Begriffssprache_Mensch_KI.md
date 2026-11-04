# Research Briefing: An Extensible Concept Language for Humans, AI, and Robots

- **Author / Initiator:** Sebastian Oertel  
- **Date:** October 31, 2026  
- **Purpose:** Summary of the foundational vision, guiding research questions, and prior art. Theoretical hypotheses and empirically validated findings are strictly delineated.

---

## 1. Foundational Premise

- Language shapes which distinctions humans routinely recognize, incorporate, and communicate to an autonomous AI agent.
- The initial question examined whether specific linguistic differentiations could provide practical utility in an AI-centric world.
- The crucial insight concerns **intention formation prior to formulation**: if an operator lacks a distinction in their active conceptual repertoire, they will often fail to recognize the necessity of specifying it in an instruction.
- The counter-argument—that any nuance can simply be paraphrased in natural language—is incomplete: formulating a suitable paraphrase presupposes that the user has already recognized the relevant distinction.
- Rather than relying on accidental natural language peculiarities, the progressive approach deliberately synthesizes grounded concept operators that can be acquired across speakers of any native language.

---

## 2. The Core Concept

- Dedicated tokens, symbols, or defined compound expressions denote reusable behavioral concepts.
- Humans and AI/robotic systems acquire shared, aligned semantics for these concepts.
- An operator bundles multiple physical invariants and can be appended seamlessly to standard task instructions.
- The semantics must be cross-domain transferable: the same concept alters task execution appropriately depending on situational context.
- Implementation strategies range from in-context specifications to representation learning of dedicated token embeddings. These variants must be evaluated systematically regarding robustness and generalizability.

---

## 3. The Pilot Example "fufu"

- **Instruction:** "Go to the door and open it, fufu."
- **Intended Meaning:** "Observe your immediate surroundings. Harm no persons. Act with prudence without endangering the door, the environment, or bystanders. If execution entails unavoidable risk of harm, suspend action."
- **Function:** "fufu" denotes a cross-task synthesis of spatial vigilance, speed derating, and fail-safe stop-on-risk invariants.
- **Cross-Domain Transfer:** For a swing door, swing clearance and pedestrian occlusion are critical; for a fragile vase, tactile grip force and planar stability; for payload transport, a clear corridor and dynamic center of mass.
- **Operational Questions:** What risk thresholds are acceptable? When must the system freeze or query oversight? A definition alone guarantees neither omniscient perception nor flawless execution.

---

## 4. Vision

- A mutually acquired, extensible concept language supplements natural language with precise behavioral operators.
- Users specify complex constraints with minimal recurring cognitive and descriptive effort.
- By acquiring such concepts, humans proactively incorporate constraints that might otherwise have been omitted during intention formation.
- Embodied AI systems transfer known physical invariants to novel tasks and explain their actions deterministically on demand.
- In the long term, concepts can be shared across agents and human operators, provided semantics and behaviors remain verified.
- The vision unifies **sharper human intention formation**, **communicative efficiency**, and **guaranteed machine execution safety**.

---

## 5. Core Research Hypotheses

- **Conceptual Utility:** Learning a named concept facilitates human retention and proactive consideration of safety conditions.
- **Communicative Efficiency:** A shared concept reduces omissions and misunderstandings relative to unconstrained free-text prompts.
- **Cross-Domain Generalization:** Humans and machines transfer the concept to situations unobserved during training.
- **Compositionality:** Concepts combine sequentially and hierarchically; domain boundaries and conflict algebras are preserved.
- **Mutual Semantic Alignment:** Humans and machines share consistent behavioral expectations, eliminating superficial or unfaithful alignment.

---

## 6. Research Directions & Critical Open Questions

- **Interdisciplinary Nexus:** Neologism Learning, Human-AI Communication, Concept Learning, Human-Robot Interaction, and Formal Safety Verification.
- **Guiding Question:** Does an acquired shared vocabulary improve human capability to recognize safety conditions independently and communicate them effectively to an embodied agent?
- **Human Effects:** Does a concept merely shorten prompt length, or does it genuinely improve the completeness and depth of human intention formation?
- **Machine Effects:** Is an in-context definition sufficient, or does continuous embedding representation learning improve cross-domain transfer?
- **Token Design:** How do synthetic neologisms, natural words, transparent compounds, and latent embeddings compare?
- **Boundaries:** At what point do concepts become overly complex? How are direct goal conflicts resolved?
- **Verification:** Which components of an operator can be formalized into observable invariants and runtime monitors?

---

## 7. Relevant Prior Art

1. **Hewitt, J., Geirhos, R. & Kim, B. (2025): _Position: We Can’t Understand AI Using our Existing Vocabulary_. ICML 2025.**
   - Proposed expanding human-machine vocabulary through novel words to communicate concepts and steer model behaviors with higher precision.
   - Initial demonstrations steering generation length and lexical diversity.
   - *Relation:* Direct theoretical justification for reusable control tokens.
   - *Limitation:* Position paper with text-only demonstrations; no physical embodiment or safety invariants.

2. **Hewitt, J., Tafjord, O., Geirhos, R. & Kim, B. (2026): _Neologism Learning for Controllability and Self-Verbalization_. ICLR 2026; Preprint 2025.**
   - Introduces novel vocabulary by training dedicated token embeddings on few-shot examples while freezing all base model weights.
   - Evaluates steering and linguistic self-verbalization of acquired meanings.
   - *Relation:* Technical blueprint for representation learning of concept tokens.
   - *Limitation:* No physical robotics control or temporal safety verification.

3. **Lupyan, G., Rakison, D. H. & McClelland, J. L. (2007): _Language Is Not Just for Talking: Redundant Labels Facilitate Learning of Novel Categories_. Psychological Science.**
   - Redundant category labels significantly facilitated human acquisition and retention of novel categories.
   - *Relation:* Empirical evidence for human cognitive benefits during concept acquisition.
   - *Limitation:* Focused on static visual categorization rather than dynamic sequential planning.

4. **Yang, Z., Raman, S. S., Shah, A. & Tellex, S. (2024): _Plug in the Safety Chip: Enforcing Constraints for LLM-driven Robot Agents_. ICRA 2024; Preprint 2023.**
   - Translates natural language constraints into Linear Temporal Logic (LTL) and verifies proposed robot actions against an environmental world model.
   - *Relation:* Demonstrates formal verification of constraints underlying operators like `fufu`.
   - *Limitation:* No synthetic vocabulary or token compression; dependent upon manual rule specification.

---

## 8. Positioning of the Research Contribution

- While individual facets (neologism steering, LTL safety chips, label learning) exist in isolation, the core contribution of this project lies in their complete closed-loop synthesis:
- **Humans form sharper intentions $\leftrightarrow$ Embodied agents bind discrete concept operators $\leftrightarrow$ Invariants transfer zero-shot across physical domains $\leftrightarrow$ Temporal safety contracts are deterministically enforced.**
