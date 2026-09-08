"""
Wildfire Simulation Engine

Simulates wildfire development using environmental conditions
such as temperature, humidity, wind speed, and soil/fuel dryness.

This engine generates fire-related environmental observations.
It does NOT calculate the final risk score.
"""

from dataclasses import dataclass


@dataclass
class WildfireState:
    """Current wildfire-related environmental state."""

    fire_intensity: float = 0.0
    smoke_level: float = 0.0
    fire_spread_rate: float = 0.0
    hazard_state: str = "NORMAL"


class WildfireEngine:
    """
    Simulates wildfire development.

    Environmental conditions influence the probability and
    intensity of fire development.
    """

    def __init__(self):

        self.fire_intensity = 0.0
        self.smoke_level = 0.0
        self.fire_spread_rate = 0.0

        self.fire_active = False

    def start_fire(self):
        """Ignite a wildfire event."""

        self.fire_active = True

    def stop_fire(self):
        """Stop the wildfire event."""

        self.fire_active = False

    def step(
        self,
        temperature_c: float,
        humidity_pct: float,
        wind_speed_m_s: float,
        soil_moisture_pct: float,
    ) -> dict:
        """
        Advance the wildfire simulation by one timestep.
        """

        # -------------------------------------------------
        # 1. Calculate environmental dryness
        # -------------------------------------------------

        dryness = 0.0

        if temperature_c > 35:
            dryness += 0.3

        elif temperature_c > 30:
            dryness += 0.15

        if humidity_pct < 30:
            dryness += 0.3

        elif humidity_pct < 50:
            dryness += 0.15

        if soil_moisture_pct < 20:
            dryness += 0.3

        elif soil_moisture_pct < 40:
            dryness += 0.15

        # -------------------------------------------------
        # 2. Fire inactive
        # -------------------------------------------------

        if not self.fire_active:

            # Fire naturally dies down
            self.fire_intensity = max(
                0.0,
                self.fire_intensity - 0.1
            )

            self.smoke_level = max(
                0.0,
                self.smoke_level - 2.0
            )

            self.fire_spread_rate = 0.0

            if self.fire_intensity == 0:

                hazard_state = "NORMAL"

            else:

                hazard_state = "RECEDING"

        # -------------------------------------------------
        # 3. Fire active
        # -------------------------------------------------

        else:

            # Environmental conditions influence intensity
            intensity_change = (
                0.2
                + dryness * 0.5
                + wind_speed_m_s * 0.02
            )

            self.fire_intensity += intensity_change

            # Limit intensity to 100
            self.fire_intensity = min(
                self.fire_intensity,
                100.0
            )

            # Wind increases fire spread
            self.fire_spread_rate = (
                0.1
                + wind_speed_m_s * 0.05
            )

            # Smoke is related to fire intensity
            self.smoke_level = min(
                self.fire_intensity * 1.2,
                100.0
            )

            # Determine fire state
            if self.fire_intensity >= 60:

                hazard_state = "SEVERE"

            elif self.fire_intensity >= 30:

                hazard_state = "ACTIVE"

            else:

                hazard_state = "IGNITION"

        return {
            "fire_intensity": round(
                self.fire_intensity,
                2
            ),

            "smoke_level": round(
                self.smoke_level,
                2
            ),

            "fire_spread_rate": round(
                self.fire_spread_rate,
                2
            ),

            "hazard_state": hazard_state,

            "fire_active": self.fire_active,
        }


# ---------------------------------------------------------
# Standalone test
# ---------------------------------------------------------

