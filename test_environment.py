from engines.node_model import VirtualNode
from engines.random_environment import RandomEnvironment


# Create background environment
environment = RandomEnvironment(seed=42)

# Create virtual monitoring node
node = VirtualNode(
    node_id="NODE_001",
    location="Test Zone"
)


# Generate 10 environmental readings
for step in range(10):

    # Get environmental conditions
    state = environment.step()

    # Transfer environment values to the virtual node
    node.rainfall_mm_h = state["rainfall_mm_h"]
    node.temperature_c = state["temperature_c"]
    node.humidity_pct = state["humidity_pct"]
    node.soil_moisture_pct = state["soil_moisture_pct"]
    node.wind_speed_m_s = state["wind_speed_m_s"]

    # Update timestamp
    node.update_timestamp()

    # Store reading in node history
    node.add_reading()

    print(
        f"Step {step + 1:02d} | "
        f"Rain: {node.rainfall_mm_h:5.2f} mm/h | "
        f"Temp: {node.temperature_c:5.2f} °C | "
        f"Humidity: {node.humidity_pct:5.2f}% | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Wind: {node.wind_speed_m_s:4.2f} m/s"
    )


print("\nTotal readings stored:", len(node.history))