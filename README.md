# 🌍 Environmental Intelligence Network

## Offline-First Multi-Hazard Environmental Intelligence & Local Risk Inference

### SIH 2026 — Phase 1 Software Prototype

> **Detect locally. Decide locally. Communicate when possible. Synchronize when connected.**

The **Environmental Intelligence Network** is an offline-first, distributed environmental intelligence platform designed for **rural, remote, and connectivity-constrained environments**. The system is designed around a simple principle: critical environmental intelligence should continue to operate even when communication infrastructure becomes unavailable.

The platform combines environmental sensing, temporal reasoning, sensor fusion, deterministic risk assessment, local Edge AI, offline event buffering, store-and-forward synchronization, CSV-based data logging, and a real-time web dashboard into a single modular architecture.

The Phase 1 prototype primarily validates the **flood intelligence pipeline**, while the overall architecture is designed to support additional hazards such as **wildfire and landslide**.

---

## 🚨 Problem

Environmental monitoring and disaster-management systems frequently depend on continuous connectivity for sensor data transmission, centralized processing, alert generation, dashboards, and communication with remote servers.

However, during severe environmental events, communication infrastructure may become unreliable or unavailable.

This creates a critical problem:

    NETWORK FAILURE
           ↓
    DATA TRANSMISSION STOPS
           ↓
    CENTRAL SYSTEM LOSES REAL-TIME DATA
           ↓
    DELAYED DECISION

The Environmental Intelligence Network follows an offline-first approach:

    NETWORK FAILURE
           ↓
    LOCAL PROCESSING CONTINUES
           ↓
    LOCAL RISK ASSESSMENT
           ↓
    LOCAL ALERT
           ↓
    EVENT BUFFERED
           ↓
    NETWORK RESTORED
           ↓
    EVENT SYNCHRONIZED

Therefore, network failure affects communication but does not stop local environmental intelligence.

---

## 🎯 Objectives

The primary objective of the project is to create a resilient environmental intelligence architecture capable of operating under both normal connectivity and communication outage conditions.

The system is designed to provide:

- Distributed environmental monitoring
- Local environmental processing
- Temporal analysis of changing conditions
- Multi-parameter sensor fusion
- Deterministic and explainable risk assessment
- Local Edge AI response selection
- Offline-first operation
- Local event buffering
- Store-and-forward synchronization
- CSV-based environmental logging
- Real-time web-based monitoring
- 3D flood visualization
- Multi-hazard extensibility
- A foundation for future physical sensor deployment

---

## 🧠 System Architecture

The Environmental Intelligence Network is divided into multiple modular layers.

    ENVIRONMENTAL INPUTS
            ↓
    VIRTUAL ENVIRONMENTAL NODES
            ↓
    TEMPORAL INTELLIGENCE
            ↓
    SENSOR FUSION
            ↓
    DETERMINISTIC RISK ENGINE
            ↓
    LOCAL EDGE AI
            ↓
    ONLINE / OFFLINE COMMUNICATION
            ↓
    EVENT BUFFERING
            ↓
    STORE-AND-FORWARD SYNCHRONIZATION
            ↓
    CSV LOGGING
            ↓
    FASTAPI BACKEND
            ↓
    WEBSOCKET STREAM
            ↓
    REACT WEB DASHBOARD

The architecture separates environmental simulation, intelligence processing, communication, storage, backend services, and visualization.

This makes individual modules easier to test, replace, and extend.

---

## 🌐 Distributed Environmental Nodes

The Phase 1 software prototype contains five virtual environmental nodes representing different geographical deployment conditions.

| Node | Location | Purpose |
|---|---|---|
| Node A | Upstream | Monitors incoming environmental conditions |
| Node B | Downstream | Monitors downstream flood response |
| Node C | Village | Represents a populated region |
| Node D | Low-Risk Area | Represents a comparatively safer region |
| Node E | Critical Community | Represents a high-priority community |

Each node maintains environmental measurements and intelligence state information.

The node model includes parameters such as:

- Rainfall
- Temperature
- Humidity
- Soil moisture
- Water level
- Wind speed
- Smoke level
- Gas level
- Soil stability
- Rate of rise
- Trend
- Risk score
- Risk level
- Hazard state
- Event state
- Network status
- Edge-processing status
- Timestamp
- Historical readings

This allows each node to behave as an independent environmental intelligence unit.

---

## 🌧️ Flood Intelligence

