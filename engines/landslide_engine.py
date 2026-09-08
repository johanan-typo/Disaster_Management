"""
Landslide Simulation Engine

Simulates gradual slope instability caused by rainfall,
soil saturation, and prolonged wet conditions.

This engine generates landslide-related environmental
observations. It does NOT calculate the final risk score.
"""

from dataclasses import dataclass


@dataclass
class LandslideState:
    """Current landslide-related environmental state."""

    soil_stability: float = 1.0
    ground_movement_mm: float = 0.0
    movement_rate_mm_h: float = 0.0
    hazard_state: str = "NORMAL"


class LandslideEngine:
    """
    Simulates slope stability and landslide development.

    Stability ranges from:

        1.0 → highly stable
        0.0 → complete instability
    """

    def __init__(self, initial_stability: float = 1.0):

        self.soil_stability = initial_stability

        self.ground_movement_mm = 0.0
        self.previous_movement_mm = 0.0

    def step(
        self,
        rainfall_mm_h: float,
        soil_moisture_pct: float,
    ) -> dict:
        """
        Advance the landslide simulation by one timestep.
        """

        self.previous_movement_mm = self.ground_movement_mm

        # -------------------------------------------------
        # 1. Calculate rainfall effect
        # -------------------------------------------------

        if rainfall_mm_h > 30:
            rainfall_effect = 0.04

        elif rainfall_mm_h > 20:
            rainfall_effect = 0.025

        elif rainfall_mm_h > 10:
            rainfall_effect = 0.015

        elif rainfall_mm_h > 5:
            rainfall_effect = 0.005

        else:
            rainfall_effect = 0.0

        # -------------------------------------------------
        # 2. Calculate soil saturation effect
        # -------------------------------------------------

        if soil_moisture_pct > 85:
            saturation_effect = 0.04

        elif soil_moisture_pct > 70:
            saturation_effect = 0.02

        elif soil_moisture_pct > 50:
            saturation_effect = 0.01

        else:
            saturation_effect = 0.0

        # -------------------------------------------------
        # 3. Reduce soil stability
        # -------------------------------------------------

        stability_loss = rainfall_effect + saturation_effect

        self.soil_stability -= stability_loss

        # Keep stability between 0 and 1
        self.soil_stability = max(
            0.0,
            min(self.soil_stability, 1.0)
        )

        # -------------------------------------------------
        # 4. Calculate ground movement
        # -------------------------------------------------

        if self.soil_stability < 0.3:

            movement = 5.0

        elif self.soil_stability < 0.5:

            movement = 2.0

        elif self.soil_stability < 0.7:

            movement = 0.8

        else:

            movement = 0.1

        # Add movement
        self.ground_movement_mm += movement

        # -------------------------------------------------
        # 5. Calculate movement rate
        # -------------------------------------------------

        self.movement_rate_mm_h = (
            self.ground_movement_mm
            - self.previous_movement_mm
        )

        # -------------------------------------------------
        # 6. Determine hazard state
        # -------------------------------------------------

        if self.soil_stability <= 0.3:

            hazard_state = "LANDSLIDE"

        elif self.soil_stability <= 0.5:

            hazard_state = "CRITICAL"

        elif self.soil_stability <= 0.7:

            hazard_state = "UNSTABLE"

        elif rainfall_mm_h > 20:

            hazard_state = "HEAVY_RAIN"

        else:

            hazard_state = "NORMAL"

        return {
            "soil_stability": round(
                self.soil_stability,
                3
            ),

            "ground_movement_mm": round(
                self.ground_movement_mm,
                2
            ),

            "movement_rate_mm_h": round(
                self.movement_rate_mm_h,
                2
            ),

            "hazard_state": hazard_state,
        }


# ---------------------------------------------------------
# Standalone test
# ---------------------------------------------------------

if __name__ == "__main__":

    landslide = LandslideEngine()

    print("Landslide Simulation Engine")
    print("-" * 110)

    # =================================================
    # PHASE 1 — STABLE CONDITIONS
    # =================================================

    print("\n--- PHASE 1: STABLE SLOPE ---")

    for step in range(5):

        state = landslide.step(
            rainfall_mm_h=2.0,
            soil_moisture_pct=40.0,
        )

        print(
            f"Step {step + 1:02d} | "
            f"Rain: 2.0 mm/h | "
            f"Soil: 40.0% | "
            f"Stability: {state['soil_stability']:.3f} | "
            f"Movement: {state['ground_movement_mm']:6.2f} mm | "
            f"Rate: {state['movement_rate_mm_h']:5.2f} mm/h | "
            f"State: {state['hazard_state']}"
        )

    # =================================================
    # PHASE 2 — HEAVY RAIN
    # =================================================

    print("\n--- PHASE 2: HEAVY RAIN ---")

    for step in range(10):

        state = landslide.step(
            rainfall_mm_h=25.0,
            soil_moisture_pct=75.0,
        )

        print(
            f"Step {step + 6:02d} | "
            f"Rain: 25.0 mm/h | "
            f"Soil: 75.0% | "
            f"Stability: {state['soil_stability']:.3f} | "
            f"Movement: {state['ground_movement_mm']:6.2f} mm | "
            f"Rate: {state['movement_rate_mm_h']:5.2f} mm/h | "
            f"State: {state['hazard_state']}"
        )

    # =================================================
    # PHASE 3 — EXTREME RAIN
    # =================================================

    print("\n--- PHASE 3: EXTREME RAIN + SATURATED SOIL ---")

    for step in range(20):

        state = landslide.step(
            rainfall_mm_h=40.0,
            soil_moisture_pct=90.0,
        )

        print(
            f"Step {step + 16:02d} | "
            f"Rain: 40.0 mm/h | "
            f"Soil: 90.0% | "
            f"Stability: {state['soil_stability']:.3f} | "
            f"Movement: {state['ground_movement_mm']:6.2f} mm | "
            f"Rate: {state['movement_rate_mm_h']:5.2f} mm/h | "
            f"State: {state['hazard_state']}"
        )