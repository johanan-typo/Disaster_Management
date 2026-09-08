from typing import Dict, List


class TemporalEngine:
    """
    Analyzes recent environmental observations over time.

    Extracts rate of change, trend, and persistence.
    It does not determine the final hazard risk.
    """

    def __init__(self, history_window: int = 5):
        self.history_window = history_window

    def calculate_rate_of_rise(
        self,
        current_level: float,
        previous_level: float,
        time_interval_hours: float = 1.0,
    ) -> float:

        if time_interval_hours <= 0:
            raise ValueError("Time interval must be greater than zero.")

        return (current_level - previous_level) / time_interval_hours

    def determine_trend(
        self,
        rate_of_rise: float,
        stable_threshold: float = 0.01,
    ) -> str:

        if rate_of_rise > stable_threshold:
            return "RISING"

        if rate_of_rise < -stable_threshold:
            return "FALLING"

        return "STABLE"

    def calculate_persistence(self, history: List[Dict]) -> int:

        if len(history) < 2:
            return 0

        recent_history = history[-self.history_window:]

        persistence = 0

        for current, previous in zip(
            recent_history[1:],
            recent_history[:-1],
        ):
            if current["water_level_m"] > previous["water_level_m"]:
                persistence += 1
            else:
                break

        return persistence

    def analyze(self, node) -> Dict:

        if len(node.history) < 2:
            return {
                "rate_of_rise_m_h": 0.0,
                "trend": "STABLE",
                "persistence": 0,
            }

        current = node.history[-1]
        previous = node.history[-2]

        rate = self.calculate_rate_of_rise(
            current["water_level_m"],
            previous["water_level_m"],
        )

        trend = self.determine_trend(rate)

        persistence = self.calculate_persistence(node.history)

        node.rate_of_rise_m_h = round(rate, 4)
        node.trend = trend

        return {
            "rate_of_rise_m_h": round(rate, 4),
            "trend": trend,
            "persistence": persistence,
        }