Flood is the primary validated hazard for the SIH 2026 Phase 1 prototype.

The Flood Engine models changing water conditions using environmental inputs such as:

- Rainfall
- Soil moisture
- Water level
- Rate of water-level change

The flood state can transition through conditions such as:

    NORMAL
       ↓
    RAINSTORM
       ↓
    RISING
       ↓
    FLOOD

The system also supports a recovery condition where water levels begin to decrease.

The important design principle is that the system does not rely only on a single water-level threshold.

Instead, it considers the current environmental state together with the rate and persistence of change.

---

## 📈 Temporal Intelligence

Environmental hazards are dynamic.

A single sensor reading cannot always determine whether a dangerous condition is developing.

The Temporal Intelligence layer analyzes historical readings to determine how the environmental condition is evolving.

The system calculates:

- Rate of rise
- Trend
- Persistence

The trend is classified as:

    RISING
    STABLE
    FALLING

For example:

    WATER LEVEL INCREASE
            ↓
    RATE OF RISE INCREASE
            ↓
    RISING TREND
            ↓
    PERSISTENT RISE
            ↓
    DEVELOPING FLOOD CONDITION

This temporal layer allows the system to distinguish between an isolated measurement and a sustained environmental change.

---

## 🔀 Sensor Fusion

The Sensor Fusion layer combines multiple environmental indicators into a single evidence score.

The current flood intelligence pipeline uses the following weighting:

| Parameter | Weight |
|---|---:|
| Water Level | 0.30 |
| Rainfall | 0.20 |
| Rate of Rise | 0.25 |
| Soil Moisture | 0.15 |
| Persistence | 0.10 |

The combined evidence score is passed to the deterministic Risk Engine.

This provides a multi-parameter assessment rather than depending on one environmental variable.

The approach also makes the risk calculation explainable because each contributing parameter has a defined role in the final score.

---

## ⚠️ Deterministic Risk Engine

The Risk Engine is the authoritative decision layer for environmental risk.

It converts the fused evidence score into four risk levels:

    NORMAL
    WATCH
    WARNING
    CRITICAL

The current thresholds are:

| Risk Level | Threshold |
|---|---:|
| WATCH | ≥ 0.30 |
| WARNING | ≥ 0.55 |
| CRITICAL | ≥ 0.75 |

The Risk Engine also considers environmental trends, persistence, water level, rainfall, rate of rise, and soil moisture when determining the current environmental and event state.

The system separates:

- Risk level
- Hazard state
- Event state
- Local response

This separation is important because environmental assessment and response selection are different responsibilities.

The Risk Engine remains authoritative even when Edge AI is active.

---

## 🚨 Event Intelligence

The system represents the evolution of an environmental event using event states such as:

    NORMAL
    DEVELOPING
    DETECTED
    PROPAGATING

This allows the system to represent more than simply "safe" or "dangerous."

For example:

    NORMAL
       ↓
    DEVELOPING
       ↓
    DETECTED
       ↓
    PROPAGATING

The event state can therefore be used by the communication layer to determine whether an event should be transmitted, buffered, or synchronized.

---

## 🤖 Local Edge AI

The project integrates **Needle** as a constrained local Edge AI action-selection layer.

Edge AI is not used to replace the deterministic environmental intelligence pipeline.

It does not:

- Calculate flood physics
- Generate water-level measurements
- Replace sensor fusion
- Replace the Risk Engine
- Invent sensor information
- Override the deterministic risk level

Instead, Edge AI receives an already-computed environmental state and selects an appropriate local response.

The response mapping is:

    NORMAL   → NO_ACTION
    WATCH    → LOCAL_ALERT
    WARNING  → LOCAL_ALERT
    CRITICAL → CRITICAL_LOCAL_ALERT

The architecture is therefore:

    ENVIRONMENTAL DATA
            ↓
    TEMPORAL INTELLIGENCE
            ↓
    SENSOR FUSION
            ↓
    RISK ENGINE
            ↓
    DETERMINISTIC RISK
            ↓
    EDGE AI
            ↓
    LOCAL RESPONSE

This constrained approach prevents the Edge AI layer from becoming the authoritative source of safety-critical environmental decisions.

---

## 📡 Offline-First Communication

One of the main characteristics of the project is that environmental intelligence continues to operate when the network becomes unavailable.

### Online Mode

