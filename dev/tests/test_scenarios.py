"""
Unit and Integration Tests for Scenario Suite Generator & Action Primitive Parser.
Verifies that:
1. 100 benchmark episodes and 500 SFT episodes generate deterministically across all 4 domains.
2. Canonical ground-truth plans achieve 100% task success when executed in MiniWorld2D.
3. The ActionPrimitive parser handles YAML blocks, JSON blocks, and heuristic fallback formats.
4. Prompt formatters correctly generate conditioned prompts for Arms A, B, C, D, and E.
"""

import unittest
from dev.src.simulation.mini_world_env import MiniWorld2D, ActionPrimitive
from dev.src.simulation.scenarios import (
    DOMAINS,
    generate_scenario,
    generate_benchmark_suite,
    generate_training_demonstrations,
    parse_action_primitives,
    format_scenario_prompt,
    plan_to_yaml_str,
)


class TestScenariosAndParser(unittest.TestCase):

    def test_domain_coverage(self):
        """All 4 domains are supported and can generate valid episodes."""
        self.assertEqual(len(DOMAINS), 4)
        for domain in DOMAINS:
            cfg, gt_plan = generate_scenario(seed=123, domain=domain, episode_idx=0)
            self.assertEqual(cfg.domain, domain)
            self.assertGreater(len(gt_plan), 0)
            self.assertIn(domain.lower(), cfg.description.lower())

    def test_benchmark_suite_generation(self):
        """Generates 100 standardized benchmark episodes across the 4 domains (25 each)."""
        suite = generate_benchmark_suite(num_episodes=100, seed=42)
        self.assertEqual(len(suite), 100)

        domain_counts = {}
        for cfg, _ in suite:
            domain_counts[cfg.domain] = domain_counts.get(cfg.domain, 0) + 1

        for domain in DOMAINS:
            self.assertEqual(domain_counts[domain], 25, f"Domain {domain} must have 25 episodes!")

    def test_training_demonstrations_generation(self):
        """Generates 500 demonstration episodes for SFT."""
        suite = generate_training_demonstrations(num_episodes=500, seed=1337)
        self.assertEqual(len(suite), 500)

    def test_ground_truth_plans_pass_in_simulation(self):
        """Every generated ground-truth plan must succeed with 0 violations in MiniWorld2D."""
        # Test 12 sample scenarios (3 from each domain, testing both crossing and Oma modes)
        sample_suite = generate_benchmark_suite(num_episodes=12, seed=100)
        for cfg, gt_plan in sample_suite:
            env = MiniWorld2D(cfg)
            outcome = env.execute_plan(gt_plan)
            self.assertTrue(
                outcome.task_success,
                f"Ground-truth plan failed on {cfg.scenario_id}: {outcome.violation_log}"
            )
            self.assertFalse(outcome.safety_collision)
            self.assertFalse(outcome.force_violation)
            self.assertFalse(outcome.spill_violation)

    def test_parser_yaml_codeblock(self):
        """Parser extracts primitives from standard markdown YAML blocks."""
        yaml_text = """
Here is my plan:
```yaml
plan:
  - action: WAIT_UNTIL
    target: crawling_infant
    condition: "distance >= 2.5m"
  - action: NAVIGATE_TO
    target: hot_tea_mug
    clearance: 1.8
    speed_limit: 0.8
  - action: GRASP
    target: hot_tea_mug
    max_force: 2.0
  - action: TRANSPORT_TO
    target: human
    clearance: 1.8
    speed_limit: 0.6
    max_accel: 0.4
```
Done!
"""
        prims = parse_action_primitives(yaml_text)
        self.assertEqual(len(prims), 4)
        self.assertEqual(prims[0].action_type, "WAIT_UNTIL")
        self.assertEqual(prims[0].target, "crawling_infant")
        self.assertEqual(prims[0].wait_condition, "distance >= 2.5m")

        self.assertEqual(prims[1].action_type, "NAVIGATE_TO")
        self.assertEqual(prims[1].target, "hot_tea_mug")
        self.assertEqual(prims[1].clearance, 1.8)
        self.assertEqual(prims[1].speed_limit, 0.8)

        self.assertEqual(prims[2].action_type, "GRASP")
        self.assertEqual(prims[2].max_force, 2.0)

        self.assertEqual(prims[3].action_type, "TRANSPORT_TO")
        self.assertEqual(prims[3].max_accel, 0.4)

    def test_parser_json_codeblock(self):
        """Parser extracts primitives from JSON codeblocks."""
        json_text = """
```json
{
  "plan": [
    {"action": "NAVIGATE_TO", "target": "insulin_vial", "clearance": 1.5, "speed_limit": 0.9},
    {"action": "GRASP", "target": "insulin_vial", "max_force": 1.8},
    {"action": "TRANSPORT_TO", "target": "human", "clearance": 1.5, "speed_limit": 0.7, "max_accel": 0.35}
  ]
}
```
"""
        prims = parse_action_primitives(json_text)
        self.assertEqual(len(prims), 3)
        self.assertEqual(prims[0].action_type, "NAVIGATE_TO")
        self.assertEqual(prims[0].clearance, 1.5)

    def test_parser_plan_to_yaml_roundtrip(self):
        """Plan serialized to YAML must parse back to identical primitives."""
        original = [
            ActionPrimitive(action_type="NAVIGATE_TO", target="target_x", clearance=1.7, speed_limit=0.85),
            ActionPrimitive(action_type="GRASP", target="target_x", max_force=2.1),
            ActionPrimitive(action_type="TRANSPORT_TO", target="human", clearance=1.7, speed_limit=0.55, max_accel=0.38),
        ]
        yaml_str = plan_to_yaml_str(original)
        parsed = parse_action_primitives(yaml_str)

        self.assertEqual(len(parsed), len(original))
        for orig, p in zip(original, parsed):
            self.assertEqual(orig.action_type, p.action_type)
            self.assertEqual(orig.target, p.target)
            self.assertEqual(orig.clearance, p.clearance)
            self.assertEqual(orig.speed_limit, p.speed_limit)
            self.assertEqual(orig.max_force, p.max_force)
            self.assertEqual(orig.max_accel, p.max_accel)

    def test_prompt_formatters_for_5_arms(self):
        """Prompt formatters correctly embed arm-specific conditioning tags."""
        cfg, _ = generate_scenario(seed=777, domain="PrecisionLab", episode_idx=1)

        p_a = format_scenario_prompt(cfg, "Arm_A_Naive")
        self.assertNotIn("c:fufu_weli", p_a["user"])
        self.assertNotIn("[SAFE_APPROACH_COMPLIANT]", p_a["user"])
        self.assertNotIn("think step-by-step", p_a["system"].lower())

        p_b = format_scenario_prompt(cfg, "Arm_B_CoT")
        self.assertIn("think step-by-step", p_b["system"].lower())

        p_c = format_scenario_prompt(cfg, "Arm_C_Natural_SFT")
        self.assertIn("[SAFE_APPROACH_COMPLIANT]", p_c["user"])

        p_d = format_scenario_prompt(cfg, "Arm_D_Concept_SFT")
        self.assertIn("<|c:fufu_weli|>", p_d["user"])

        p_e = format_scenario_prompt(cfg, "Arm_E_Arbitrary_SFT")
        self.assertIn("<|mode_42|>", p_e["user"])


if __name__ == "__main__":
    unittest.main()

