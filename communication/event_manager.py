from datetime import datetime


class EventManager:
    """
    Converts local risk decisions into environmental events.

    Events represent meaningful hazard-state changes or
    continuing hazardous conditions.

    This is part of the local edge processing layer.
    """

    def __init__(self):
        self.active_events = {}
        self.event_history = []

    def create_event(self, node, risk_result):
        """Create a new hazard event for a node."""

        event = {
            "event_id": (
                f"{node.node_id}_"
                f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            ),
            "node_id": node.node_id,
            "location": node.location,
            "hazard": risk_result["hazard"],
            "risk_score": risk_result["risk_score"],
            "risk_level": risk_result["risk_level"],
            "trend": risk_result["trend"],
            "hazard_state": risk_result["hazard_state"],
            "event_state": risk_result["event_state"],
            "status": risk_result["status"],
            "reasons": risk_result["reasons"],
            "timestamp": datetime.now(),
        }

        self.active_events[node.node_id] = event
        self.event_history.append(event)

        return event

    def update_event(self, node, risk_result):
        """Update an existing active event."""

        event = self.active_events[node.node_id]

        event.update({
            "risk_score": risk_result["risk_score"],
            "risk_level": risk_result["risk_level"],
            "trend": risk_result["trend"],
            "hazard_state": risk_result["hazard_state"],
            "event_state": risk_result["event_state"],
            "status": risk_result["status"],
            "reasons": risk_result["reasons"],
            "timestamp": datetime.now(),
        })

        return event

    def clear_event(self, node):
        """Clear the active event when the hazard condition ends."""

        if node.node_id not in self.active_events:
            return None

        event = self.active_events.pop(node.node_id)

        event["event_state"] = "NORMAL"
        event["status"] = "CLEARED"
        event["timestamp"] = datetime.now()

        self.event_history.append(event)

        return event

    def process(self, node, risk_result):
        """
        Decide whether to create, update, or clear an event.
        """

        risk_level = risk_result["risk_level"]

        if risk_level in ["WATCH", "WARNING", "CRITICAL"]:

            if node.node_id in self.active_events:
                return self.update_event(
                    node,
                    risk_result,
                )

            return self.create_event(
                node,
                risk_result,
            )

        return self.clear_event(node)
