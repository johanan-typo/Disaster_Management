import needle
from typing import Literal


@needle.tool
def raise_local_alert(
    severity: Literal["WATCH", "WARNING", "CRITICAL"],
    reason: str,
):
    """Activate a local disaster alert.

    Args:
        severity: alert severity based on the detected hazard condition
        reason: short reason for activating the alert
    """
    print("\n🚨 LOCAL ALERT TOOL EXECUTED")
    print("Severity:", severity)
    print("Reason:", reason)

    return {
        "action": "LOCAL_ALERT",
        "severity": severity,
        "status": "ACTIVATED",
    }


agent = needle.Needle(
    tools=[raise_local_alert],
    system=(
        "network: offline; "
        "device: local disaster monitoring computer"
    ),
)

result = agent.run(
    "A flood has reached CRITICAL severity. "
    "The water level is 3.2 meters and rising rapidly. "
    "Activate the appropriate local emergency alert."
)

print("\nNEEDLE RESULT:")
print(result)

agent.close()
