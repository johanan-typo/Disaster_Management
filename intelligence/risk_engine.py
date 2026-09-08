class RiskEngine:
    """
    Converts fused environmental evidence into a local
    hazard risk decision.

    This is a transparent engineering rule set.
    It is not a trained prediction model.
    """

    def __init__(self):
        self.thresholds = {
            "WATCH": 0.30,
            "WARNING": 0.55,
            "CRITICAL": 0.75,
        }

    def determine_risk_level(self, evidence_score):
        """Convert evidence score into a risk level."""

        if evidence_score >= self.thresholds["CRITICAL"]:
            return "CRITICAL"

        if evidence_score >= self.thresholds["WARNING"]:
            return "WARNING"

        if evidence_score >= self.thresholds["WATCH"]:
            return "WATCH"

        return "NORMAL"

    def determine_hazard_state(self, risk_level):
        """Map risk level to the corresponding hazard state."""

        if risk_level == "CRITICAL":
            return "CRITICAL"

        if risk_level == "WARNING":
            return "WARNING"

        if risk_level == "WATCH":
            return "WATCH"

        return "NORMAL"

    def determine_event_state(
        self,
        risk_level,
        trend,
        persistence,
    ):
        """
        Determine the local event state using risk,
        temporal trend, and persistence.
        """

        if risk_level == "CRITICAL":
            return "DETECTED"

        if risk_level == "WARNING":
            if trend == "RISING" and persistence >= 1:
                return "DETECTED"

            return "DEVELOPING"

        if risk_level == "WATCH":
            if trend == "RISING":
                return "DEVELOPING"

            return "NORMAL"

        return "NORMAL"

    def generate_reasons(
        self,
        node,
        temporal_features,
        fusion_result,
        risk_level,
    ):
        """Generate human-readable reasons for the decision."""

        reasons = []

        if node.water_level_m >= 2.5:
            reasons.append(
                f"Elevated water level ({node.water_level_m:.2f} m)"
            )

        if node.rainfall_mm_h >= 60:
            reasons.append(
                f"Heavy rainfall ({node.rainfall_mm_h:.1f} mm/h)"
            )

        if temporal_features["rate_of_rise_m_h"] >= 0.10:
            reasons.append(
                f"Rapid water-level rise "
                f"({temporal_features['rate_of_rise_m_h']:.2f} m/h)"
            )

        if node.soil_moisture_pct >= 75:
            reasons.append(
                f"High soil moisture ({node.soil_moisture_pct:.1f}%)"
            )

        if temporal_features["persistence"] >= 2:
            reasons.append(
                f"Persistent rising condition "
                f"({temporal_features['persistence']} intervals)"
            )

        if not reasons:
            reasons.append("No significant combined hazard indicators")

        return reasons

    def analyze(self, node, temporal_features, fusion_result):
        """
        Produce the complete local edge risk decision.
        """

        evidence_score = fusion_result["flood_evidence_score"]

        risk_level = self.determine_risk_level(
            evidence_score
        )

        hazard_state = self.determine_hazard_state(
            risk_level
        )

        event_state = self.determine_event_state(
            risk_level,
            temporal_features["trend"],
            temporal_features["persistence"],
        )

        reasons = self.generate_reasons(
            node,
            temporal_features,
            fusion_result,
            risk_level,
        )

        node.risk_score = evidence_score
        node.risk_level = risk_level
        node.hazard_state = hazard_state
        node.event_state = event_state

        return {
            "hazard": "FLOOD",
            "risk_score": evidence_score,
            "risk_level": risk_level,
            "trend": temporal_features["trend"],
            "hazard_state": hazard_state,
            "event_state": event_state,
            "status": (
                "DEVELOPING"
                if event_state in ["DEVELOPING", "DETECTED"]
                else "NORMAL"
            ),
            "reasons": reasons,
        }
