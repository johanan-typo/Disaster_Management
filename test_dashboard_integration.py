"""
Test Dashboard Integration: REST API, WebSocket & Backend Simulation
-------------------------------------------------------------------
Verifies that the new FastAPI + WebSocket backend interacts correctly with
the existing EnvironmentalIntelligenceNetwork simulation.
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from dashboard.backend.api import app, simulation


def test_dashboard_api():
    print("=" * 80)
    print("STARTING DASHBOARD API INTEGRATION TESTS")
    print("=" * 80)

    client = TestClient(app)

    # 1. Test GET /api/status
    res = client.get("/api/status")
    assert res.status_code == 200, f"Status failed: {res.text}"
    status_data = res.json()
    assert "system" in status_data
    assert "simulation" in status_data
    assert "risk_overview" in status_data
    print("[PASS] GET /api/status verified")

    # 2. Test GET /api/nodes
    res = client.get("/api/nodes")
    assert res.status_code == 200
    nodes = res.json()
    assert len(nodes) == 5, f"Expected 5 nodes, got {len(nodes)}"
    assert all("water_level_m" in n for n in nodes)
    assert all("risk_level" in n for n in nodes)
    assert all("edge_ai_response" in n for n in nodes)
    print("[PASS] GET /api/nodes verified (5 nodes with authentic attributes)")

    # 3. Test GET /api/network
    res = client.get("/api/network")
    assert res.status_code == 200
    net_data = res.json()
    assert net_data["status"] == "ONLINE"
    print("[PASS] GET /api/network verified (ONLINE)")

    # 4. Test POST /api/simulation/step
    step_before = simulation.step_number
    res = client.post("/api/simulation/step")
    assert res.status_code == 200
    step_data = res.json()
    assert step_data["step"] == step_before + 1
    print(f"[PASS] POST /api/simulation/step executed (step #{step_data['step']})")

    # 5. Test Network Outage Simulation (POST /api/network/off)
    res = client.post("/api/network/off")
    assert res.status_code == 200
    assert res.json()["network"] == "OFFLINE"
    assert not simulation.network.is_online()
    print("[PASS] POST /api/network/off executed (network switched to OFFLINE)")

    # 6. Test Scenario Switching (POST /api/scenario/CRITICAL)
    res = client.post("/api/scenario/CRITICAL")
    assert res.status_code == 200
    assert res.json()["scenario_phase"] == "CRITICAL"
    print("[PASS] POST /api/scenario/CRITICAL executed")

    # 7. Test Offline Step Execution & Event Buffering
    res = client.post("/api/simulation/step")
    assert res.status_code == 200
    buffered_count = simulation.event_buffer.count()
    print(f"[PASS] Offline step executed: {buffered_count} event(s) buffered in EventBuffer")

    # 8. Test Network Restoration & Store-and-Forward Sync (POST /api/network/on)
    res = client.post("/api/network/on")
    assert res.status_code == 200
    sync_res = res.json()
    assert sync_res["network"] == "ONLINE"
    assert sync_res["buffered_events"] == 0
    assert sync_res["sync_info"]["status"] == "SYNC_COMPLETE"
    print(f"[PASS] POST /api/network/on executed: Store-and-forward synchronized ({sync_res['sync_info']['synced_events']} events, 0 remaining)")

    # 9. Test Static Frontend Mounting (GET /)
    res = client.get("/")
    assert res.status_code == 200
    assert '<div id="root"></div>' in res.text
    print("[PASS] GET / returned production frontend HTML with React mount point")

    # 10. Test WebSocket /ws
    with client.websocket_connect("/ws") as websocket:
        initial_data = websocket.receive_json()
        assert "nodes" in initial_data
        assert "system" in initial_data
        assert len(initial_data["nodes"]) == 5
        websocket.send_text("ping")
        pong = websocket.receive_text()
        assert pong == "pong"
        print("[PASS] WebSocket /ws verified (initial state received, ping-pong passed)")

    print("=" * 80)
    print("ALL 10 INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    test_dashboard_api()
