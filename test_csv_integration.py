from engines.node_model import VirtualNode
from utils.node_serializer import node_to_dict
from data.csv_logger import CSVLogger


# Create a virtual flood monitoring node
node = VirtualNode(
    node_id="FLOOD_NODE_01",
    location="River Zone A",

    rainfall_mm_h=55.0,
    temperature_c=28.0,
    humidity_pct=90.0,
    soil_moisture_pct=78.0,

    water_level_m=3.2,

    wind_speed_m_s=4.5,
    smoke_level=0.0,

    gas_level=0.0,

    soil_stability=0.72,

    rate_of_rise_m_h=0.8,
    trend="RISING",
    risk_score=82.0,
    risk_level="HIGH",
    hazard_state="DEVELOPING",
    event_state="ACTIVE",

    network_status="ONLINE",
    edge_processing="ACTIVE"
)


# Convert VirtualNode to dictionary
node_data = node_to_dict(node)


# Create CSV logger
logger = CSVLogger()


# Log data
logger.log_data(node_data)


print("\nCSV Integration Test Completed Successfully.")