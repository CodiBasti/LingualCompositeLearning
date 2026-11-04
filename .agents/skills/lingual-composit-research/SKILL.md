---
name: lingual-composit-research
description: Guidelines and workflows for autonomous research in Lingual Composite Learning (extensible concept language for humans, AI, and robots).
---

# Skill: Lingual Composite Research

This skill instructs AI agents and researchers in conducting structured, scientifically rigorous research within the **Lingual Composite Learning** initiative.

## Core Principles

1. **Evidence-Based Assertions:** Claims are marked as verified only when backed by reproducible empirical data.
2. **Concept Precision:** Novel concepts (e.g., `fufu`) must be decomposed into formal contracts (pre-conditions, post-conditions, physical invariants).
3. **Documentation Currency:** Every significant progress step immediately updates the central tracking files (`STATE.md`, `HYPOTHESES.md`, `BACKLOG.md`).

## Standard Workflows

### 1. Specifying a New Concept
- Create file under `dev/concepts/<concept_name>.md` following `dev/templates/concept_template.md`.
- Decompose definition into atomic semantic invariants across 5 dimensions.
- Formulate at least 2 cross-domain transfer tasks.
- Specify epistemic halting thresholds and fail-safe stop conditions.

### 2. Setting up an Experiment
- Create dedicated directory: `dev/experiments/EXP-<Number>_<name>/`.
- Instantiate `README.md` from `dev/templates/experiment_template.md`.
- Link investigated hypotheses from `dev/HYPOTHESES.md`.
- Upon completion: write execution report and update `HYPOTHESES.md` and `STATE.md`.

### 3. Analyzing Literature
- Add notes under `dev/literature/<author>_<year>_<short_title>.md` following `dev/templates/literature_note_template.md`.
- Explicitly emphasize differentiation and research gaps relative to our contribution.
