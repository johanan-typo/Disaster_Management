def node_to_dict(node):
    """
    Convert a VirtualNode object into a dictionary
    suitable for CSV logging and JSON event buffering.
    """

    return {

        # Node identity
        "timestamp": node.timestamp.isoformat(),
        "node_id": node.node_id,
        "location": node.location,

        # Common environmental observations
        "rainfall_mm_h": node.rainfall_mm_h,
        "temperature_c": node.temperature_c,
        "humidity_pct": node.humidity_pct,
        "soil_moisture_pct": node.soil_moisture_pct,

        # Flood-related observation
        "water_level_m": node.water_level_m,

        # Fire-related observations
        "wind_speed_m_s": node.wind_speed_m_s,
        "smoke_level": node.smoke_level,

        # Gas observation
        "gas_level": node.gas_level,

        # Landslide observation
        "soil_stability": node.soil_stability,

        # Intelligence state
        "rate_of_rise_m_h": node.rate_of_rise_m_h,
        "trend": node.trend,
        "risk_score": node.risk_score,
        "risk_level": node.risk_level,
        "hazard_state": node.hazard_state,
        "event_state": node.event_state,

        # System state
        "network_status": node.network_status,
        "edge_processing": node.edge_processing
    }