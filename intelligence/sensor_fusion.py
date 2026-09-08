class SensorFusion:
    """
    Combines multiple environmental indicators into
    a single normalized flood-evidence score.

    This is an engineering-defined fusion model,
    not a trained AI model.
    """

    def __init__(self):
        self.weights = {
            "water_level": 0.30,
            "rainfall": 0.20,
            "rate_of_rise": 0.25,
            "soil_moisture": 0.15,
            "persistence": 0.10,
        }

    @staticmethod
    def normalize(value, minimum, maximum):
        """Normalize a value to the range 0–1."""

        if maximum <= minimum:
            raise ValueError("Maximum must be greater than minimum.")

        normalized = (value - minimum) / (maximum - minimum)

        return max(0.0, min(normalized, 1.0))

    def calculate_evidence(
        self,
        water_level_m,
        rainfall_mm_h,
        rate_of_rise_m_h,
        soil_moisture_pct,
        persistence,
    ):
        """Calculate combined environmental flood evidence."""

        water_score = self.normalize(
            water_level_m, 0.5, 4.0
        )

        rainfall_score = self.normalize(
            rainfall_mm_h, 0.0, 120.0
        )

        rate_score = self.normalize(
            rate_of_rise_m_h, 0.0, 0.40
        )

        soil_score = self.normalize(
            soil_moisture_pct, 20.0, 100.0
        )

        persistence_score = self.normalize(
            persistence, 0, 5
        )

        evidence = (
            water_score * self.weights["water_level"]
            + rainfall_score * self.weights["rainfall"]
            + rate_score * self.weights["rate_of_rise"]
            + soil_score * self.weights["soil_moisture"]
            + persistence_score * self.weights["persistence"]
        )

        return round(evidence, 4)

    def analyze(self, node, temporal_features):
        """Combine environmental observations with temporal features."""

        evidence = self.calculate_evidence(
            water_level_m=node.water_level_m,
            rainfall_mm_h=node.rainfall_mm_h,
            rate_of_rise_m_h=temporal_features["rate_of_rise_m_h"],
            soil_moisture_pct=node.soil_moisture_pct,
            persistence=temporal_features["persistence"],
        )

        return {
            "flood_evidence_score": evidence,
            "water_level": node.water_level_m,
            "rainfall": node.rainfall_mm_h,
            "rate_of_rise": temporal_features["rate_of_rise_m_h"],
            "soil_moisture": node.soil_moisture_pct,
            "persistence": temporal_features["persistence"],
        }
