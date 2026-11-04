# Open Research & Guiding Questions

This document records the foundational research questions governing experimental design and theoretical inquiry.

---

## 1. Human Cognitive & Intention Formation Effects
- **Q1.1:** Does acquiring a formal concept operator such as `fufu` enhance the human operator's capacity to recognize safety conditions *proactively* (during intention formation), or does it merely compress instructions that were already consciously recognized?
- **Q1.2:** What is the cognitive acquisition burden for human operators learning a multi-concept synthetic vocabulary?
- **Q1.3:** How robust is concept retention across extended temporal horizons without decay?

---

## 2. Machine Grounding & Model Architecture
- **Q2.1:** Is in-context specification in prompt headers sufficient, or does continuous representation learning (neologism embeddings, soft prompting, LoRA) provide demonstrable generalizability gains?
- **Q2.2:** Do foundation models exhibit "Attention Drift" and unfaithful lip-service under in-context prompts, whereas dedicated latent embeddings establish stable manifold attractors? *(Empirically confirmed: Attention Drift documented in EXP-001/002/003).*
- **Q2.3:** Can the model faithfully verbalize the precise physical invariants and execution bounds governing its behavior upon human query (Self-Verbalization)?

---

## 3. Morphology, Semiotics & Vocabulary Architecture
- **Q3.1:** Which token representation format exhibits the optimal balance of parsimony and stability?
  - *Synthetic CVCV Neologisms* (e.g., `fufu`, `weli`): Eliminate colloquial semantic noise and prior bias.
  - *Transparent Natural Compounds* (e.g., `caution-stop`): Intuitive for humans, but trigger noisy pre-training priors.
  - *Dedicated Latent Embeddings* (e.g., `<|c_fufu|>`): Unambiguous, zero-prompt compute overhead.
- **Q3.2:** What is the optimal granularity of the vocabulary? (Monolithic roles vs. hierarchical atomic morphemes; answered via 3-tier ontological hierarchy).

---

## 4. Boundaries, Goal Conflicts & Superficial Alignment
- **Q4.1:** At what threshold does an operator become overloaded, triggering unexpected hallucinations or behavioral paralysis (perpetual aborts / overcompliance)?
- **Q4.2:** How does the agent resolve direct semantic contradictions (e.g., clearance caution `fufu` combined with aggressive user urgency *"Hurry up!"*)? *(Resolved via lexicographic dominance: $\mathcal{D}_{\text{risk}} \succ \mathcal{D}_{\text{time}}$).*
- **Q4.3:** How do humans and autonomous systems detect and calibrate mutual semantic drift?

---

## 5. Formal Verification & Physical Runtime Monitors
- **Q5.1:** Which components of a behavioral concept map directly into temporal logic (LTL) and Control Barrier Functions (CBFs)?
- **Q5.2:** How does the framework handle epistemic uncertainty and sensory occlusion? (Resolved via the Freeze Axiom in $\mathcal{D}_{\text{risk}}$).
- **Q5.3:** Can concepts function as modular runtime safety arbiters between high-level foundation planners and low-level torque/impedance controllers?