During normal connectivity:

    ENVIRONMENTAL DATA
            ↓
    LOCAL PROCESSING
            ↓
    RISK ASSESSMENT
            ↓
    EVENT GENERATION
            ↓
    NETWORK TRANSMISSION
            ↓
    CSV LOGGING

### Offline Mode

When the network is disabled:

    ENVIRONMENTAL DATA
            ↓
    LOCAL PROCESSING
            ↓
    RISK ASSESSMENT
            ↓
    LOCAL ALERT
            ↓
    EVENT BUFFER
            ↓
    CONTINUE PROCESSING

The network outage therefore does not stop the local intelligence pipeline.

---

## 💾 Event Buffering

Actionable environmental events generated during network outages are stored locally in the Event Buffer.

The purpose is to prevent important environmental events from being lost simply because communication is temporarily unavailable.

The architecture follows:

    EVENT DETECTED
          ↓
    NETWORK OFFLINE
          ↓
    STORE EVENT LOCALLY
          ↓
    CONTINUE MONITORING
          ↓
    NETWORK RESTORED
          ↓
    SYNCHRONIZE EVENTS

This is the foundation of the store-and-forward mechanism.

---

## 🔄 Store-and-Forward Synchronization

When network connectivity is restored, buffered events are synchronized.

    OFFLINE EVENTS
          ↓
    LOCAL EVENT BUFFER
          ↓
    NETWORK RESTORED
          ↓
    SYNCHRONIZATION
          ↓
    TRANSMISSION
          ↓
    CSV LOGGING
          ↓
    BUFFER CLEARED

The synchronization mechanism ensures that events generated during an outage can be transferred after communication becomes available again.

This separates local intelligence from network availability.

---

## 💾 CSV Data Logging

The project includes a CSV logging layer for recording environmental and intelligence information.

Important fields include:

    timestamp
    node_id
    location
    rainfall_mm_h
    temperature_c
    humidity_pct
    soil_moisture_pct
    water_level_m
    wind_speed_m_s
    smoke_level
    gas_level
    soil_stability
    rate_of_rise_m_h
    trend
    risk_score
    risk_level
    hazard_state
    event_state
    network_status
    edge_processing

The CSV data can be used for:

- Validation
- Debugging
- Demonstration
- Environmental analysis
- Historical inspection
- Future machine-learning development
- System performance evaluation

The CSV also provides a clear way to demonstrate how environmental measurements evolve into intelligence and decisions.

---

## 🖥️ Frontend

The web dashboard is built using **React and Vite**.

The frontend provides the user interface for monitoring and controlling the Environmental Intelligence Network.

The frontend contains:

- Node monitoring cards
- Risk overview
- Alert panel
- Network controller
- Simulation controls
- Synchronization status
- System information
- Edge AI status
- 3D flood visualization

Frontend structure:

    dashboard/frontend/
    ├── src/
    │   ├── components/
    │   │   ├── AlertPanel.jsx
    │   │   ├── NetworkController.jsx
    │   │   ├── NodeCard.jsx
    │   │   ├── RiskOverview.jsx
    │   │   ├── SimulationControls.jsx
    │   │   ├── SyncStatusBanner.jsx
    │   │   └── TopBar.jsx
    │   │
    │   ├── hooks/
    │   │   ├── useSimulationStream.js
    │   │   └── useSystemTime.js
    │   │
    │   ├── three/
    │   │   └── FloodWater3D.jsx
    │   │
    │   ├── styles/
    │   │   └── theme.css
    │   │
    │   ├── App.jsx
    │   └── main.jsx
    │
    ├── index.html
    ├── package.json
    ├── package-lock.json
    └── vite.config.js

The dashboard uses dynamic system time rather than relying only on simulation time.

Simulation time is maintained separately so that environmental progression can be demonstrated independently from the actual system clock.

---

## 🌊 3D Flood Visualization

The dashboard includes a Three.js-based 3D flood visualization.

The visualization represents changing water conditions using:

- Water-level variation
- Surface movement
- Wave motion
- Flow variation
- Visual flood severity

The 3D visualization is connected to the underlying simulation state.

The visualization is intended to make environmental changes easier to understand during demonstrations while the actual risk decision remains controlled by the intelligence pipeline.

The flood visualization is implemented in:

    dashboard/frontend/src/three/FloodWater3D.jsx

---

## 🌐 Backend

The dashboard backend is implemented using **FastAPI**.

Backend structure:

    dashboard/backend/
    ├── api.py
    └── run_server.py

