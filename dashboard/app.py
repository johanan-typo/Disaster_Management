# ============================================================
# ENVIRONMENTAL INTELLIGENCE NETWORK
# ============================================================
#
# Stage-1 Flood Simulation Dashboard
#
# Modes:
#   1. MANUAL
#   2. AUTOMATIC
#
# Backend:
#   EnvironmentalIntelligenceNetwork
#
# Visualization:
#   Plotly 3D
#
# ============================================================


# ============================================================
# IMPORT PATH
# ============================================================

import sys

from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


# ============================================================
# IMPORTS
# ============================================================

import time

import pandas as pd

import streamlit as st


from simulation.simulation_runner import (
    EnvironmentalIntelligenceNetwork
)


from flood_3d import (
    create_flood_3d
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(

    page_title=(
        "Environmental Intelligence Network"
    ),

    page_icon="🌊",

    layout="wide",

)


# ============================================================
# SESSION STATE
# ============================================================

if "simulation" not in st.session_state:

    st.session_state.simulation = (
        EnvironmentalIntelligenceNetwork()
    )


if "mode" not in st.session_state:

    st.session_state.mode = "MANUAL"


if "running" not in st.session_state:

    st.session_state.running = False


if "auto_phase_index" not in st.session_state:

    st.session_state.auto_phase_index = 0


if "auto_phase_steps" not in st.session_state:

    st.session_state.auto_phase_steps = 0


# ------------------------------------------------------------
# Local reference
# ------------------------------------------------------------

simulation = (
    st.session_state.simulation
)


# ============================================================
# AUTOMATIC DEMONSTRATION
# ============================================================
#
# This sequence is a controlled demonstration.
#
# NORMAL
#    ↓
# DEVELOPING
#    ↓
# SEVERE
#    ↓
# CRITICAL
#    ↓
# RECOVERY
#
# ============================================================

AUTO_PHASES = [

    ("NORMAL", 5),

    ("DEVELOPING", 8),

    ("SEVERE", 8),

    ("CRITICAL", 12),

    ("RECOVERY", 10),

]


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def reset_simulation():

    st.session_state.simulation = (
        EnvironmentalIntelligenceNetwork()
    )

    st.session_state.mode = "MANUAL"

    st.session_state.running = False

    st.session_state.auto_phase_index = 0

    st.session_state.auto_phase_steps = 0

    st.rerun()


# ------------------------------------------------------------
# Buffer count
# ------------------------------------------------------------
#
# IMPORTANT:
# The real backend uses:
#
#     simulation.event_buffer
#
# NOT:
#
#     simulation.buffer
#
# ------------------------------------------------------------

def get_buffer_count():

    return simulation.event_buffer.count()


# ------------------------------------------------------------
# Risk symbol
# ------------------------------------------------------------

def risk_symbol(level):

    return {

        "NORMAL": "🟢",

        "WATCH": "🟡",

        "WARNING": "🟠",

        "CRITICAL": "🔴",

    }.get(
        level,
        "⚪"
    )


# ------------------------------------------------------------
# Risk display
# ------------------------------------------------------------

def risk_display(level):

    return (
        f"{risk_symbol(level)} {level}"
    )


# ============================================================
# MANUAL STEP
# ============================================================

def manual_step():

    simulation.step()


# ============================================================
# AUTOMATIC STEP
# ============================================================

def automatic_step():

    phase_index = (
        st.session_state.auto_phase_index
    )


    phase_name, phase_duration = (
        AUTO_PHASES[phase_index]
    )


    # --------------------------------------------------------
    # Set scenario
    # --------------------------------------------------------

    if (
        simulation.scenario_phase
        != phase_name
    ):

        simulation.set_scenario(
            phase_name
        )


    # --------------------------------------------------------
    # Execute real backend timestep
    # --------------------------------------------------------

    simulation.step()


    st.session_state.auto_phase_steps += 1


    # --------------------------------------------------------
    # Move to next phase
    # --------------------------------------------------------

    if (
        st.session_state.auto_phase_steps
        >= phase_duration
    ):

        st.session_state.auto_phase_steps = 0


        if (
            phase_index
            < len(AUTO_PHASES) - 1
        ):

            st.session_state.auto_phase_index += 1

        else:

            st.session_state.running = False


# ============================================================
# HEADER
# ============================================================

st.title(
    "🌍 Environmental Intelligence Network"
)


st.caption(
    "Offline-First Multi-Hazard Intelligence "
    "and Flood Simulation — Stage 1"
)


# ============================================================
# SYSTEM STATUS
# ============================================================

network_status = (
    simulation.network.get_status()
)


buffer_count = (
    get_buffer_count()
)


status_1, status_2, status_3, status_4 = (
    st.columns(4)
)


with status_1:

    st.metric(
        "Network",
        network_status
    )


with status_2:

    st.metric(
        "Edge Processing",
        "ACTIVE"
    )


with status_3:

    st.metric(
        "Scenario",
        simulation.scenario_phase
    )


with status_4:

    st.metric(
        "Buffered Events",
        buffer_count
    )


# ============================================================
# NETWORK BANNER
# ============================================================

if network_status == "OFFLINE":

    st.warning(
        "🔌 NETWORK OFFLINE  |  "
        "EDGE PROCESSING ACTIVE  |  "
        "LOCAL ALERTS ACTIVE"
    )

else:

    st.success(
        "🟢 NETWORK ONLINE  |  "
        "EDGE PROCESSING ACTIVE"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "🎛️ Simulation Control"
    )


    # ========================================================
    # MODE
    # ========================================================

    st.subheader(
        "Simulation Mode"
    )


    selected_mode = st.radio(

        "Choose mode",

        [
            "MANUAL",
            "AUTOMATIC",
        ],

        index=(
            0
            if st.session_state.mode
            == "MANUAL"
            else 1
        ),

    )


    if (
        selected_mode
        != st.session_state.mode
    ):

        st.session_state.mode = (
            selected_mode
        )

        st.session_state.running = False


    # ========================================================
    # MANUAL MODE
    # ========================================================

    if (
        st.session_state.mode
        == "MANUAL"
    ):

        st.subheader(
            "Manual Controls"
        )


        if st.button(
            "▶ NEXT TIME STEP",
            use_container_width=True,
        ):

            manual_step()

            st.rerun()


        if st.button(
            "🔄 RESET",
            use_container_width=True,
        ):

            reset_simulation()


        st.subheader(
            "Scenario"
        )


        scenarios = [

            "NORMAL",

            "DEVELOPING",

            "SEVERE",

            "CRITICAL",

            "RECOVERY",

        ]


        selected_scenario = (
            st.selectbox(

                "Scenario",

                scenarios,

                index=scenarios.index(
                    simulation.scenario_phase
                ),

            )
        )


        if (
            selected_scenario
            != simulation.scenario_phase
        ):

            simulation.set_scenario(
                selected_scenario
            )

            st.rerun()


    # ========================================================
    # AUTOMATIC MODE
    # ========================================================

    else:

        st.subheader(
            "Automatic Demonstration"
        )


        if (
            not st.session_state.running
        ):

            if st.button(
                "▶ START AUTO",
                use_container_width=True,
            ):

                st.session_state.running = True

                st.rerun()

        else:

            if st.button(
                "⏸ PAUSE",
                use_container_width=True,
            ):

                st.session_state.running = False

                st.rerun()


        if st.button(
            "🔄 RESET AUTO",
            use_container_width=True,
        ):

            reset_simulation()


        phase_index = (
            st.session_state.auto_phase_index
        )


        phase_name, phase_duration = (
            AUTO_PHASES[phase_index]
        )


        st.info(

            f"Phase: **{phase_name}**\n\n"

            f"Progress: "
            f"{st.session_state.auto_phase_steps}"
            f"/{phase_duration}"

        )


    # ========================================================
    # NETWORK CONTROL
    # ========================================================

    st.subheader(
        "Communication"
    )


    if network_status == "ONLINE":

        if st.button(
            "🔌 NETWORK OFF",
            use_container_width=True,
        ):

            simulation.network_off()

            st.rerun()


    else:

        if st.button(
            "📡 RESTORE NETWORK",
            use_container_width=True,
        ):

            simulation.network_on()

            st.rerun()


    # ========================================================
    # SIMULATION INFO
    # ========================================================

    st.subheader(
        "Simulation Information"
    )


    st.write(
        f"**Time Step:** "
        f"{simulation.step_number}"
    )


    st.write(
        f"**Simulation Time:** "
        f"{simulation.simulation_time}"
    )


    st.write(
        f"**Virtual Nodes:** "
        f"{len(simulation.nodes)}"
    )


    st.write(
        "**Timestep Duration:** 1 hour"
    )


# ============================================================
# AUTOMATIC EXECUTION
# ============================================================

if (

    st.session_state.mode
    == "AUTOMATIC"

    and

    st.session_state.running

):

    automatic_step()


    time.sleep(
        0.7
    )


    st.rerun()


# ============================================================
# 3D FLOOD ENVIRONMENT
# ============================================================

st.header(
    "🌊 3D Flood Environment"
)


st.caption(
    "The 3D environment is driven by the actual "
    "VirtualNode water-level state from the simulation."
)


# ------------------------------------------------------------
# Create figure
# ------------------------------------------------------------

flood_figure = create_flood_3d(
    simulation.nodes
)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

st.plotly_chart(

    flood_figure,

    use_container_width=True,

)


# ============================================================
# CURRENT FLOOD SUMMARY
# ============================================================

st.header(
    "🌊 Current Flood State"
)


max_water = max(

    float(node.water_level_m)

    for node in simulation.nodes

)


avg_water = (

    sum(
        float(node.water_level_m)
        for node in simulation.nodes
    )

    /

    len(simulation.nodes)

)


rising_nodes = sum(

    1

    for node in simulation.nodes

    if node.trend == "RISING"

)


critical_nodes = sum(

    1

    for node in simulation.nodes

    if node.risk_level == "CRITICAL"

)


f1, f2, f3, f4 = (
    st.columns(4)
)


with f1:

    st.metric(
        "Maximum Water",
        f"{max_water:.2f} m"
    )


with f2:

    st.metric(
        "Average Water",
        f"{avg_water:.2f} m"
    )


with f3:

    st.metric(
        "Rising Nodes",
        rising_nodes
    )


with f4:

    st.metric(
        "Critical Nodes",
        critical_nodes
    )


# ============================================================
# VIRTUAL SENSOR NODES
# ============================================================

st.header(
    "📡 Virtual Sensor Nodes"
)


node_columns = st.columns(
    len(simulation.nodes)
)


for column, node in zip(

    node_columns,

    simulation.nodes

):

    with column:

        st.subheader(
            f"Node {node.node_id}"
        )


        st.caption(
            node.location
        )


        st.metric(
            "Water Level",
            f"{node.water_level_m:.2f} m"
        )


        st.write(
            f"Risk: "
            f"{risk_display(node.risk_level)}"
        )


        st.write(
            f"🌧️ Rainfall: "
            f"{node.rainfall_mm_h:.1f} mm/h"
        )


        st.write(
            f"📈 Rate: "
            f"{node.rate_of_rise_m_h:.3f} m/h"
        )


        st.write(
            f"📊 Trend: "
            f"{node.trend}"
        )


        st.write(
            f"⚠️ Hazard: "
            f"{node.hazard_state}"
        )


        st.write(
            f"🚨 Event: "
            f"{node.event_state}"
        )


        st.write(
            f"📡 Network: "
            f"{node.network_status}"
        )


        st.write(
            f"🧠 Edge: "
            f"{node.edge_processing}"
        )


# ============================================================
# DOWNSTREAM MONITORING
# ============================================================

st.header(
    "➡️ Possible Downstream Hazard Progression"
)


st.info(

    "A → B → C represents a possible simulated "
    "downstream hazard progression across monitored "
    "locations. It is not a scientifically validated "
    "prediction of real flood propagation."

)


progression = st.columns(
    3
)


for column, node_id in zip(

    progression,

    ["A", "B", "C"]

):

    node = next(

        node

        for node in simulation.nodes

        if node.node_id == node_id

    )


    with column:

        st.metric(

            f"Node {node_id}",

            f"{node.water_level_m:.2f} m",

            delta=(
                f"{node.rate_of_rise_m_h:.3f} m/h"
            ),

        )


        st.write(
            risk_display(
                node.risk_level
            )
        )


# ============================================================
# OFFLINE RESILIENCE
# ============================================================

st.header(
    "🔌 Offline Resilience"
)


offline_1, offline_2, offline_3 = (
    st.columns(3)
)


with offline_1:

    st.metric(
        "Network",
        simulation.network.get_status()
    )


with offline_2:

    st.metric(
        "Buffered Events",
        get_buffer_count()
    )


with offline_3:

    st.metric(
        "Edge Processing",
        "ACTIVE"
    )


if (
    simulation.network.get_status()
    == "OFFLINE"
):

    st.warning(

        "Network unavailable. Local sensing, "
        "temporal analysis, sensor fusion and "
        "risk inference continue at the edge. "
        "Actionable events are buffered for "
        "store-and-forward synchronization."

    )

else:

    st.success(

        "Network available. "
        "Local intelligence remains active."

    )


# ============================================================
# SENSOR DATA
# ============================================================

st.header(
    "📊 Sensor Data"
)


csv_path = (

    PROJECT_ROOT

    / "data"

    / "sensor_data.csv"

)


if csv_path.exists():

    try:

        dataframe = pd.read_csv(
            csv_path
        )


        st.caption(

            f"Stored records: "
            f"{len(dataframe)}"

        )


        display_columns = [

            "timestamp",

            "node_id",

            "location",

            "rainfall_mm_h",

            "water_level_m",

            "rate_of_rise_m_h",

            "trend",

            "risk_score",

            "risk_level",

            "hazard_state",

            "event_state",

            "network_status",

        ]


        available_columns = [

            column

            for column in display_columns

            if column in dataframe.columns

        ]


        st.dataframe(

            dataframe[
                available_columns
            ].tail(25),

            use_container_width=True,

        )


    except Exception as error:

        st.error(
            f"Unable to read CSV: {error}"
        )

else:

    st.info(
        "No sensor CSV has been generated yet."
    )


# ============================================================
# SCIENTIFIC DISCLAIMER
# ============================================================

st.divider()


st.caption(

    "Stage-1 Proof of Concept. Environmental "
    "conditions are generated using virtual sensors. "
    "Local risk inference is transparent and rule-based. "
    "The system does not claim real-world flood prediction "
    "accuracy or scientifically validated flood propagation."

)
