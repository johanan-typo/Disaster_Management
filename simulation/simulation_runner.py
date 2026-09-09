"""
Environmental Intelligence Network
-----------------------------------

Stage-1 simulation runner for the Environmental Intelligence Network.

Architecture:

    RandomEnvironment
            ↓
       FloodEngine
            ↓
        VirtualNode
            ↓
      TemporalEngine
            ↓
       SensorFusion
            ↓
        RiskEngine
            ↓
       EventManager
            ↓
    NetworkSimulator
       ↙          ↘
    ONLINE       OFFLINE
      ↓             ↓
   CSVLogger    EventBuffer
                    ↓
              Network restored
                    ↓
              Store-and-forward

This is a software simulation / proof of concept.

The local risk engine is a transparent engineering rule set,
not a trained prediction model.
"""

from datetime import datetime, timedelta

from engines.node_model import VirtualNode
from engines.random_environment import RandomEnvironment
from engines.flood_engine import FloodEngine

from intelligence.temporal_engine import TemporalEngine
from intelligence.sensor_fusion import SensorFusion
from intelligence.risk_engine import RiskEngine

from communication.network_simulator import NetworkSimulator
from communication.event_buffer import EventBuffer
from communication.event_manager import EventManager

from data.csv_logger import CSVLogger


class EnvironmentalIntelligenceNetwork:
    """
    Main Stage-1 environmental intelligence simulation.

    Five virtual monitoring nodes are processed independently.

    The system demonstrates:

        1. Environmental sensing
        2. Flood condition generation
        3. Temporal analysis
        4. Multi-parameter sensor fusion
        5. Local risk inference
        6. Event management
        7. Network resilience
        8. Offline event buffering
        9. Store-and-forward synchronization
        10. CSV logging
    """

    TIME_STEP_HOURS = 1.0

    def __init__(self):
        # ---------------------------------------------------------
        # SIMULATION CLOCK
        # ---------------------------------------------------------

        self.simulation_time = datetime.now().replace(
            minute=0,
            second=0,
            microsecond=0,
        )

        self.step_number = 0

        # ---------------------------------------------------------
        # INTELLIGENCE COMPONENTS
        # ---------------------------------------------------------

        self.temporal_engine = TemporalEngine(
            history_window=5
        )

        self.sensor_fusion = SensorFusion()

        self.risk_engine = RiskEngine()

        # ---------------------------------------------------------
        # COMMUNICATION / RESILIENCE
        # ---------------------------------------------------------

        self.network = NetworkSimulator()

        self.event_manager = EventManager()

        self.event_buffer = EventBuffer()

        # ---------------------------------------------------------
        # DATA STORAGE
        # ---------------------------------------------------------

        self.csv_logger = CSVLogger(
            "data/sensor_data.csv"
        )

        # ---------------------------------------------------------
        # VIRTUAL NODES
        # ---------------------------------------------------------

        self.nodes = [
            VirtualNode(
                node_id="A",
                location="Upstream",
                water_level_m=0.60,
            ),

            VirtualNode(
                node_id="B",
                location="Downstream",
                water_level_m=0.50,
            ),

            VirtualNode(
                node_id="C",
                location="Village",
                water_level_m=0.40,
            ),

            VirtualNode(
                node_id="D",
                location="Low-Risk Area",
                water_level_m=0.30,
            ),

            VirtualNode(
                node_id="E",
                location="Critical Community",
                water_level_m=0.70,
            ),
        ]

        # ---------------------------------------------------------
        # ENVIRONMENT GENERATORS
        # ---------------------------------------------------------

        self.environments = {
            "A": RandomEnvironment(seed=42),
            "B": RandomEnvironment(seed=43),
            "C": RandomEnvironment(seed=44),
            "D": RandomEnvironment(seed=45),
            "E": RandomEnvironment(seed=46),
        }

        # ---------------------------------------------------------
        # FLOOD ENGINES
        # ---------------------------------------------------------

        self.flood_engines = {
            "A": FloodEngine(initial_water_level=0.60),
            "B": FloodEngine(initial_water_level=0.50),
            "C": FloodEngine(initial_water_level=0.40),
            "D": FloodEngine(initial_water_level=0.30),
            "E": FloodEngine(initial_water_level=0.70),
        }

        # ---------------------------------------------------------
        # SCENARIO CONTROL
        # ---------------------------------------------------------

        self.rainstorm_active = False

        # Controlled Stage-1 demonstration scenario.
        #
        # NORMAL
        # DEVELOPING
        # SEVERE
        # CRITICAL
        # RECOVERY
        self.scenario_phase = "NORMAL"

    # =============================================================
    # NETWORK CONTROL
    # =============================================================

    def network_on(self):
        """
        Restore network connectivity.

        Any events accumulated while offline are synchronized.
        """

        was_offline = not self.network.is_online()

        self.network.turn_on()

        for node in self.nodes:
            node.network_status = "ONLINE"

        print()
        print("=" * 80)
        print("NETWORK RESTORED")
        print("ONLINE")
        print("Edge processing remains active.")
        print("=" * 80)

        if was_offline:
            self.synchronize_buffer()

        print()

    def network_off(self):
        """
        Simulate network failure.

        Local edge processing continues and actionable events
        are buffered locally.
        """

        self.network.turn_off()

        for node in self.nodes:
            node.network_status = "OFFLINE"

        print()
        print("=" * 80)
        print("NETWORK FAILURE SIMULATED")
        print("NETWORK OFFLINE")
        print("EDGE PROCESSING ACTIVE")
        print("LOCAL ALERTS ACTIVE")
        print("ACTIONABLE EVENTS WILL BE BUFFERED")
        print("=" * 80)
        print()

    # =============================================================
    # RAINSTORM CONTROL
    # =============================================================

    def start_rainstorm(self):
        """
        Start rainstorm mode in all flood engines.
        """

        self.rainstorm_active = True

        for flood_engine in self.flood_engines.values():
            flood_engine.start_rainstorm()

        print()
        print("=" * 80)
        print("RAINFALL EVENT STARTED")
        print("Flood engines entering rainstorm mode.")
        print("=" * 80)
        print()

    def stop_rainstorm(self):
        """
        Stop the rainstorm.

        Water levels may subsequently begin to recede depending
        on the simulated environmental conditions.
        """

        self.rainstorm_active = False

        for flood_engine in self.flood_engines.values():
            flood_engine.stop_rainstorm()

        print()
        print("=" * 80)
        print("RAINFALL EVENT STOPPED")
        print("Flood engines returning to normal/recession behavior.")
        print("=" * 80)
        print()

    # =============================================================
    # CONTROLLED STAGE-1 FLOOD SCENARIO
    # =============================================================

    def set_scenario(self, phase):
        """
        Set a deterministic flood scenario for the Stage-1
        demonstration.

        Phases:

            NORMAL
                Background conditions.

            DEVELOPING
                Rainfall increases and soil moisture rises.

            SEVERE
                Sustained heavy rainfall and wet soil.

            CRITICAL
                Extreme rainfall and saturated soil.

            RECOVERY
                Rainfall decreases.
        """

        valid_phases = [
            "NORMAL",
            "DEVELOPING",
            "SEVERE",
            "CRITICAL",
            "RECOVERY",
        ]

        if phase not in valid_phases:
            raise ValueError(
                f"Invalid scenario phase: {phase}. "
                f"Use one of {valid_phases}"
            )

        self.scenario_phase = phase

        if phase in [
            "DEVELOPING",
            "SEVERE",
            "CRITICAL",
        ]:
            if not self.rainstorm_active:
                self.start_rainstorm()

        else:
            if self.rainstorm_active:
                self.stop_rainstorm()

        print(
            f"[SCENARIO] Flood demonstration phase: "
            f"{self.scenario_phase}"
        )

    def get_controlled_conditions(self, node):
        """
        Return deterministic rainfall and soil-moisture
        conditions for the Stage-1 flood demonstration.

        Temperature, humidity and wind remain generated by
        RandomEnvironment.

        The node parameter is intentionally retained so that
        node-specific scenario behavior can be introduced later.
        """

        phase = self.scenario_phase

        if phase == "NORMAL":
            rainfall = 5.0
            soil_moisture = 45.0

        elif phase == "DEVELOPING":
            rainfall = 35.0
            soil_moisture = 65.0

        elif phase == "SEVERE":
            rainfall = 80.0
            soil_moisture = 85.0

        elif phase == "CRITICAL":
            rainfall = 120.0
            soil_moisture = 100.0

        elif phase == "RECOVERY":
            rainfall = 5.0
            soil_moisture = 80.0

        else:
            rainfall = 5.0
            soil_moisture = 45.0

        return {
            "rainfall_mm_h": rainfall,
            "soil_moisture_pct": soil_moisture,
        }

    # =============================================================
    # ENVIRONMENT GENERATION
    # =============================================================

    def generate_environment(self, node):
        """
        Generate the current background environment for a node.

        Temperature, humidity and wind come from the normal
        RandomEnvironment generator.

        Rainfall and soil moisture are controlled by the
        Stage-1 demonstration scenario.
        """

        environment = self.environments[
            node.node_id
        ].step()

        # ---------------------------------------------------------
        # Keep background environmental variables dynamic.
        # ---------------------------------------------------------

        node.temperature_c = environment[
            "temperature_c"
        ]

        node.humidity_pct = environment[
            "humidity_pct"
        ]

        node.wind_speed_m_s = environment[
            "wind_speed_m_s"
        ]

        # ---------------------------------------------------------
        # Apply deterministic flood-demo conditions.
        # ---------------------------------------------------------

        controlled = self.get_controlled_conditions(
            node
        )

        node.rainfall_mm_h = controlled[
            "rainfall_mm_h"
        ]

        node.soil_moisture_pct = controlled[
            "soil_moisture_pct"
        ]

        environment.update(controlled)

        return environment

    # =============================================================
    # FLOOD GENERATION
    # =============================================================

    def generate_flood_state(self, node):
        """
        Generate the flood-related observation for a node.

        The normal flood behavior is generated by FloodEngine.

        During the RECOVERY phase, a controlled drainage/recession
        effect is applied so that water levels gradually decrease.
        This keeps the Stage-1 demonstration environmentally coherent
        without modifying the underlying FloodEngine implementation.
        """

        flood_engine = self.flood_engines[
            node.node_id
        ]

        # ---------------------------------------------------------
        # Normal flood-engine calculation
        # ---------------------------------------------------------

        flood_state = flood_engine.step(
            rainfall_mm_h=node.rainfall_mm_h,
            soil_moisture_pct=node.soil_moisture_pct,
        )

        water_level = flood_state[
            "water_level_m"
        ]

        rate_of_rise = flood_state[
            "rate_of_rise_m_h"
        ]

        # ---------------------------------------------------------
        # RECOVERY / DRAINAGE
        # ---------------------------------------------------------

        if self.scenario_phase == "RECOVERY":

            recovery_rate_m_h = 0.08

            previous_level = water_level

            water_level = max(
                0.0,
                water_level - recovery_rate_m_h,
            )

            # Keep FloodEngine synchronized with the adjusted
            # water level so the next timestep starts from the
            # recovered level.

            flood_engine.water_level_m = water_level

            flood_engine.previous_water_level = (
                previous_level
            )

            rate_of_rise = (
                water_level - previous_level
            )

            flood_state["water_level_m"] = round(
                water_level,
                3,
            )

            flood_state["rate_of_rise_m_h"] = round(
                rate_of_rise,
                3,
            )

            flood_state["hazard_state"] = (
                "RECEDING"
            )

        # ---------------------------------------------------------
        # Update virtual node
        # ---------------------------------------------------------

        node.water_level_m = flood_state[
            "water_level_m"
        ]

        node.rate_of_rise_m_h = flood_state[
            "rate_of_rise_m_h"
        ]

        return flood_state

    # =============================================================
    # LOCAL INTELLIGENCE
    # =============================================================

    def process_intelligence(self, node):
        """
        Execute the complete local intelligence pipeline.

        Pipeline:

            History
                ↓
            Temporal analysis
                ↓
            Sensor fusion
                ↓
            Risk decision
        """

        # ---------------------------------------------------------
        # 1. Temporal analysis
        # ---------------------------------------------------------

        temporal_features = self.temporal_engine.analyze(
            node
        )

        # ---------------------------------------------------------
        # 2. Sensor fusion
        # ---------------------------------------------------------

        evidence_score = self.sensor_fusion.calculate_evidence(
            node.water_level_m,
            node.rainfall_mm_h,
            temporal_features[
                "rate_of_rise_m_h"
            ],
            node.soil_moisture_pct,
            temporal_features[
                "persistence"
            ],
        )

        evidence_score = float(evidence_score)

        # ---------------------------------------------------------
        # 3. Convert fusion output to RiskEngine structure
        # ---------------------------------------------------------

        fusion_result = {
            "flood_evidence_score": evidence_score
        }

        # ---------------------------------------------------------
        # 4. Local risk decision
        # ---------------------------------------------------------

        risk_result = self.risk_engine.analyze(
            node,
            temporal_features,
            fusion_result,
        )

        # ---------------------------------------------------------
        # 5. Synchronize node state
        # ---------------------------------------------------------

        node.risk_score = float(
            risk_result["risk_score"]
        )

        node.risk_level = risk_result[
            "risk_level"
        ]

        node.trend = risk_result[
            "trend"
        ]

        node.hazard_state = risk_result[
            "hazard_state"
        ]

        node.event_state = risk_result[
            "event_state"
        ]

        return {
            "temporal": temporal_features,
            "fusion": fusion_result,
            "risk": risk_result,
        }

    # =============================================================
    # EVENT PROCESSING
    # =============================================================

    def process_event(self, node, risk_result):
        """
        Convert the local risk decision into an event.

        EventManager decides whether to:

            - create an event
            - update an event
            - clear an event
        """

        event = self.event_manager.process(
            node=node,
            risk_result=risk_result,
        )

        return event

    # =============================================================
    # RECORD CREATION
    # =============================================================

    def create_record(
        self,
        node,
        temporal_features,
        risk_result,
    ):
        """
        Create a CSV-compatible sensor/intelligence record.

        This combines:

            RAW SENSOR DATA

        with:

            ACTIONABLE LOCAL INTELLIGENCE
        """

        return {
            "timestamp": self.simulation_time.isoformat(),

            "node_id": node.node_id,

            "location": node.location,

            "rainfall_mm_h": round(
                node.rainfall_mm_h,
                2,
            ),

            "temperature_c": round(
                node.temperature_c,
                2,
            ),

            "humidity_pct": round(
                node.humidity_pct,
                2,
            ),

            "soil_moisture_pct": round(
                node.soil_moisture_pct,
                2,
            ),

            "water_level_m": round(
                node.water_level_m,
                3,
            ),

            "wind_speed_m_s": round(
                node.wind_speed_m_s,
                2,
            ),

            "smoke_level": round(
                node.smoke_level,
                2,
            ),

            "gas_level": round(
                node.gas_level,
                2,
            ),

            "soil_stability": round(
                node.soil_stability,
                3,
            ),

            "rate_of_rise_m_h": round(
                temporal_features[
                    "rate_of_rise_m_h"
                ],
                4,
            ),

            "trend": temporal_features[
                "trend"
            ],

            "risk_score": round(
                float(
                    risk_result["risk_score"]
                ),
                4,
            ),

            "risk_level": risk_result[
                "risk_level"
            ],

            "hazard_state": risk_result[
                "hazard_state"
            ],

            "event_state": risk_result[
                "event_state"
            ],

            "network_status": self.network.get_status(),

            "edge_processing": node.edge_processing,
        }

    # =============================================================
    # ACTIONABLE EVENT LOGIC
    # =============================================================

    def is_actionable(self, risk_result):
        """
        Determine whether a local risk decision should be
        treated as an actionable hazard event.

        WATCH, WARNING and CRITICAL are considered actionable.
        """

        return risk_result[
            "risk_level"
        ] in [
            "WATCH",
            "WARNING",
            "CRITICAL",
        ]

    # =============================================================
    # OFFLINE BUFFERING
    # =============================================================

    def buffer_event(self, event):
        """
        Store an event locally while the network is offline.

        EventBuffer is used through its actual API:
            add()
        """

        if event is None:
            return

        self.event_buffer.add(event)

    # =============================================================
    # STORE-AND-FORWARD
    # =============================================================

    def synchronize_buffer(self):
        """
        Synchronize locally buffered events after network
        recovery.

        Events are transmitted through NetworkSimulator and
        then written to the CSV data store.
        """

        buffered_events = self.event_buffer.get_all()

        if not buffered_events:
            print(
                "[SYNC] No buffered events to synchronize."
            )
            return

        print()
        print("=" * 80)
        print(
            f"[SYNC] Synchronizing "
            f"{len(buffered_events)} buffered event(s)..."
        )
        print("=" * 80)

        synchronized = []

        for event in buffered_events:

            transmitted = self.network.transmit(
                event
            )

            if transmitted:

                self.csv_logger.log_data(
                    event
                )

                synchronized.append(
                    event
                )

        if synchronized:

            # Remove successfully synchronized events.
            self.event_buffer.clear()

            print(
                f"[SYNC] Successfully synchronized "
                f"{len(synchronized)} event(s)."
            )

        else:

            print(
                "[SYNC] No events were synchronized."
            )

        print(
            f"[SYNC] Remaining buffer: "
            f"{self.event_buffer.count()}"
        )

        print()

    # =============================================================
    # DISPLAY
    # =============================================================

    def display_node(
        self,
        node,
        temporal_features,
        risk_result,
    ):
        """
        Display one node's current state in the terminal.
        """

        network_status = self.network.get_status()

        print(
            f"\nNODE {node.node_id} | "
            f"{node.location}"
        )

        print(
            f"  Rainfall       : "
            f"{node.rainfall_mm_h:.2f} mm/h"
        )

        print(
            f"  Water Level    : "
            f"{node.water_level_m:.3f} m"
        )

        print(
            f"  Rate of Rise   : "
            f"{temporal_features['rate_of_rise_m_h']:.3f} m/h"
        )

        print(
            f"  Soil Moisture  : "
            f"{node.soil_moisture_pct:.2f}%"
        )

        print(
            f"  Trend          : "
            f"{temporal_features['trend']}"
        )

        print(
            f"  Persistence    : "
            f"{temporal_features['persistence']}"
        )

        print(
            f"  Evidence Score : "
            f"{risk_result['risk_score']:.3f}"
        )

        print(
            f"  Risk Level     : "
            f"{risk_result['risk_level']}"
        )

        print(
            f"  Hazard State   : "
            f"{risk_result['hazard_state']}"
        )

        print(
            f"  Event State    : "
            f"{risk_result['event_state']}"
        )

        print(
            f"  Network        : "
            f"{network_status}"
        )

        print(
            f"  Edge Processing: "
            f"{node.edge_processing}"
        )

        if risk_result["reasons"]:

            print("  Reasons:")

            for reason in risk_result[
                "reasons"
            ]:

                print(
                    f"    - {reason}"
                )

    # =============================================================
    # ONE SIMULATION STEP
    # =============================================================

    def step(self):
        """
        Execute one complete simulation timestep.
        """

        self.step_number += 1

        print()
        print("=" * 80)

        print(
            f"TIME STEP {self.step_number}"
        )

        print(
            f"SIMULATION TIME: "
            f"{self.simulation_time.isoformat()}"
        )

        print(
            f"SCENARIO: "
            f"{self.scenario_phase}"
        )

        print(
            f"NETWORK: "
            f"{self.network.get_status()}"
        )

        print("=" * 80)

        # ---------------------------------------------------------
        # Process every virtual node
        # ---------------------------------------------------------

        for node in self.nodes:

            # -----------------------------------------------------
            # Set simulation timestamp
            # -----------------------------------------------------

            node.timestamp = self.simulation_time

            # -----------------------------------------------------
            # Set system state
            # -----------------------------------------------------

            node.network_status = (
                self.network.get_status()
            )

            node.edge_processing = "ACTIVE"

            # -----------------------------------------------------
            # Generate background environment
            # -----------------------------------------------------

            self.generate_environment(
                node
            )

            # -----------------------------------------------------
            # Generate flood conditions
            # -----------------------------------------------------

            self.generate_flood_state(
                node
            )

            # -----------------------------------------------------
            # Store raw observation in node history
            # -----------------------------------------------------

            node.add_reading()

            # -----------------------------------------------------
            # Local intelligence
            # -----------------------------------------------------

            intelligence = self.process_intelligence(
                node
            )

            temporal_features = intelligence[
                "temporal"
            ]

            risk_result = intelligence[
                "risk"
            ]

            # -----------------------------------------------------
            # Event management
            # -----------------------------------------------------

            event = self.process_event(
                node,
                risk_result,
            )

            # -----------------------------------------------------
            # Create CSV record
            # -----------------------------------------------------

            record = self.create_record(
                node,
                temporal_features,
                risk_result,
            )

            # -----------------------------------------------------
            # ONLINE
            # -----------------------------------------------------

            if self.network.is_online():

                self.csv_logger.log_data(
                    record
                )

                # If an event exists, simulate transmission.
                if event is not None:

                    self.network.transmit(
                        event
                    )

            # -----------------------------------------------------
            # OFFLINE
            # -----------------------------------------------------

            else:

                # Local processing continues.

                if self.is_actionable(
                    risk_result
                ):

                    # Buffer actionable local event.
                    #
                    # Use the event generated by EventManager
                    # when available. Otherwise use the record.

                    event_to_buffer = (
                        event
                        if event is not None
                        else record
                    )

                    self.buffer_event(
                        event_to_buffer
                    )

            # -----------------------------------------------------
            # Display current node
            # -----------------------------------------------------

            self.display_node(
                node,
                temporal_features,
                risk_result,
            )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        print()
        print("-" * 80)

        print(
            f"STEP {self.step_number} COMPLETE"
        )

        print(
            f"Scenario: "
            f"{self.scenario_phase}"
        )

        print(
            f"Network: "
            f"{self.network.get_status()}"
        )

        print(
            f"Buffered Events: "
            f"{self.event_buffer.count()}"
        )

        print("-" * 80)

        # ---------------------------------------------------------
        # Advance simulation clock
        # ---------------------------------------------------------

        self.simulation_time += timedelta(
            hours=self.TIME_STEP_HOURS
        )

    # =============================================================
    # RUN
    # =============================================================

    def run(self, steps=5):
        """
        Run a fixed number of simulation steps.

        Args:
            steps: Number of simulation timesteps.
        """

        print()
        print(
            f"Starting simulation for "
            f"{steps} timestep(s)..."
        )
        print()

        for _ in range(steps):

            self.step()

        print()
        print("=" * 80)

        print("SIMULATION COMPLETE")

        print("=" * 80)

        print(
            f"Total timesteps: "
            f"{self.step_number}"
        )

        print(
            f"Final network status: "
            f"{self.network.get_status()}"
        )

        print(
            f"Buffered events: "
            f"{self.event_buffer.count()}"
        )

        print(
            "Sensor data file: "
            "data/sensor_data.csv"
        )

        print("=" * 80)


# =================================================================
# MAIN
# =================================================================

if __name__ == "__main__":

    simulation = EnvironmentalIntelligenceNetwork()

    print()
    print("=" * 80)
    print("STAGE-1 CONTROLLED FLOOD DEMONSTRATION")
    print("=" * 80)
    print()

    # -------------------------------------------------------------
    # PHASE 1: NORMAL
    # -------------------------------------------------------------

    simulation.set_scenario("NORMAL")
    simulation.run(steps=3)

    # -------------------------------------------------------------
    # PHASE 2: DEVELOPING FLOOD
    # -------------------------------------------------------------

    simulation.set_scenario("DEVELOPING")
    simulation.run(steps=4)

    # -------------------------------------------------------------
    # PHASE 3: SEVERE FLOOD
    # -------------------------------------------------------------

    simulation.set_scenario("SEVERE")
    simulation.run(steps=6)

    # -------------------------------------------------------------
    # PHASE 4: CRITICAL FLOOD
    # -------------------------------------------------------------

    simulation.set_scenario("CRITICAL")
    simulation.run(steps=15)

    print()
    print("=" * 80)
    print("STAGE-1 FLOOD SCENARIO FINISHED")
    print("=" * 80)
