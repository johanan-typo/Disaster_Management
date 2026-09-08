"""
Flood Simulation Engine

Simulates gradual flood development and rainstorm events.

The engine generates flood-related environmental observations.
It does NOT calculate the final risk score.
"""

from dataclasses import dataclass


@dataclass
class FloodState:
    """Current flood-related environmental state."""

    water_level_m: float = 0.5
    rate_of_rise_m_h: float = 0.0
    hazard_state: str = "NORMAL"


class FloodEngine:
    """
    Simulates flood development.

    The engine supports:
        - Normal conditions
        - Rainstorm event
        - Flood development
        - Rain stopping
        - Water-level recession
    """

    def __init__(self, initial_water_level: float = 0.5):

        self.water_level_m = initial_water_level
        self.previous_water_level = initial_water_level

        # Rainstorm control
        self.rainstorm_active = False

    def start_rainstorm(self):
        """Start a heavy rainfall event."""

        self.rainstorm_active = True

    def stop_rainstorm(self):
        """Stop the current rainfall event."""

        self.rainstorm_active = False

    def step(
        self,
        rainfall_mm_h: float,
        soil_moisture_pct: float,
    ) -> dict:
        """
        Advance the flood simulation by one timestep.
        """

        self.previous_water_level = self.water_level_m

        # -------------------------------------------------
        # 1. Determine rainfall effect
        # -------------------------------------------------

        if self.rainstorm_active:

            # Strong runoff during rainstorm
            if rainfall_mm_h > 30:
                rainfall_effect = 0.12

            elif rainfall_mm_h > 20:
                rainfall_effect = 0.08

            elif rainfall_mm_h > 10:
                rainfall_effect = 0.05

            else:
                rainfall_effect = 0.02

        else:

            # Normal environmental conditions
            if rainfall_mm_h > 10:
                rainfall_effect = 0.03

            elif rainfall_mm_h > 5:
                rainfall_effect = 0.015

            else:
                rainfall_effect = -0.005

        # -------------------------------------------------
        # 2. Soil saturation effect
        # -------------------------------------------------

        if soil_moisture_pct > 80:
            soil_effect = 0.04

        elif soil_moisture_pct > 60:
            soil_effect = 0.02

        else:
            soil_effect = 0.0

        # -------------------------------------------------
        # 3. Update water level
        # -------------------------------------------------

        self.water_level_m += rainfall_effect + soil_effect

        # Water level cannot become negative
        self.water_level_m = max(0.0, self.water_level_m)

        # -------------------------------------------------
        # 4. Calculate rate of rise
        # -------------------------------------------------

        self.rate_of_rise_m_h = (
            self.water_level_m - self.previous_water_level
        )

        # -------------------------------------------------
        # 5. Determine flood state
        # -------------------------------------------------

        if self.water_level_m >= 2.0:

            hazard_state = "FLOOD"

        elif self.water_level_m >= 1.0:

            hazard_state = "RISING"

        elif self.rate_of_rise_m_h < 0:

            hazard_state = "RECEDING"

        elif self.rainstorm_active:

            hazard_state = "RAINSTORM"

        else:

            hazard_state = "NORMAL"

        return {
            "water_level_m": round(self.water_level_m, 3),
            "rate_of_rise_m_h": round(self.rate_of_rise_m_h, 3),
            "hazard_state": hazard_state,
            "rainstorm_active": self.rainstorm_active,
        }


# ---------------------------------------------------------
# Standalone test
# ---------------------------------------------------------

if __name__ == "__main__":

    flood = FloodEngine(initial_water_level=0.5)

    print("Flood Rainstorm Simulation")
    print("-" * 90)

    # ---------------------------------------------
    # Phase 1: Normal conditions
    # ---------------------------------------------

    print("\n--- NORMAL CONDITIONS ---")

    for step in range(5):

        state = flood.step(
            rainfall_mm_h=3.0,
            soil_moisture_pct=40.0,
        )

        print(
            f"Step {step + 1:02d} | "
            f"Rain: 3.0 mm/h | "
            f"Water: {state['water_level_m']:.3f} m | "
            f"Rise: {state['rate_of_rise_m_h']:.3f} m/h | "
            f"State: {state['hazard_state']}"
        )

    # ---------------------------------------------
    # Phase 2: Rainstorm begins
    # ---------------------------------------------

    print("\n--- RAINSTORM STARTED ---")

    flood.start_rainstorm()

    for step in range(20):

        state = flood.step(
            rainfall_mm_h=35.0,
            soil_moisture_pct=75.0,
        )

        print(
            f"Step {step + 6:02d} | "
            f"Rain: 35.0 mm/h | "
            f"Water: {state['water_level_m']:.3f} m | "
            f"Rise: {state['rate_of_rise_m_h']:.3f} m/h | "
            f"State: {state['hazard_state']}"
        )

    # ---------------------------------------------
    # Phase 3: Rainstorm stops
    # ---------------------------------------------

    print("\n--- RAINSTORM STOPPED ---")

    flood.stop_rainstorm()

    for step in range(10):

        state = flood.step(
            rainfall_mm_h=0.0,
            soil_moisture_pct=70.0,
        )

        print(
            f"Step {step + 26:02d} | "
            f"Rain: 0.0 mm/h | "
            f"Water: {state['water_level_m']:.3f} m | "
            f"Rise: {state['rate_of_rise_m_h']:.3f} m/h | "
            f"State: {state['hazard_state']}"
        )