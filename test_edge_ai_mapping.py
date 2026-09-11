"""
Edge AI Response Mapping Test
=============================

Verifies that the deterministic risk level and
Needle Edge AI response are consistent.

Expected mapping:

NORMAL   -> NO_ACTION
WATCH    -> LOCAL_ALERT
WARNING  -> LOCAL_ALERT
CRITICAL -> CRITICAL_LOCAL_ALERT
"""

from engines.node_model import VirtualNode
from intelligence.edge_ai import EdgeAI


def create_node(risk_level):

    node = VirtualNode(
        node_id="TEST",
        location="Test Location",
        water_level_m=1.0,
    )

    node.rainfall_mm_h = 80.0
    node.rate_of_rise_m_h = 0.15
    node.soil_moisture_pct = 90.0

    node.trend = "RISING"
    node.risk_score = 0.8
    node.risk_level = risk_level
    node.hazard_state = risk_level
    node.event_state = "DETECTED"
    node.network_status = "OFFLINE"

    return node


def get_response_value(ai_result):

    response = ai_result.get("response")

    if isinstance(response, dict):
        return response.get("response")

    return None


def main():

    print("=" * 72)
    print("EDGE AI RESPONSE MAPPING TEST")
    print("=" * 72)
    print()

    expected_mapping = {
        "NORMAL": "NO_ACTION",
        "WATCH": "LOCAL_ALERT",
        "WARNING": "LOCAL_ALERT",
        "CRITICAL": "CRITICAL_LOCAL_ALERT",
    }

    ai = EdgeAI()

    passed = 0
    failed = 0

    try:

        for risk_level, expected_response in expected_mapping.items():

            node = create_node(risk_level)

            print("-" * 72)
            print(f"Testing Risk Level: {risk_level}")

            result = ai.analyze_node(node)

            actual_response = get_response_value(result)

            print(f"AI Status       : {result['status']}")
            print(f"AI Active       : {result['ai_active']}")
            print(f"Tool Called     : {result['tool_called']}")
            print(f"Expected        : {expected_response}")
            print(f"Actual          : {actual_response}")

            if actual_response == expected_response:

                print("[PASS] Correct response selected")
                passed += 1

            else:

                print("[FAIL] Incorrect response selected")
                failed += 1

        print()
        print("=" * 72)
        print("TEST SUMMARY")
        print("=" * 72)

        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        if failed == 0:

            print()
            print("EDGE AI MAPPING TEST PASSED")

        else:

            print()
            print("EDGE AI MAPPING TEST FAILED")

    finally:

        ai.close()


if __name__ == "__main__":
    main()