if __name__ == "__main__":

    wildfire = WildfireEngine()

    print("Dynamic Wildfire Simulation")
    print("-" * 110)

    # =================================================
    # PHASE 1 — NORMAL CONDITIONS
    # =================================================

    print("\n--- PHASE 1: NORMAL CONDITIONS ---")

    for step in range(5):

        state = wildfire.step(
            temperature_c=28.0,
            humidity_pct=65.0,
            wind_speed_m_s=2.0,
            soil_moisture_pct=50.0,
        )

        print(
            f"Step {step + 1:02d} | "
            f"Temp: 28.0°C | "
            f"Humidity: 65.0% | "
            f"Wind: 2.0 m/s | "
            f"Soil: 50.0% | "
            f"Intensity: {state['fire_intensity']:6.2f} | "
            f"Smoke: {state['smoke_level']:6.2f} | "
            f"Spread: {state['fire_spread_rate']:5.2f} | "
            f"State: {state['hazard_state']}"
        )

    # =================================================
    # PHASE 2 — HOT AND DRY CONDITIONS
    # =================================================

    print("\n--- PHASE 2: HOT + DRY CONDITIONS ---")

    for step in range(5):

        state = wildfire.step(
            temperature_c=38.0,
            humidity_pct=25.0,
            wind_speed_m_s=3.0,
            soil_moisture_pct=20.0,
        )

        print(
            f"Step {step + 6:02d} | "
            f"Temp: 38.0°C | "
            f"Humidity: 25.0% | "
            f"Wind: 3.0 m/s | "
            f"Soil: 20.0% | "
            f"Intensity: {state['fire_intensity']:6.2f} | "
            f"Smoke: {state['smoke_level']:6.2f} | "
            f"Spread: {state['fire_spread_rate']:5.2f} | "
            f"State: {state['hazard_state']}"
        )

    # =================================================
    # PHASE 3 — FIRE IGNITION
    # =================================================

    print("\n--- PHASE 3: FIRE IGNITION ---")

    wildfire.start_fire()

    for step in range(5):

        state = wildfire.step(
            temperature_c=38.0,
            humidity_pct=25.0,
            wind_speed_m_s=3.0,
            soil_moisture_pct=20.0,
        )

        print(
            f"Step {step + 11:02d} | "
            f"Temp: 38.0°C | "
            f"Humidity: 25.0% | "
            f"Wind: 3.0 m/s | "
            f"Soil: 20.0% | "
            f"Intensity: {state['fire_intensity']:6.2f} | "
            f"Smoke: {state['smoke_level']:6.2f} | "
            f"Spread: {state['fire_spread_rate']:5.2f} | "
            f"State: {state['hazard_state']}"
        )

    # =================================================
    # PHASE 4 — HIGH WIND
    # =================================================

    print("\n--- PHASE 4: HIGH WIND — RAPID SPREAD ---")

    for step in range(10):

        state = wildfire.step(
            temperature_c=40.0,
            humidity_pct=20.0,
            wind_speed_m_s=10.0,
            soil_moisture_pct=15.0,
        )

        print(
            f"Step {step + 16:02d} | "
            f"Temp: 40.0°C | "
            f"Humidity: 20.0% | "
            f"Wind: 10.0 m/s | "
            f"Soil: 15.0% | "
            f"Intensity: {state['fire_intensity']:6.2f} | "
            f"Smoke: {state['smoke_level']:6.2f} | "
            f"Spread: {state['fire_spread_rate']:5.2f} | "
            f"State: {state['hazard_state']}"
        )

    # =================================================
    # PHASE 5 — FIRE CONTAINED
    # =================================================

    print("\n--- PHASE 5: FIRE CONTAINED ---")

    wildfire.stop_fire()

    for step in range(15):

        state = wildfire.step(
            temperature_c=30.0,
            humidity_pct=55.0,
            wind_speed_m_s=2.0,
            soil_moisture_pct=45.0,
        )

        print(
            f"Step {step + 26:02d} | "
            f"Temp: 30.0°C | "
            f"Humidity: 55.0% | "
            f"Wind: 2.0 m/s | "
            f"Soil: 45.0% | "
            f"Intensity: {state['fire_intensity']:6.2f} | "
            f"Smoke: {state['smoke_level']:6.2f} | "
            f"Spread: {state['fire_spread_rate']:5.2f} | "
            f"State: {state['hazard_state']}"
        )