The backend acts as the bridge between the Python environmental intelligence system and the React dashboard.

The API provides endpoints including:

    GET  /api/nodes
    GET  /api/network
    POST /api/simulation/step

Real-time updates are provided through:

    WebSocket /ws

The communication architecture is:

    ENVIRONMENTAL SIMULATION
            ↓
       FASTAPI BACKEND
            ↓
        WEBSOCKET
            ↓
       REACT FRONTEND
            ↓
     REAL-TIME DASHBOARD

This allows the dashboard to display changing environmental conditions and system states without requiring constant page refreshes.

---

## 🎮 Simulation Scenarios

The prototype provides controlled scenarios for demonstration and validation.

Available scenarios include:

    NORMAL
    DEVELOPING
    SEVERE
    CRITICAL
    RECOVERY

A complete demonstration sequence can be:

    NORMAL
       ↓
    DEVELOPING
       ↓
    SEVERE
       ↓
    CRITICAL
       ↓
    NETWORK OFFLINE
       ↓
    LOCAL PROCESSING
       ↓
    EVENT BUFFERING
       ↓
    NETWORK ONLINE
       ↓
    EVENT SYNCHRONIZATION
       ↓
    RECOVERY

This sequence demonstrates the complete lifecycle of the system.

---

## 🌋 Multi-Hazard Architecture

Although flood is the primary validated hazard in Phase 1, the repository is structured for multi-hazard expansion.

The architecture includes engines for:

- Flood
- Wildfire
- Landslide

The long-term objective is to allow different hazard-specific engines to share common intelligence and communication infrastructure.

The general architecture is:

    ENVIRONMENTAL INPUTS
            ↓
        HAZARD ENGINE
            ↓
    TEMPORAL INTELLIGENCE
            ↓
       SENSOR FUSION
            ↓
       RISK ENGINE
            ↓
        EDGE AI
            ↓
      COMMUNICATION
            ↓
        DASHBOARD

This makes it possible to extend the same platform to multiple environmental threats.

---

## 🧪 Testing and Validation

The project contains multiple component-level and integration tests.

Important test files include:

    test_csv_integration.py
    test_dashboard_integration.py
    test_edge_ai.py
    test_edge_ai_mapping.py
    test_environment.py
    test_flood_integration.py
    test_landslide_integration.py
    test_needle.py
    test_node_serializer.py
    test_offline_resilience.py
    test_runner_integration.py
    test_wildfire_integration.py

The tests cover areas such as:

- Environmental simulation
- Virtual nodes
- Flood processing
- Wildfire integration
- Landslide integration
- CSV logging
- Node serialization
- Edge AI
- Edge AI response mapping
- Needle integration
- Dashboard integration
- Offline resilience
- Event buffering
- Synchronization
- Store-and-forward behavior

Testing can be performed using:

    pytest

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Frontend Language | JavaScript / JSX |
| Frontend Framework | React |
| Frontend Build Tool | Vite |
| Backend | FastAPI |
| Real-Time Communication | WebSocket |
| 3D Visualization | Three.js |
| Numerical Processing | NumPy |
| Data Processing | Pandas |
| Visualization | Plotly / Matplotlib |
| Local Edge AI | Needle |
| Data Logging | CSV |
| Testing | Pytest |
| Version Control | Git |
| Repository | GitHub |

---

## 📁 Repository Structure

    Disaster_Management/
    │
    ├── communication/
    │   ├── network_simulator.py
    │   ├── event_buffer.py
    │   ├── event_manager.py
    │   └── sync_manager.py
    │
    ├── dashboard/
    │   ├── backend/
    │   │   ├── api.py
    │   │   └── run_server.py
    │   │
    │   └── frontend/
    │       ├── src/
    │       ├── index.html
    │       ├── package.json
    │       ├── package-lock.json
    │       └── vite.config.js
    │
    ├── data/
    │   └── csv_logger.py
    │
    ├── engines/
    │   ├── node_model.py
    │   ├── random_environment.py
    │   ├── flood_engine.py
    │   ├── wildfire_engine.py
    │   └── landslide_engine.py
    │
    ├── intelligence/
    │   ├── temporal_engine.py
    │   ├── sensor_fusion.py
    │   ├── risk_engine.py
    │   └── edge_ai.py
    │
    ├── scripts/
    │
    ├── simulation/
    │   └── simulation_runner.py
    │
    ├── utils/
    │
    ├── main.py
    │
    └── test_*.py

