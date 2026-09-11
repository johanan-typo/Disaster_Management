from pathlib import Path

from simulation.simulation_runner import (
    EnvironmentalIntelligenceNetwork,
)


def main():

    print("=" * 80)
    print("STAGE-1 RUNNER INTEGRATION TEST")
    print("=" * 80)

    simulation = EnvironmentalIntelligenceNetwork()

    # ---------------------------------------------------------
    # 1. Virtual nodes
    # ---------------------------------------------------------

    assert len(simulation.nodes) == 5

    print("\n[PASS] Five virtual nodes initialized")

    # ---------------------------------------------------------
    # 2. ONLINE operation
    # ---------------------------------------------------------

    simulation.set_scenario("NORMAL")

    simulation.step()

    assert simulation.network.is_online()

    print("[PASS] ONLINE simulation completed")

    # ---------------------------------------------------------
    # 3. OFFLINE operation
    # ---------------------------------------------------------

    simulation.network_off()

    assert not simulation.network.is_online()

    print("[PASS] Network switched OFF")

    # ---------------------------------------------------------
    # 4. CRITICAL scenario while offline
    # ---------------------------------------------------------

    simulation.set_scenario("CRITICAL")

    simulation.step()

    print(
        "[PASS] CRITICAL scenario executed while OFFLINE"
    )

    # ---------------------------------------------------------
    # 5. Local processing
    # ---------------------------------------------------------

    assert all(
        node.edge_processing == "ACTIVE"
        for node in simulation.nodes
    )

    print(
        "[PASS] Local edge processing continued offline"
    )

    # ---------------------------------------------------------
    # 6. Edge AI
    # ---------------------------------------------------------

    edge_results = simulation.last_edge_ai_results

    assert len(edge_results) > 0

    successful_actions = [
        result
        for result in edge_results.values()
        if result["action_executed"]
    ]

    assert len(successful_actions) > 0

    print(
        f"[PASS] Needle Edge AI executed locally "
        f"for {len(successful_actions)} node(s)"
    )

    # ---------------------------------------------------------
    # 7. Offline CSV buffering
    # ---------------------------------------------------------

    pending_csv = len(
        simulation.pending_csv_records
    )

    assert pending_csv == 5

    print(
        f"[PASS] {pending_csv} CSV record(s) "
        f"buffered locally"
    )

    # ---------------------------------------------------------
    # 8. Event buffering
    # ---------------------------------------------------------

    buffered_events = simulation.event_buffer.count()

    assert buffered_events > 0

    print(
        f"[PASS] {buffered_events} actionable event(s) "
        f"buffered"
    )

    # ---------------------------------------------------------
    # 9. Network recovery
    # ---------------------------------------------------------

    simulation.network_on()

    assert simulation.network.is_online()

    print("[PASS] Network restored")

    # ---------------------------------------------------------
    # 10. Verify CSV synchronization
    # ---------------------------------------------------------

    assert len(
        simulation.pending_csv_records
    ) == 0

    print(
        "[PASS] Offline CSV records synchronized"
    )

    # ---------------------------------------------------------
    # 11. Verify event synchronization
    # ---------------------------------------------------------

    assert simulation.event_buffer.count() == 0

    print(
        "[PASS] Buffered events synchronized"
    )

    # ---------------------------------------------------------
    # 12. CSV existence
    # ---------------------------------------------------------

    csv_path = Path(
        "data/sensor_data.csv"
    )

    assert csv_path.exists()

    print(
        f"[PASS] CSV exists: {csv_path}"
    )

    # ---------------------------------------------------------
    # 13. Cleanup
    # ---------------------------------------------------------

    simulation.close()

    print("\n" + "=" * 80)
    print("INTEGRATION TEST PASSED")
    print("=" * 80)


if __name__ == "__main__":
    main()
