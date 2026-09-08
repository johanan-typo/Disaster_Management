from engines.node_model import VirtualNode
from engines.random_environment import RandomEnvironment
from engines.landslide_engine import LandslideEngine


# Create simulation components
environment = RandomEnvironment(seed=42)

landslide = LandslideEngine()

node = VirtualNode(
    node_id="LANDSLIDE_NODE_001",
    location="Hilly Zone"
)


print("Landslide Integration Test")
print("-" * 110)


# =================================================
# PHASE 1 — STABLE CONDITIONS
# =================================================

print("\n--- STABLE CONDITIONS ---")

for step in range(5):

    env = environment.step()

    landslide_state = landslide.step(
        rainfall_mm_h=env["rainfall_mm_h"],
        soil_moisture_pct=env["soil_moisture_pct"]
    )

    node.rainfall_mm_h = env["rainfall_mm_h"]
    node.temperature_c = env["temperature_c"]
    node.humidity_pct = env["humidity_pct"]
    node.soil_moisture_pct = env["soil_moisture_pct"]

    node.soil_stability = landslide_state["soil_stability"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 1:02d} | "
        f"Rain: {node.rainfall_mm_h:5.2f} mm/h | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Stability: {node.soil_stability:5.3f} | "
        f"Movement: "
        f"{landslide_state['ground_movement_mm']:6.2f} mm | "
        f"State: {landslide_state['hazard_state']}"
    )


# =================================================
# PHASE 2 — HEAVY RAIN
# =================================================

print("\n--- HEAVY RAIN ---")

for step in range(10):

    rainfall = 25.0
    soil_moisture = 75.0

    landslide_state = landslide.step(
        rainfall_mm_h=rainfall,
        soil_moisture_pct=soil_moisture
    )

    node.rainfall_mm_h = rainfall
    node.soil_moisture_pct = soil_moisture

    node.soil_stability = landslide_state["soil_stability"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 6:02d} | "
        f"Rain: {rainfall:5.2f} mm/h | "
        f"Soil: {soil_moisture:5.2f}% | "
        f"Stability: {node.soil_stability:5.3f} | "
        f"Movement: "
        f"{landslide_state['ground_movement_mm']:6.2f} mm | "
        f"Rate: "
        f"{landslide_state['movement_rate_mm_h']:5.2f} mm/h | "
        f"State: {landslide_state['hazard_state']}"
    )


# =================================================
# PHASE 3 — EXTREME RAIN
# =================================================

print("\n--- EXTREME RAIN + SATURATED SOIL ---")

for step in range(20):

    rainfall = 40.0
    soil_moisture = 90.0

    landslide_state = landslide.step(
        rainfall_mm_h=rainfall,
        soil_moisture_pct=soil_moisture
    )

    node.rainfall_mm_h = rainfall
    node.soil_moisture_pct = soil_moisture

    node.soil_stability = landslide_state["soil_stability"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 16:02d} | "
        f"Rain: {rainfall:5.2f} mm/h | "
        f"Soil: {soil_moisture:5.2f}% | "
        f"Stability: {node.soil_stability:5.3f} | "
        f"Movement: "
        f"{landslide_state['ground_movement_mm']:6.2f} mm | "
        f"Rate: "
        f"{landslide_state['movement_rate_mm_h']:5.2f} mm/h | "
        f"State: {landslide_state['hazard_state']}"
    )


print("\nTotal readings stored:", len(node.history))