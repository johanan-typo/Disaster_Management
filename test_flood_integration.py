from engines.node_model import VirtualNode
from engines.random_environment import RandomEnvironment
from engines.flood_engine import FloodEngine


# Create the three components
environment = RandomEnvironment(seed=42)

flood = FloodEngine(initial_water_level=0.5)

node = VirtualNode(
    node_id="FLOOD_NODE_001",
    location="Flood-Prone Zone"
)


print("Flood Integration Test")
print("-" * 90)


for step in range(30):

    # 1. Generate background environment
    env = environment.step()

    # 2. Send environment to flood engine
    flood_state = flood.step(
        rainfall_mm_h=env["rainfall_mm_h"],
        soil_moisture_pct=env["soil_moisture_pct"]
    )

    # 3. Update virtual sensor node
    node.rainfall_mm_h = env["rainfall_mm_h"]
    node.temperature_c = env["temperature_c"]
    node.humidity_pct = env["humidity_pct"]
    node.soil_moisture_pct = env["soil_moisture_pct"]

    node.water_level_m = flood_state["water_level_m"]
    node.rate_of_rise_m_h = flood_state["rate_of_rise_m_h"]
    node.hazard_state = flood_state["hazard_state"]

    # 4. Store reading
    node.update_timestamp()
    node.add_reading()

    # 5. Display result
    print(
        f"Step {step + 1:02d} | "
        f"Rain: {node.rainfall_mm_h:5.2f} mm/h | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Water: {node.water_level_m:5.3f} m | "
        f"Rise: {node.rate_of_rise_m_h:5.3f} m/h | "
        f"State: {node.hazard_state}"
    )


print("\nTotal readings stored:", len(node.history))