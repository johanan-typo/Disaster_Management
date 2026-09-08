from engines.node_model import VirtualNode
from engines.random_environment import RandomEnvironment
from engines.wildfire_engine import WildfireEngine


# Create simulation components
environment = RandomEnvironment(seed=42)

wildfire = WildfireEngine()

node = VirtualNode(
    node_id="FIRE_NODE_001",
    location="Forest Zone"
)


print("Wildfire Integration Test")
print("-" * 110)


# =================================================
# Phase 1 — Normal environment
# =================================================

print("\n--- NORMAL CONDITIONS ---")

for step in range(5):

    env = environment.step()

    fire_state = wildfire.step(
        temperature_c=env["temperature_c"],
        humidity_pct=env["humidity_pct"],
        wind_speed_m_s=env["wind_speed_m_s"],
        soil_moisture_pct=env["soil_moisture_pct"]
    )

    node.temperature_c = env["temperature_c"]
    node.humidity_pct = env["humidity_pct"]
    node.wind_speed_m_s = env["wind_speed_m_s"]
    node.soil_moisture_pct = env["soil_moisture_pct"]

    node.smoke_level = fire_state["smoke_level"]
    node.hazard_state = fire_state["hazard_state"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 1:02d} | "
        f"Temp: {node.temperature_c:5.2f}°C | "
        f"Humidity: {node.humidity_pct:5.2f}% | "
        f"Wind: {node.wind_speed_m_s:5.2f} m/s | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Smoke: {node.smoke_level:6.2f} | "
        f"State: {node.hazard_state}"
    )


# =================================================
# Phase 2 — Fire ignition
# =================================================

print("\n--- FIRE IGNITION ---")

wildfire.start_fire()

for step in range(10):

    # Simulate hot and dry conditions
    temperature = 38.0
    humidity = 25.0
    wind = 5.0
    soil_moisture = 20.0

    fire_state = wildfire.step(
        temperature_c=temperature,
        humidity_pct=humidity,
        wind_speed_m_s=wind,
        soil_moisture_pct=soil_moisture
    )

    node.temperature_c = temperature
    node.humidity_pct = humidity
    node.wind_speed_m_s = wind
    node.soil_moisture_pct = soil_moisture

    node.smoke_level = fire_state["smoke_level"]
    node.hazard_state = fire_state["hazard_state"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 6:02d} | "
        f"Temp: {node.temperature_c:5.2f}°C | "
        f"Humidity: {node.humidity_pct:5.2f}% | "
        f"Wind: {node.wind_speed_m_s:5.2f} m/s | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Smoke: {node.smoke_level:6.2f} | "
        f"State: {node.hazard_state}"
    )


# =================================================
# Phase 3 — High wind
# =================================================

print("\n--- HIGH WIND / RAPID FIRE SPREAD ---")

for step in range(10):

    temperature = 40.0
    humidity = 20.0
    wind = 10.0
    soil_moisture = 15.0

    fire_state = wildfire.step(
        temperature_c=temperature,
        humidity_pct=humidity,
        wind_speed_m_s=wind,
        soil_moisture_pct=soil_moisture
    )

    node.temperature_c = temperature
    node.humidity_pct = humidity
    node.wind_speed_m_s = wind
    node.soil_moisture_pct = soil_moisture

    node.smoke_level = fire_state["smoke_level"]
    node.hazard_state = fire_state["hazard_state"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 16:02d} | "
        f"Temp: {node.temperature_c:5.2f}°C | "
        f"Humidity: {node.humidity_pct:5.2f}% | "
        f"Wind: {node.wind_speed_m_s:5.2f} m/s | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Smoke: {node.smoke_level:6.2f} | "
        f"State: {node.hazard_state}"
    )


# =================================================
# Phase 4 — Fire contained
# =================================================

print("\n--- FIRE CONTAINED ---")

wildfire.stop_fire()

for step in range(10):

    fire_state = wildfire.step(
        temperature_c=30.0,
        humidity_pct=55.0,
        wind_speed_m_s=2.0,
        soil_moisture_pct=45.0
    )

    node.temperature_c = 30.0
    node.humidity_pct = 55.0
    node.wind_speed_m_s = 2.0
    node.soil_moisture_pct = 45.0

    node.smoke_level = fire_state["smoke_level"]
    node.hazard_state = fire_state["hazard_state"]

    node.update_timestamp()
    node.add_reading()

    print(
        f"Step {step + 26:02d} | "
        f"Temp: {node.temperature_c:5.2f}°C | "
        f"Humidity: {node.humidity_pct:5.2f}% | "
        f"Wind: {node.wind_speed_m_s:5.2f} m/s | "
        f"Soil: {node.soil_moisture_pct:5.2f}% | "
        f"Smoke: {node.smoke_level:6.2f} | "
        f"State: {node.hazard_state}"
    )


print("\nTotal readings stored:", len(node.history))