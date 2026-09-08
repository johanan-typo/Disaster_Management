from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class VirtualNode:
    """
    Digital representation of one environmental monitoring node.

    The node stores raw environmental observations and local
    processing state. Hazard-specific engines generate the
    environmental conditions; intelligence modules interpret them.
    """

    # Node identity
    node_id: str
    location: str

    # Common environmental observations
    rainfall_mm_h: float = 0.0
    temperature_c: float = 0.0
    humidity_pct: float = 0.0
    soil_moisture_pct: float = 0.0

    # Flood-related observation
    water_level_m: float = 0.0

    # Fire-related observations
    wind_speed_m_s: float = 0.0
    smoke_level: float = 0.0

    # Gas / air-quality related observation
    gas_level: float = 0.0

    # Landslide-related observation
    soil_stability: float = 1.0

    # System state
    timestamp: datetime = field(default_factory=datetime.now)
    network_status: str = "ONLINE"
    edge_processing: str = "ACTIVE"

    # Local intelligence state
    rate_of_rise_m_h: float = 0.0
    trend: str = "STABLE"
    risk_score: float = 0.0
    risk_level: str = "NORMAL"
    hazard_state: str = "NORMAL"
    event_state: str = "NORMAL"

    # Temporal history
    history: List[Dict] = field(default_factory=list)

    def add_reading(self):
        """Store the current environmental reading locally."""

        self.history.append({
            "timestamp": self.timestamp,
            "rainfall_mm_h": self.rainfall_mm_h,
            "temperature_c": self.temperature_c,
            "humidity_pct": self.humidity_pct,
            "soil_moisture_pct": self.soil_moisture_pct,
            "water_level_m": self.water_level_m,
            "wind_speed_m_s": self.wind_speed_m_s,
            "smoke_level": self.smoke_level,
            "gas_level": self.gas_level,
            "soil_stability": self.soil_stability,
        })

    def update_timestamp(self):
        """Update the node timestamp."""

        self.timestamp = datetime.now()
