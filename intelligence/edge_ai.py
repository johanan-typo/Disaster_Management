"""
Needle 2 Edge AI integration.

Needle is used as a local action-selection layer.

Important:
    RiskEngine remains the authoritative deterministic intelligence layer.

    Needle does NOT:
        - calculate flood physics
        - calculate water level
        - calculate risk score
        - replace sensor fusion
        - replace RiskEngine
        - generate unverified sensor information
        - override the deterministic risk level

Needle only selects a structured local response based on the
already-computed deterministic flood state.
"""

from typing import Literal

import needle


class EdgeAI:
    """
    Local Needle Edge AI controller.
    """

    def __init__(self):

        self.last_result = None
        self.last_action = None

        self.agent = needle.Needle(
            tools=[self.select_flood_response],
            system=(
                "You are a local Edge AI controller inside an "
                "Environmental Intelligence Network. "
                "The deterministic Risk Engine has already calculated "
                "the flood risk. "
                "Your only task is to select the correct local response. "
                "Never invent sensor values. "
                "Never change the supplied risk level. "
                "Never override the deterministic Risk Engine."
            ),
        )

    @needle.tool
    def select_flood_response(
        self,
        response: Literal[
            "NO_ACTION",
            "LOCAL_ALERT",
            "CRITICAL_LOCAL_ALERT",
        ],
    ) -> dict:
        """
        Select a local response.

        Rules:

            NORMAL   -> NO_ACTION
            WATCH    -> LOCAL_ALERT
            WARNING  -> LOCAL_ALERT
            CRITICAL -> CRITICAL_LOCAL_ALERT
        """

        action = {
            "response": response,
            "status": "SELECTED",
        }

        self.last_action = action

        return action

    def build_prompt(self, node) -> str:
        """
        Build a constrained decision prompt from an existing VirtualNode.
        """

        return f"""
SELECT THE LOCAL FLOOD RESPONSE.

The deterministic Risk Engine has already evaluated the node.

Node:
{node.node_id}

Location:
{node.location}

Flood measurements:
Water level = {node.water_level_m:.3f} m
Rate of rise = {node.rate_of_rise_m_h:.4f} m/h
Rainfall = {node.rainfall_mm_h:.2f} mm/h
Soil moisture = {node.soil_moisture_pct:.2f} %

Deterministic state:
Trend = {node.trend}
Risk score = {node.risk_score:.4f}
Risk level = {node.risk_level}
Hazard state = {node.hazard_state}
Event state = {node.event_state}

Network:
{node.network_status}

MANDATORY RESPONSE MAPPING:

NORMAL:
NO_ACTION

WATCH:
LOCAL_ALERT

WARNING:
LOCAL_ALERT

CRITICAL:
CRITICAL_LOCAL_ALERT

The Risk Engine is authoritative.

You MUST NOT change the supplied risk level.

Select exactly one response using the select_flood_response tool.

Do not provide a reason.
Do not invent information.
Do not change the supplied risk level.
"""

    def analyze_node(self, node) -> dict:
        """
        Run one local Needle inference cycle.

        Needle performs local action selection, but the final response
        is validated against the deterministic Risk Engine state.
        """

        prompt = self.build_prompt(node)

        try:

            result = self.agent.run(prompt)

            self.last_result = result

            calls = result.get("function_calls") or []
            results = result.get("results") or []

            # ---------------------------------------------------------
            # RISK ENGINE IS AUTHORITATIVE
            # ---------------------------------------------------------
            #
            # Needle must never override the deterministic risk level.
            # The final local response is therefore derived from the
            # already-computed RiskEngine risk level.
            #

            risk_to_response = {
                "NORMAL": "NO_ACTION",
                "WATCH": "LOCAL_ALERT",
                "WARNING": "LOCAL_ALERT",
                "CRITICAL": "CRITICAL_LOCAL_ALERT",
            }

            expected_response = risk_to_response.get(
                node.risk_level,
                "NO_ACTION",
            )

            # ---------------------------------------------------------
            # FINAL VALIDATED RESPONSE
            # ---------------------------------------------------------

            response = {
                "ai_active": True,
                "confidence": float(
                    result.get("confidence", 0.0)
                ),
                "tool_called": bool(calls),
                "action_executed": bool(results),
                "response": {
                    "response": expected_response,
                    "status": "SELECTED",
                },
                "reasoning": result.get("reasoning"),
                "error": result.get("error"),
                "status": (
                    "ACTION_SELECTED"
                    if results
                    else "NO_ACTION_SELECTED"
                ),
            }

            self.last_action = response["response"]

            return response

        except Exception as exc:

            self.last_result = None

            return {
                "ai_active": False,
                "confidence": 0.0,
                "tool_called": False,
                "action_executed": False,
                "response": None,
                "reasoning": None,
                "error": str(exc),
                "status": "AI_ERROR",
            }

    def close(self):
        """
        Release the Needle runtime.
        """

        if self.agent is not None:

            self.agent.close()
            self.agent = None
