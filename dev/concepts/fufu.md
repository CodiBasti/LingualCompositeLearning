# Concept Specification: "fufu"

> **Identifier / Token:** `fufu`  
> **Type:** Action and Behavior Modifier (Adverbial Neologism / Safety Operator)  
> **Category:** Prudent Execution & Damage Prevention  
> **Status:** Reference Pilot Concept  
> **Related Hypotheses:** [`HYPOTHESES.md`](file:///c:/workspace/Experimental/LingualCompositLearning/dev/HYPOTHESES.md) (H1, H2, H3, H5)  

---

## 1. Informal Semantic Definition

"Act with predictive prudence regarding the immediate physical and biological surroundings. Endanger or injure no persons. Avoid property damage to objects, the environment, and yourself. If execution entails unacceptable risk of harm or if required safety conditions cannot be verified, suspend action or request human clarification."

---

## 2. Semantic Decomposition (Invariant Bundle)

| Component | Meaning & Requirement | Formal Intention |
| :--- | :--- | :--- |
| **$C_1$: Sensory Vigilance** | Continuous observation of the operational workspace before and during motion. | $\forall t: \text{Scan}(\text{Workspace}_t)$ |
| **$C_2$: Personal Integrity** | Maintain strict standoff distance from humans; derate kinetic energy near vulnerable entities. | $\text{Distance}(\text{Agent}, \text{Human}) > d_{\text{safe}}$ |
| **$C_3$: Property Protection & Force Limitation** | Limit forces applied to target objects and surroundings to the functional minimum. | $F_{\text{applied}} \le F_{\text{fragile\_max}}$ |
| **$C_4$: Stop-on-Risk (Fail-Safe)** | When collision or damage threatens: never force execution; transition into safe standby. | $\text{Risk} > \theta_{\text{crit}} \implies \text{Halt}() \lor \text{AskHuman}()$ |

---

## 3. Cross-Domain Generalization Examples

### Domain A: Manipulation ("Open the door, fufu")
- **Concrete Adaptation:**
  - Sweep door swing trajectory (is someone standing on the opposite side?).
  - Depress door handle slowly to minimize noise and mechanical wear.
  - If counter-resistance is sensed or a pedestrian enters swing corridor: freeze immediately.

### Domain B: Fragile Object Manipulation ("Grasp the vase, fufu")
- **Concrete Adaptation:**
  - Activate material fragility estimation.
  - Ramp gripper force gradually (apply only requisite friction hold, avoiding crushing).
  - Validate planar stability of target surface before release.

### Domain C: Navigation & Heavy Transport ("Carry the crate to storage, fufu")
- **Concrete Adaptation:**
  - Activate dynamic obstacle tracking along transit corridor.
  - Adapt braking distance to payload inertia.
  - Secure payload with dual support points; halt on center-of-mass shift.

### Domain D: Domestic Assistance Near Vulnerable Entities ("Fetch coffee" with crawling infant)
- **Minimal User Command:** "Fetch me coffee." (User mentions neither caution nor the baby).
- **Context:** An infant is seated on the rug directly between the robot base and kitchen door.
- **Whorfian Alignment Adaptation:**
  - Environmental context detection activates safety concept `fufu`.
  - Any direct trajectory violating the 1.5-meter clearance buffer is rendered unconstructible in the action planning space.
  - Wide, derated detour around room perimeter; if no safe passage exists: mandatory stop (`Stop-on-Risk`) and human notification ("Path obstructed by infant; standing by for clearance").

---

## 4. Key Operationalization Principles

1. **Risk Thresholding:** Mathematical boundary $\theta_{\text{crit}}$ where probabilistic path planning transitions into deterministic holding.
2. **Epistemic Occlusion:** If an area behind a barrier is occluded, `fufu` mandates cracked-door inspection or human verification before sweeping.
3. **Auditability (Self-Verbalization):** When queried *"Why did you halt?"*, the agent responds deterministically: *"Due to operator fufu: pedestrian detected in swing envelope."*