---

## 🚀 Installation

Clone the repository:

    git clone https://github.com/johanan-typo/Disaster_Management.git

Enter the project directory:

    cd Disaster_Management

Create the Python virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

Install the required Python dependencies.

The frontend dependencies can be installed using:

    cd dashboard/frontend
    npm install

---

## ▶️ Running the Backend

From the project root, start the FastAPI backend:

    python dashboard/backend/run_server.py

The backend will be available at:

    http://localhost:8000

---

## ▶️ Running the Frontend

Open another terminal:

    cd dashboard/frontend
    npm install
    npm run dev

The dashboard will be available at:

    http://localhost:5173/

The frontend communicates with the FastAPI backend and receives real-time simulation updates through WebSocket communication.

---

## 🎬 Recommended Demonstration Flow

For an SIH demonstration, the system can be presented as a complete environmental intelligence lifecycle.

### Step 1 — Normal Environment

Start the system in:

    NORMAL

All five nodes operate normally.

The dashboard displays:

- Node status
- Environmental measurements
- Risk levels
- Network status
- Edge processing status

### Step 2 — Increasing Environmental Stress

Change the scenario to:

    DEVELOPING

Rainfall and environmental conditions begin to increase.

The system begins observing:

    RAINFALL ↑
       ↓
    WATER LEVEL ↑
       ↓
    RATE OF RISE ↑
       ↓
    RISING TREND
       ↓
    INCREASING RISK

### Step 3 — Severe Condition

Change the scenario to:

    SEVERE

Sensor fusion produces stronger environmental evidence and the Risk Engine increases the risk level.

### Step 4 — Critical Condition

Change the scenario to:

    CRITICAL

The system produces critical environmental states and Edge AI selects the appropriate local critical response.

### Step 5 — Network Failure

Switch the network controller to:

    OFFLINE

The communication layer becomes unavailable.

However:

    LOCAL PROCESSING = ACTIVE

The nodes continue processing environmental conditions.

### Step 6 — Event Buffering

Actionable events generated while offline are stored in the local Event Buffer.

The dashboard displays the offline and synchronization state.

### Step 7 — Network Recovery

Switch the network back to:

    ONLINE

The system synchronizes buffered events.

Buffered events are transmitted and logged.

### Step 8 — Recovery

Switch the environmental scenario to:

    RECOVERY

The environmental condition begins moving toward a safer state.

This demonstrates:

    DETECTION
        ↓
    LOCAL DECISION
        ↓
    OFFLINE OPERATION
        ↓
    EVENT STORAGE
        ↓
    NETWORK RECOVERY
        ↓
    SYNCHRONIZATION
        ↓
    RECOVERY

---

## 💡 What Makes the System Different?

The project does not claim that individual technologies such as sensor fusion, Edge AI, WebSockets, flood simulation, or offline storage are individually new.

The key engineering focus is their integration into a single offline-first environmental intelligence architecture.

The central design principle is:

> **Critical environmental intelligence should not depend entirely on network availability.**

The system therefore separates:

    SENSING
       ↓
    INTELLIGENCE
       ↓
    DECISION
       ↓
    COMMUNICATION

Communication is treated as an additional layer rather than a prerequisite for local intelligence.

This allows the system to continue operating during communication outages and synchronize information once connectivity is restored.

---

## 🔐 Design Principles

### Local Intelligence

Environmental processing and risk assessment should be capable of running locally.

### Deterministic Safety Layer

The Risk Engine remains authoritative and explainable.

### Constrained AI

Edge AI is used for response selection rather than replacing deterministic environmental decisions.

### Offline Resilience

Network failure should not stop local environmental intelligence.

### Store-and-Forward

Important events should be preserved during outages and synchronized after connectivity returns.

### Modular Architecture

Hazard engines, intelligence modules, communication, data logging, backend, and frontend are separated.

### Extensibility

The system can evolve from a software prototype into a distributed physical environmental intelligence network.

---

## 🛣️ Future Roadmap

### Phase 2 — Physical Sensor Integration

The next stage can replace virtual environmental inputs with real sensors.

Potential platforms include:

- ESP32
- STM32
- Environmental sensor nodes
- Water-level sensors
- Rainfall sensors
- Soil-moisture sensors
- Temperature and humidity sensors
- Smoke sensors
- Gas sensors
- Soil-stability sensors

The existing software architecture can act as the intelligence layer for these physical nodes.

