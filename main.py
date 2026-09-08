from communication.network_simulator import NetworkSimulator
from communication.event_buffer import EventBuffer
from communication.sync_manager import SyncManager
from data.csv_logger import CSVLogger


# Initialize all system components
network = NetworkSimulator()
buffer = EventBuffer()
logger = CSVLogger()
sync_manager = SyncManager()


def process_event(event):
    """
    Process an incoming event based on network availability.
    """

    if network.get_status():
        print("\nNetwork ONLINE → Logging event directly to CSV")
        event["network_status"] = "ONLINE"
        logger.log_data(event)

    else:
        print("\nNetwork OFFLINE → Storing event in local buffer")
        event["network_status"] = "OFFLINE"
        buffer.add_event(event)


# --------------------------------------------------
# TEST 1: NETWORK ONLINE
# --------------------------------------------------

print("\n========== SYSTEM START ==========")
print("Network Status:", "ONLINE")


event1 = {

    # Node identity
    "timestamp": "2026-09-08 13:00:00",
    "node_id": "FLOOD_NODE_01",
    "location": "River Zone A",

    # Common environmental observations
    "rainfall_mm_h": 45,
    "temperature_c": 28,
    "humidity_pct": 82,
    "soil_moisture_pct": 70,

    # Flood
    "water_level_m": 2.5,

    # Fire
    "wind_speed_m_s": 0.0,
    "smoke_level": 0.0,

    # Gas
    "gas_level": 0.0,

    # Landslide
    "soil_stability": 0.85,

    # Intelligence
    "rate_of_rise_m_h": 0.4,
    "trend": "RISING",
    "risk_score": 45,
    "risk_level": "MEDIUM",
    "hazard_state": "DEVELOPING",
    "event_state": "NORMAL",

    # System
    "network_status": "",
    "edge_processing": "ACTIVE"
}


process_event(event1)


# --------------------------------------------------
# TEST 2: NETWORK FAILURE
# --------------------------------------------------

print("\n========== NETWORK FAILURE ==========")

network.turn_off()


event2 = {

    # Node identity
    "timestamp": "2026-09-08 13:05:00",
    "node_id": "FLOOD_NODE_01",
    "location": "River Zone A",

    # Common environmental observations
    "rainfall_mm_h": 95,
    "temperature_c": 27,
    "humidity_pct": 90,
    "soil_moisture_pct": 92,

    # Flood
    "water_level_m": 4.3,

    # Fire
    "wind_speed_m_s": 0.0,
    "smoke_level": 0.0,

    # Gas
    "gas_level": 0.0,

    # Landslide
    "soil_stability": 0.45,

    # Intelligence
    "rate_of_rise_m_h": 1.8,
    "trend": "RISING",
    "risk_score": 92,
    "risk_level": "CRITICAL",
    "hazard_state": "CRITICAL",
    "event_state": "ACTIVE",

    # System
    "network_status": "",
    "edge_processing": "ACTIVE"
}


process_event(event2)


# --------------------------------------------------
# TEST 3: NETWORK RESTORATION
# --------------------------------------------------

print("\n========== NETWORK RESTORED ==========")

network.turn_on()


# Synchronize buffered events
sync_manager.synchronize()


print("\n========== FINAL STATUS ==========")
print("Network:", "ONLINE")
print("Buffered Events:", buffer.get_events())
print("System Test Completed Successfully.")