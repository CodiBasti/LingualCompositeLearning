# Methodological & Architectural Decisions (MDR/ADR)

This document records pivotal methodological and architectural decision records for the research project.

---

## Overview

| ID | Date | Title | Status |
| :--- | :--- | :--- | :--- |
| **MDR-001** | Oct 31, 2026 | Decoupling In-Context Definitions from Continuous Representation Learning | Accepted |
| **MDR-002** | Oct 31, 2026 | Establishing `fufu` as Primary Pilot Concept Operator | Accepted |
| **MDR-003** | Oct 31, 2026 | Strict Boundary between Theoretical Hypotheses and Empirical Evidence | Accepted |
| **MDR-004** | Oct 31, 2026 | Three-Tier Evaluation Framework (Text Planning -> Simulation -> Physical HRI) | Accepted |
| **MDR-005** | Oct 31, 2026 | Whorfian Alignment: Structural Unconstructibility of Hazardous Action Trajectories | Accepted |
| **MDR-006** | Nov 01, 2026 | Cross-Domain Vulnerability Transfer as Core Architectural Paradigm | Accepted |
| **MDR-007** | Nov 06, 2026 | Empirical Pivot: Post-Mortem of In-Context Routing & Focus on Deep Latent Token Anchoring | Accepted |

---

## MDR-001: Decoupling In-Context Definitions from Continuous Representation Learning

- **Context:** Foundation models can acquire concept operators via two technical routes:
  1. *In-Context:* Instruction specifications in prompt headers or system context.
  2. *Representation Learning:* Training dedicated token embeddings (e.g. Hewitt et al. 2026) or LoRA adapters.
- **Decision:** Both routes are investigated across decoupled phases. First, establish a rigorous in-context benchmark baseline across large-scale scenarios (model-agnostic, zero-shot), followed by targeted continuous embedding tuning.
- **Consequences:** Clear comparative metrics; prevents conflating in-context prompt artifacts with intrinsic latent manifold geometry.

---

## MDR-002: Establishing `fufu` as Primary Pilot Concept Operator

- **Context:** An initial reference concept is required to validate evaluation harnesses and benchmark runner pipelines.
- **Decision:** Formalize `fufu` as the primary reference operator ([`dev/concepts/fufu.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/concepts/fufu.md)).
- **Semantic Core:** Prudent motion execution, continuous environmental observation, minimization of risk to biological and physical entities, and mandatory action abort upon unverified danger.
- **Consequences:** `fufu` serves as the anchor pilot benchmark across initial manipulation and navigation tasks.

---

## MDR-003: Strict Boundary between Theoretical Hypotheses and Empirical Evidence

- **Context:** LLM research frequently falls into the trap of declaring a well-crafted prompt as "language comprehension" without causal or physical validation.
- **Decision:** Claims are classified as "findings" only when corroborated by reproducible experimental logs in [`dev/findings/`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/findings). Prior to verification, statements remain indexed as open hypotheses in [`dev/HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md).
- **Consequences:** Guarantees peer-review scientific integrity and auditability.

---

## MDR-004: Three-Tier Evaluation Framework

- **Context:** Hardware deployment on physical robotic manipulators is resource-intensive and requires safe staging.
- **Decision:**
  1. *Tier 1:* Text-based symbolic action planning & invariant recall audits across open-weights LLMs.
  2. *Tier 2:* Physics simulation (PyBullet / Isaac Lab) with runtime safety-chip monitors.
  3. *Tier 3:* Human-Robot Interaction (HRI) human-subject studies assessing cognitive intention formation.
- **Consequences:** Early error isolation and rapid iteration cycles.

---

## MDR-005: Whorfian Alignment (Structural Unconstructibility of Hazardous States)

- **Context:** Traditional post-hoc alignment (RLHF, DPO, system prompts) operates purely probabilistically. The model retains full capability to formulate hazardous paths, merely penalizing them statistically. Under goal conflicts or adversarial urgency (*"Hurry!"*), probabilistic barriers routinely collapse.
- **Decision:** The project introduces *Whorfian Alignment*: by anchoring synthetic behavioral operators as discrete attractors in latent space, hazardous trajectories violating physical invariants are rendered structurally unconstructible in the planning graph. The robot does not require moralistic admonishment—it cannot formulate the colliding trajectory as a valid path.
- **Consequences:** Research prioritizes the mapping between perceptual context and autonomous invariant contract synthesis.

---

## MDR-006: Cross-Domain Vulnerability Transfer as Core Architectural Paradigm

- **Context:** Restricting benchmarks to a narrow niche (e.g. only domestic kitchens) undermines paper generalizability and invites criticism of ad-hoc over-fitting.
- **Decision:** The concept vocabulary is grounded in the universal intersection: **Vulnerable Co-Presence**. Operators encode universal laws of spatial standoff ($\mathcal{D}_{\text{space}}$), force limits ($\mathcal{D}_{\text{force}}$), and acoustic discretion ($\mathcal{D}_{\text{social}}$) that apply uniformly across Domestic environments, Clinical Geriatric Care, Precision Craft Labs, and Emergency Disaster response.
- **Consequences:** The principal scientific contribution is empirical demonstration of **Zero-Shot Cross-Domain Invariant Transfer**.

---

## MDR-007: Empirical Pivot: Post-Mortem of In-Context Routing & Focus on Deep Latent Token Anchoring

- **Context:** An independent adversarial Red-Team audit on Nov 05, 2026 ([`dev/reports/review_audit_2026-11-05_FULL_PROJECT.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/reports/review_audit_2026-11-05_FULL_PROJECT.md)) evaluated the codebase with 8 GPU hours of controls, ablations, blinded ratings, and evaluator probes. The audit exposed critical failure modes:
  1. *Evaluator Blindness (F1):* The regex checker approved dangerous violations (e.g., 0.2m passed a 1.5m clearance rule due to ungrounded keyword matching).
  2. *Token-Budget Confound (F5):* Verbose CoT suffered from output truncation at `max_new_tokens=300`, not mysterious cognitive "attention drift".
  3. *Lack of Latent Anchoring (F2):* In-context prompt-routing does not alter model representations; for a frozen instruct model, neologisms (`fufu`) are arbitrary tokens requiring verbose textual contracts, which plain structured natural English (`structured_direct`) outperformed (71.7% vs. 65.8%).
  4. *Grammar Implementation Defect (F3):* The Python synthesizer mapped `fufu-weli` and `weli-fufu` to identical sets, failing to enforce non-commutative syntax.
  5. *Sycophancy of Prior Reviews (F8):* Earlier reviews (8.2/10 and 8.5/10) praised conceptual narratives without validating executable code. The verified audit score is **2/10 (Strong Reject)**.
- **Decision:**
  1. *Transparent Open-Science Post-Mortem (Option A):* Fully retract claims of publication readiness for prompt-based routing. Document all negative findings, evaluator limits, and confounds openly in the repository and manuscript.
  2. *Re-centering on the Core Vision:* Pivot away from surface-level prompt engineering and human-subject questionnaires. Focus strictly on **Agent-to-Robot System Coordination**: *Can deeply anchored composite concept tokens (trained directly into model weights via PEFT/LoRA) enforce physical invariants more robustly and efficiently than verbose Chain-of-Thought?*
  3. *Phase 5 Advancement:* Implement authentic continuous token tuning (`<|c:fufu|>`, `<|c:weli|>`) with numerical constraint evaluation and unconstrained CoT baselines (1024 tokens).
- **Consequences:** Establishes uncompromising scientific credibility, eliminates sycophancy, and focuses engineering resources on genuine representation learning.
