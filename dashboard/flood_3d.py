# ============================================================
# 3D FLOOD VISUALIZATION
# Environmental Intelligence Network
# ============================================================

import numpy as np
import plotly.graph_objects as go


# ------------------------------------------------------------
# FIXED VIRTUAL NODE LOCATIONS
# ------------------------------------------------------------

NODE_POSITIONS = {
    "A": (0.0, 0.0),
    "B": (3.0, 1.0),
    "C": (6.0, 0.0),
    "D": (3.0, -3.0),
    "E": (8.0, -3.0),
}


# ------------------------------------------------------------
# RISK LEVEL → NUMERIC VALUE
# ------------------------------------------------------------

RISK_VALUES = {
    "NORMAL": 0,
    "WATCH": 1,
    "WARNING": 2,
    "CRITICAL": 3,
}


# ------------------------------------------------------------
# CREATE 3D FLOOD FIGURE
# ------------------------------------------------------------

def create_flood_3d(nodes):

    """
    Create the 3D flood environment.

    IMPORTANT:
    The simulation backend stores nodes as a LIST.
    Therefore this function converts the list into a
    node-id dictionary locally.

    Water levels are taken directly from:
        node.water_level_m
    """

    # --------------------------------------------------------
    # Convert backend node list → dictionary
    # --------------------------------------------------------

    node_map = {
        node.node_id: node
        for node in nodes
    }


    # --------------------------------------------------------
    # Ground
    # --------------------------------------------------------

    x_ground = np.linspace(-2, 10, 35)
    y_ground = np.linspace(-5, 4, 35)

    X_ground, Y_ground = np.meshgrid(
        x_ground,
        y_ground
    )

    Z_ground = np.zeros_like(X_ground)


    fig = go.Figure()


    fig.add_trace(
        go.Surface(
            x=X_ground,
            y=Y_ground,
            z=Z_ground,
            showscale=False,
            opacity=0.35,
            name="Terrain",
            hoverinfo="skip",
        )
    )


    # --------------------------------------------------------
    # ACTUAL WATER LEVEL
    # --------------------------------------------------------

    water_levels = [
        max(
            0.0,
            float(node.water_level_m)
        )
        for node in nodes
    ]


    if water_levels:

        max_water_level = max(
            water_levels
        )

    else:

        max_water_level = 0.0


    # --------------------------------------------------------
    # DISPLAY LIMIT
    # --------------------------------------------------------
    #
    # We use a maximum visual scale of 5 m so the scene
    # remains readable even if the simulation is run for
    # many timesteps.
    #
    # This DOES NOT modify the simulation.
    #
    # --------------------------------------------------------

    display_water_level = min(
        max_water_level,
        5.0
    )


    # --------------------------------------------------------
    # WATER SURFACE
    # --------------------------------------------------------

    x_water = np.linspace(-2, 10, 35)
    y_water = np.linspace(-5, 4, 35)

    X_water, Y_water = np.meshgrid(
        x_water,
        y_water
    )

    Z_water = np.full_like(
        X_water,
        display_water_level
    )


    fig.add_trace(
        go.Surface(
            x=X_water,
            y=Y_water,
            z=Z_water,
            showscale=False,
            opacity=0.68,
            name="Flood Water",
            hovertemplate=(
                "Water Level: "
                f"{display_water_level:.2f} m"
                "<extra></extra>"
            ),
        )
    )


    # --------------------------------------------------------
    # SENSOR NODES
    # --------------------------------------------------------

    node_x = []
    node_y = []
    node_z = []

    node_labels = []
    node_hover = []
    node_risk = []


    for node in nodes:

        node_id = node.node_id

        x, y = NODE_POSITIONS.get(
            node_id,
            (0.0, 0.0)
        )

        water_level = max(
            0.0,
            float(node.water_level_m)
        )

        node_x.append(x)
        node_y.append(y)

        # Node is positioned according to actual water level.
        node_z.append(
            min(
                water_level,
                5.0
            ) + 0.18
        )

        node_labels.append(
            node_id
        )

        node_risk.append(
            RISK_VALUES.get(
                node.risk_level,
                0
            )
        )

        node_hover.append(
            "<b>Virtual Sensor Node "
            f"{node_id}</b><br>"
            f"Location: {node.location}<br>"
            f"Water Level: {water_level:.2f} m<br>"
            f"Rainfall: {node.rainfall_mm_h:.1f} mm/h<br>"
            f"Rate of Rise: "
            f"{node.rate_of_rise_m_h:.3f} m/h<br>"
            f"Risk: {node.risk_level}<br>"
            f"Trend: {node.trend}<br>"
            f"Hazard: {node.hazard_state}<br>"
            f"Event: {node.event_state}<br>"
            f"Network: {node.network_status}<br>"
            f"Edge: {node.edge_processing}"
        )


    # --------------------------------------------------------
    # NODE TRACE
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode="markers+text",

            text=node_labels,

            textposition="top center",

            marker=dict(
                size=11,

                color=node_risk,

                colorscale=[
                    [0.00, "green"],
                    [0.33, "yellow"],
                    [0.66, "orange"],
                    [1.00, "red"],
                ],

                cmin=0,
                cmax=3,

                showscale=False,
            ),

            hovertext=node_hover,

            hoverinfo="text",

            name="Virtual Sensor Nodes",
        )
    )


    # --------------------------------------------------------
    # POSSIBLE DOWNSTREAM PATH
    # --------------------------------------------------------
    #
    # This is a visualization of the monitored topology.
    # It is NOT a scientifically validated propagation model.
    # --------------------------------------------------------

    paths = [
        ("A", "B"),
        ("B", "C"),
    ]


    for source_id, target_id in paths:

        if (
            source_id not in node_map
            or target_id not in node_map
        ):
            continue


        source = node_map[source_id]
        target = node_map[target_id]


        x1, y1 = NODE_POSITIONS[source_id]
        x2, y2 = NODE_POSITIONS[target_id]


        z1 = min(
            float(source.water_level_m),
            5.0
        ) + 0.10


        z2 = min(
            float(target.water_level_m),
            5.0
        ) + 0.10


        fig.add_trace(
            go.Scatter3d(
                x=[x1, x2],
                y=[y1, y2],
                z=[z1, z2],

                mode="lines",

                line=dict(
                    width=6
                ),

                hoverinfo="skip",

                showlegend=False,
            )
        )


    # --------------------------------------------------------
    # WATER LEVEL THRESHOLD PLANES
    # --------------------------------------------------------

    threshold_levels = [
        (1.0, "WATCH / RISING"),
        (2.0, "FLOOD THRESHOLD"),
        (3.0, "HIGH WATER"),
    ]


    for threshold, label in threshold_levels:

        if threshold <= 5.0:

            X_threshold, Y_threshold = np.meshgrid(
                np.linspace(-2, 10, 2),
                np.linspace(-5, 4, 2)
            )

            Z_threshold = np.full_like(
                X_threshold,
                threshold
            )


            fig.add_trace(
                go.Surface(
                    x=X_threshold,
                    y=Y_threshold,
                    z=Z_threshold,
                    opacity=0.05,
                    showscale=False,
                    name=label,
                    hovertemplate=(
                        f"{label}: "
                        f"{threshold:.1f} m"
                        "<extra></extra>"
                    ),
                )
            )


    # --------------------------------------------------------
    # LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        title=(
            "3D Flood Environment — "
            f"Current Water Level: "
            f"{max_water_level:.2f} m"
        ),

        scene=dict(

            xaxis=dict(
                title="X Position",
                showbackground=True,
            ),

            yaxis=dict(
                title="Y Position",
                showbackground=True,
            ),

            zaxis=dict(
                title="Water Level (m)",
                range=[0, 5],
            ),

            aspectmode="manual",

            aspectratio=dict(
                x=1.5,
                y=1.0,
                z=0.8,
            ),

            camera=dict(
                eye=dict(
                    x=1.6,
                    y=1.6,
                    z=1.2,
                )
            ),
        ),

        height=650,

        margin=dict(
            l=0,
            r=0,
            t=55,
            b=0,
        ),
    )


    return fig