---

### Phase 3 — Multi-Hazard Physical Deployment

Extend the system to real-world sensing for:

    FLOOD
    WILDFIRE
    LANDSLIDE
    GAS / ENVIRONMENTAL HAZARDS

Each hazard can have its own environmental engine while sharing the common intelligence and communication architecture.

---

### Phase 4 — Embedded Edge Intelligence

Move selected processing components from the software simulation to embedded platforms.

Potential platforms include:

- ESP32
- STM32
- FPGA
- Edge SoC

This can reduce dependence on centralized computing and enable real-world local inference.

---

### Phase 5 — Distributed Environmental Intelligence Network

The long-term architecture is a network of independent environmental nodes capable of:

- Local sensing
- Local processing
- Local risk assessment
- Local alerts
- Offline operation
- Event buffering
- Store-and-forward communication
- Central synchronization

The final architecture can therefore operate as a distributed environmental intelligence system rather than simply a centralized monitoring dashboard.

---

## 👥 Team Members

### SIH 2026 — Environmental Intelligence Network

| Team Member |
|---|
| **Johanan** |
| **Aslyn Fiona** |
| **Jeffrin S Raaj** |
| **R Jeberson** |
| **Sushitra** |
| **Aparna** |

---

## 🏆 SIH 2026 — Phase 1 Status

The Phase 1 software prototype includes:

    Environmental Simulation       ✓
    Virtual Environmental Nodes    ✓
    Flood Intelligence             ✓
    Temporal Analysis              ✓
    Sensor Fusion                  ✓
    Deterministic Risk Engine      ✓
    Edge AI Integration            ✓
    Offline Processing             ✓
    Event Buffering                ✓
    Store-and-Forward               ✓
    Synchronization                ✓
    CSV Logging                    ✓
    FastAPI Backend                ✓
    React Frontend                 ✓
    WebSocket Streaming            ✓
    3D Flood Visualization         ✓
    Scenario Simulation             ✓
    Integration Testing             ✓

---

## 📊 Complete Intelligence Flow

The complete Phase 1 system can be summarized as:

    ENVIRONMENTAL CONDITIONS
             ↓
    VIRTUAL ENVIRONMENTAL NODES
             ↓
    ENVIRONMENTAL MEASUREMENTS
             ↓
    TEMPORAL ANALYSIS
             ↓
    RATE OF RISE + TREND + PERSISTENCE
             ↓
    SENSOR FUSION
             ↓
    EVIDENCE SCORE
             ↓
    DETERMINISTIC RISK ENGINE
             ↓
    NORMAL / WATCH / WARNING / CRITICAL
             ↓
    EVENT STATE
             ↓
    LOCAL EDGE AI
             ↓
    LOCAL RESPONSE
             ↓
    ┌─────────────────────────────┐
    │                             │
    │       NETWORK ONLINE        │
    │             ↓               │
    │       TRANSMIT + LOG        │
    │                             │
    │       NETWORK OFFLINE       │
    │             ↓               │
    │       LOCAL PROCESSING      │
    │             ↓               │
    │       EVENT BUFFER          │
    │             ↓               │
    │       NETWORK RESTORED      │
    │             ↓               │
    │       SYNCHRONIZATION       │
    │                             │
    └─────────────────────────────┘
             ↓
       FASTAPI BACKEND
             ↓
        WEBSOCKET
             ↓
       REACT DASHBOARD
             ↓
      REAL-TIME MONITORING
             ↓
       3D FLOOD VIEW

---

## 🌍 Final Vision

The Environmental Intelligence Network is designed as a foundation for resilient environmental monitoring where **connectivity is helpful but not a prerequisite for intelligence**.

The system demonstrates how distributed environmental nodes can continue to monitor conditions, analyze temporal changes, combine multiple environmental indicators, determine risk locally, generate local responses, buffer events during outages, and synchronize information after connectivity is restored.

The Phase 1 prototype establishes the software foundation for future integration with real environmental sensors, embedded platforms, distributed communication technologies, and multi-hazard deployments.

---

# 🌍 Environmental Intelligence Network

### Detect locally.
### Decide locally.
### Communicate when possible.
### Synchronize when connected.

**SIH 2026 — Phase 1 Software Prototype**

**Team:** Johanan • Aslyn Fiona • Jeffrin S Raaj • R Jeberson • Sushitra • Aparna

**Repository:** https://github.com/johanan-typo/Disaster_Management
