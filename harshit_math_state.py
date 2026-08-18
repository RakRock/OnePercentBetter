"""Stateful error-catching engine for Harshit Math problems."""

from __future__ import annotations

import re
from typing import Any

import harshit_math_content as hmc


def _normalize(text: str) -> str:
    s = str(text).strip().lower()
    s = s.replace("−", "-").replace(" ", "")
    return s


def _build_fallback_machine(problem_id: str) -> dict | None:
    """Simple visual → confirm flow for days without a full error graph yet."""
    for day in hmc.list_days():
        prob = day.get("ncert_problem") or {}
        if prob.get("id") != problem_id:
            continue
        manip = day.get("manipulative", "interactive_number_line")
        final = str(prob.get("final_answer", ""))
        is_frac = manip == "fraction_block_grid"
        return {
            "problem_id": problem_id,
            "day": day["day"],
            "initial_node": "visual_start",
            "error_trap_index": {},
            "nodes": {
                "visual_start": {
                    "type": "visual_prompt",
                    "component": "FractionBlockGrid" if is_frac else "InteractiveNumberLine",
                    "prompt": prob.get("steps", ["Work through the problem step by step."])[0],
                    "config": {"min": -5, "max": 5, "target": 0, "tolerance": 1.0},
                    "transitions": {"visual_correct": {"to": "final_answer"}},
                },
                "final_answer": {
                    "type": "final_input",
                    "prompt": f"Final answer: {prob.get('statement', '')}",
                    "expected_patterns": [final] if final else [],
                    "expected_values": [final] if final else [],
                    "transitions": {
                        "match": {"to": "complete", "feedback": "Correct."},
                    },
                },
                "complete": {"type": "terminal", "prompt": "Complete.", "transitions": {}},
            },
        }
    return None


def _matches_patterns(value: str, patterns: list[str]) -> bool:
    norm = _normalize(value)
    for p in patterns:
        if _normalize(p) == norm:
            return True
    return False


def _matches_values(value: str, expected: list[Any]) -> bool:
    norm = _normalize(value)
    for exp in expected:
        if _normalize(str(exp)) == norm:
            return True
    return False


