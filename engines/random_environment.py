
"""
Background Environmental Simulation

This module generates realistic baseline environmental conditions
for the disaster simulation engines.

It does NOT generate disasters directly.

Disaster-specific behavior is handled by:
    - flood_engine.py
    - wildfire_engine.py
    - landslide_engine.py

The environment changes gradually over time with small,
controlled variations instead of completely random values.
"""

from dataclasses import dataclass
import random


@dataclass
class EnvironmentState:
    """Current background environmental conditions."""

    rainfall_mm_h: float
    temperature_c: float
    humidity_pct: float
    soil_moisture_pct: float
    wind_speed_m_s: float


class RandomEnvironment:
    """
    Generates a slowly changing natural environment.

    The values have temporal continuity:
        previous state
              +
        gradual change
              +
        small noise
              =
        next state
    """

    def __init__(self, seed: int = 42):
        """
        Initialize the environment.

        Args:
            seed: Random seed for reproducible simulations.
        """

        self.random = random.Random(seed)

        # Initial environmental conditions
        self.rainfall_mm_h = 5.0
        self.temperature_c = 30.0
        self.humidity_pct = 65.0
        self.soil_moisture_pct = 40.0
        self.wind_speed_m_s = 2.5

    def _smooth_change(
        self,
        current: float,
        target: float,
        response: float,
        noise: float,
    ) -> float:
        """
        Move the current value gradually toward a target
        while adding a small amount of controlled noise.
        """

        change = (target - current) * response
        variation = self.random.uniform(-noise, noise)

        return current + change + variation

    def step(self) -> dict:
        """
        Advance the environment by one simulation timestep.

        Returns:
            Dictionary containing current environmental conditions.
        """

        # ---------------------------------------------------------
        # Generate slowly changing target conditions
        # ---------------------------------------------------------

        rainfall_target = self.random.uniform(0.0, 15.0)
        temperature_target = self.random.uniform(27.0, 34.0)
        humidity_target = self.random.uniform(55.0, 85.0)
        wind_target = self.random.uniform(1.0, 6.0)

        # ---------------------------------------------------------
        # Gradually move environmental values toward targets
        # ---------------------------------------------------------

        self.rainfall_mm_h = self._smooth_change(
            self.rainfall_mm_h,
            rainfall_target,
            response=0.08,
            noise=0.8,
        )

        self.temperature_c = self._smooth_change(
            self.temperature_c,
            temperature_target,
            response=0.05,
            noise=0.15,
        )

        self.humidity_pct = self._smooth_change(
            self.humidity_pct,
            humidity_target,
            response=0.05,
            noise=0.5,
        )

        self.wind_speed_m_s = self._smooth_change(
            self.wind_speed_m_s,
            wind_target,
            response=0.08,
            noise=0.15,
        )

        # ---------------------------------------------------------
        # Soil moisture depends on rainfall.
        #
        # Rain increases soil moisture.
        # Dry conditions slowly reduce soil moisture.
        # ---------------------------------------------------------

        if self.rainfall_mm_h > 5.0:
            moisture_change = self.rainfall_mm_h * 0.015
        else:
            moisture_change = -0.08

        soil_noise = self.random.uniform(-0.05, 0.05)

        self.soil_moisture_pct += moisture_change + soil_noise

        # ---------------------------------------------------------
        # Keep values within physically reasonable limits
        # ---------------------------------------------------------

        self.rainfall_mm_h = max(
            0.0,
            min(self.rainfall_mm_h, 100.0)
        )

        self.temperature_c = max(
            15.0,
            min(self.temperature_c, 50.0)
        )

        self.humidity_pct = max(
            20.0,
            min(self.humidity_pct, 100.0)
        )

        self.soil_moisture_pct = max(
            5.0,
            min(self.soil_moisture_pct, 100.0)
        )

        self.wind_speed_m_s = max(
            0.0,
            min(self.wind_speed_m_s, 25.0)
        )

        # ---------------------------------------------------------
        # Return the environment state
        # ---------------------------------------------------------

        return {
            "rainfall_mm_h": round(self.rainfall_mm_h, 2),
            "temperature_c": round(self.temperature_c, 2),
            "humidity_pct": round(self.humidity_pct, 2),
            "soil_moisture_pct": round(self.soil_moisture_pct, 2),
            "wind_speed_m_s": round(self.wind_speed_m_s, 2),
        }


if __name__ == "__main__":
    """
    Simple standalone test.

    Run:
        python engines/random_environment.py
    """

    environment = RandomEnvironment()

    print("Background Environmental Simulation")
    print("-" * 70)

    for step in range(20):
        state = environment.step()

        print(
            f"Step {step + 1:02d} | "
            f"Rain: {state['rainfall_mm_h']:5.2f} mm/h | "
            f"Temp: {state['temperature_c']:5.2f} °C | "
            f"Humidity: {state['humidity_pct']:5.2f}% | "
            f"Soil: {state['soil_moisture_pct']:5.2f}% | "
            f"Wind: {state['wind_speed_m_s']:4.2f} m/s"
        )

