from engines.node_model import VirtualNode
from intelligence.edge_ai import EdgeAI


def main():

    node = VirtualNode(
        node_id="A",
        location="Upstream",

        # Environmental values
        rainfall_mm_h=80.0,
        temperature_c=27.0,
        humidity_pct=90.0,
        soil_moisture_pct=90.0,

        # Flood state
        water_level_m=3.2,
        rate_of_rise_m_h=0.14,

        # Other environmental values
        wind_speed_m_s=2.0,
        smoke_level=0.0,
        gas_level=0.0,
        soil_stability=0.7,

        # Deterministic intelligence
        trend="RISING",
        risk_score=0.83,
        risk_level="CRITICAL",
        hazard_state="CRITICAL",
        event_state="DETECTED",

        # Resilience state
        network_status="OFFLINE",
        edge_processing="ACTIVE",
    )

    print("=" * 60)
    print("REAL VIRTUAL NODE -> NEEDLE EDGE AI TEST")
    print("=" * 60)

    print("\nNODE")
    print("----")
    print("ID:", node.node_id)
    print("Location:", node.location)

    print("\nSENSOR DATA")
    print("-----------")
    print("Water:", node.water_level_m, "m")
    print("Rainfall:", node.rainfall_mm_h, "mm/h")
    print("Rate:", node.rate_of_rise_m_h, "m/h")
    print("Soil:", node.soil_moisture_pct, "%")

    print("\nDETERMINISTIC INTELLIGENCE")
    print("--------------------------")
    print("Risk:", node.risk_level)
    print("Risk score:", node.risk_score)
    print("Trend:", node.trend)
    print("Hazard:", node.hazard_state)
    print("Event:", node.event_state)

    print("\nNETWORK")
    print("-------")
    print("Network:", node.network_status)
    print("Edge processing:", node.edge_processing)

    # ---------------------------------------------------------
    # Needle
    # ---------------------------------------------------------

    print("\nSTARTING NEEDLE EDGE AI...")

    ai = EdgeAI()

    result = ai.analyze_node(node)

    print("\nNEEDLE RESULT")
    print("-------------")

    print("AI active:", result["ai_active"])
    print("Tool called:", result["tool_called"])
    print("Action executed:", result["action_executed"])
    print("Status:", result["status"])

    print("Confidence:", result["confidence"])

    print("Reasoning:", result["reasoning"])

    print("Response:", result["response"])

    if result["error"]:
        print("Error:", result["error"])

    ai.close()

    print("\nTEST COMPLETE")


if __name__ == "__main__":
    main()