class ProblemStateMachine:
    """Runs a single problem through visual → intermediate → final nodes."""

    def __init__(self, problem_id: str):
        raw = hmc.get_state_machine(problem_id)
        if not raw:
            raw = _build_fallback_machine(problem_id)
        if not raw:
            raise ValueError(f"No state machine for {problem_id}")
        self.problem_id = problem_id
        self.meta = raw
        self.nodes = raw["nodes"]
        self.trap_index = raw.get("error_trap_index", {})
        self.current_node = raw["initial_node"]
        self.feedback: str | None = None

    def node(self) -> dict:
        return self.nodes[self.current_node]

    def is_complete(self) -> bool:
        return self.node().get("type") == "terminal"

    def requires_visual(self) -> bool:
        return self.node().get("type") == "visual_prompt"

    def validate_visual(
        self,
        value: float | None,
        *,
        interval: tuple[float, float] | None = None,
    ) -> tuple[bool, str | None, str | None]:
        """Return (ok, transition_key, feedback)."""
        node = self.node()
        cfg = node.get("config", {})
        transitions = node.get("transitions", {})

        if cfg.get("mode") == "interval_select" and interval is not None:
            lo, hi = interval
            expected = cfg.get("interval", [1, 2])
            if abs(lo - expected[0]) < 0.01 and abs(hi - expected[1]) < 0.01:
                t = transitions.get("interval_correct", {})
                return True, "interval_correct", t.get("feedback")
            if hi <= 0 or lo < 0:
                t = transitions.get("wrong_side_of_zero", {})
                return False, "wrong_side_of_zero", t.get("feedback")
            if hi <= 1:
                t = transitions.get("interval_too_low", {})
                return False, "interval_too_low", t.get("feedback")
            if lo >= 2:
                t = transitions.get("interval_too_high", transitions.get("plot_beyond_two", {}))
                return False, "interval_too_high", t.get("feedback")
            return False, "interval_too_low", transitions.get("interval_too_low", {}).get("feedback")

        if value is None:
            return False, None, "Place a marker on the number line."

        target = cfg.get("target")
        if target is None:
            return True, "visual_correct", None

        tolerance = float(cfg.get("tolerance", 0.25))
        diff = abs(float(value) - float(target))

        if diff <= tolerance:
            t = transitions.get("visual_correct", {})
            return True, "visual_correct", t.get("feedback")

        if target < 0 and value > 0:
            return False, "visual_wrong_side", transitions.get("visual_wrong_side", {}).get("feedback")
        if target > 0 and value < 0:
            return False, "visual_wrong_sign", transitions.get("visual_wrong_sign", {}).get("feedback")
        if target == -5 and value == -3:
            return False, "visual_wrong_magnitude", transitions.get("visual_wrong_magnitude", {}).get("feedback")
        if target == 1.414 and value <= 1:
            return False, "plot_left_of_one", transitions.get("plot_left_of_one", {}).get("feedback")
        if target == 1.414 and value >= 2:
            key = "plot_at_two" if value == 2 else "plot_beyond_two"
            return False, key, transitions.get(key, {}).get("feedback")

        return False, "visual_wrong_magnitude", transitions.get("visual_wrong_magnitude", {}).get("feedback")

    def validate_input(self, user_input: str) -> tuple[bool, str | None]:
        """Validate intermediate/final text input. Returns (ok, feedback)."""
        node = self.node()
        ntype = node.get("type")
        if ntype not in ("intermediate_input", "final_input"):
            return False, "This step expects a visual interaction first."

        raw = str(user_input).strip()
        trap_key = self.trap_index.get(raw) or self.trap_index.get(_normalize(raw))
        transitions = node.get("transitions", {})

        if trap_key and trap_key in transitions:
            t = transitions[trap_key]
            self._apply_transition(t)
            return False, t.get("feedback")

        if "expected_patterns" in node:
            if _matches_patterns(raw, node["expected_patterns"]):
                t = transitions.get("match", {})
                self._apply_transition(t)
                return True, t.get("feedback")
            for key in ("dropped_negative", "added_instead", "wrong_order", "said_yes", "said_rational"):
                if key in transitions:
                    t = transitions[key]
                    self._apply_transition(t)
                    return False, t.get("feedback")
            return False, "Check the signs and try rewriting the expression."

        if "expected_values" in node:
            if _matches_values(raw, node["expected_values"]):
                t = transitions.get("match", {})
                self._apply_transition(t)
                return True, t.get("feedback")
            for key, t in transitions.items():
                if key == "match":
                    continue
                if key in (
                    "subtract_instead_of_add",
                    "sign_error_positive",
                    "off_by_one",
                    "picked_15",
                    "picked_1",
                    "classic_minus_trap",
                    "positive_two",
                ):
                    self._apply_transition(t)
                    return False, t.get("feedback")
            return False, "Take another look at the number line and try again."

        return False, "Please enter your answer."

    def _apply_transition(self, transition: dict) -> None:
        to_node = transition.get("to")
        if to_node:
            self.current_node = to_node
        reroute = transition.get("reroute_node")
        if reroute:
            self.current_node = reroute
        self.feedback = transition.get("feedback")

    def advance_after_visual(self, transition_key: str = "visual_correct") -> None:
        node = self.node()
        t = node.get("transitions", {}).get(transition_key, {})
        self._apply_transition(t)

    def to_dict(self) -> dict:
        return {"current_node": self.current_node, "problem_id": self.problem_id}

    @classmethod
    def from_dict(cls, problem_id: str, data: dict) -> "ProblemStateMachine":
        sm = cls(problem_id)
        sm.current_node = data.get("current_node", sm.current_node)
        return sm
