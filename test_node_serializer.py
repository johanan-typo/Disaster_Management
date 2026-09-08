from engines.node_model import VirtualNode
from utils.node_serializer import node_to_dict


# Create a VirtualNode
node = VirtualNode(
    node_id="FLOOD_NODE_01",
    location="River Zone A",
    rainfall_mm_h=85,
    temperature_c=27,
    humidity_pct=90,
    soil_moisture_pct=88,
    water_level_m=3.8,
    wind_speed_m_s=2.5,
    smoke_level=0.0,
    gas_level=0.0,
    soil_stability=0.65
)


# Add intelligence values
node.rate_of_rise_m_h = 1.2
node.trend = "RISING"
node.risk_score = 85
node.risk_level = "HIGH"
node.hazard_state = "DEVELOPING"
node.event_state = "ACTIVE"


# Convert VirtualNode to dictionary
event_data = node_to_dict(node)


print("\n===== VIRTUAL NODE =====")
print(node)

print("\n===== SERIALIZED DATA =====")

for key, value in event_data.items():
    print(f"{key}: {value}")