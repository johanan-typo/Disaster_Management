from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "simulation" / "simulation_runner.py"
BACKUP = ROOT / "simulation" / "simulation_runner.before-stage1-integration"

TEST = ROOT / "test_runner_integration.py"


def backup_file(source, backup):
    if not backup.exists():
        shutil.copy2(source, backup)
        print(f"[BACKUP] {backup}")


def replace_once(text, old, new, description):
    if old not in text:
        raise RuntimeError(
            f"Could not find expected section: {description}"
        )

    count = text.count(old)

    if count != 1:
        raise RuntimeError(
            f"Expected exactly one occurrence of {description}, "
            f"found {count}"
        )

    return text.replace(old, new, 1)


def update_runner():
    print("\nUpdating simulation_runner.py...")

    text = RUNNER.read_text(encoding="utf-8")

    backup_file(RUNNER, BACKUP)

    # ---------------------------------------------------------
    # 1. Make direct execution robust
    # ---------------------------------------------------------

    old = '''from datetime import datetime, timedelta

from engines.node_model import VirtualNode
'''

    new = '''import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime, timedelta

from engines.node_model import VirtualNode
'''

    text = replace_once(
        text,
        old,
        new,
        "project-root import setup",
    )

    # ---------------------------------------------------------
    # 2. Initialize Edge AI and offline CSV buffer
    # ---------------------------------------------------------

    old = '''        self.risk_engine = RiskEngine()

        # ---------------------------------------------------------
        # COMMUNICATION / RESILIENCE
'''

    new = '''        self.risk_engine = RiskEngine()

        # ---------------------------------------------------------
        # LOCAL EDGE AI
        # ---------------------------------------------------------

        # RiskEngine remains the authoritative deterministic
        # intelligence layer.
        #
        # Needle only selects a structured local response
        # for an already-computed risk state.

        self.edge_ai = EdgeAI()

        # Latest Needle result for each node.
        self.last_edge_ai_results = {}

        # ---------------------------------------------------------
        # OFFLINE DATA BUFFER
        # ---------------------------------------------------------

        # Full CSV-compatible sensor/intelligence records are
        # retained while the network is offline.
        #
        # This is separate from EventBuffer:
        #
        #   pending_csv_records -> sensor/intelligence data
        #   event_buffer        -> actionable hazard events

        self.pending_csv_records = []

        # ---------------------------------------------------------
        # COMMUNICATION / RESILIENCE
'''

    text = replace_once(
        text,
        old,
        new,
        "Edge AI and offline buffer initialization",
    )

    # ---------------------------------------------------------
    # 3. Add Edge AI method before EVENT PROCESSING
    # ---------------------------------------------------------

    marker = '''    # =============================================================
    # EVENT PROCESSING
    # =============================================================
'''

    edge_method = '''    # =============================================================
    # LOCAL EDGE AI
    # =============================================================

    def process_edge_ai(self, node, risk_result):
        """
        Run Needle Edge AI for an actionable local risk state.

        RiskEngine remains authoritative.

        Needle does not:
            - calculate flood physics
            - calculate risk score
            - replace sensor fusion
            - replace RiskEngine

        Needle only selects the structured local response.
        """

        if not self.is_actionable(risk_result):
            return None

        try:
            result = self.edge_ai.analyze_node(node)

        except Exception as exc:
            result = {
                "ai_active": False,
                "confidence": 0.0,
                "tool_called": False,
                "action_executed": False,
                "response": None,
                "reasoning": None,
                "error": str(exc),
                "status": "AI_ERROR",
            }

        self.last_edge_ai_results[node.node_id] = result

        return result

    # =============================================================
    # EVENT PROCESSING
    # =============================================================
'''

    text = replace_once(
        text,
        marker,
        edge_method,
        "event processing section",
    )

    # ---------------------------------------------------------
    # 4. Add Edge AI execution after RiskEngine
    # ---------------------------------------------------------

    old = '''            risk_result = intelligence[
                "risk"
            ]

            # -----------------------------------------------------
            # Event management
'''

    new = '''            risk_result = intelligence[
                "risk"
            ]

            # -----------------------------------------------------
            # Local Needle Edge AI
            # -----------------------------------------------------

            edge_ai_result = self.process_edge_ai(
                node,
                risk_result,
            )

            # -----------------------------------------------------
            # Event management
'''

    text = replace_once(
        text,
        old,
        new,
        "Edge AI execution point",
    )

    # ---------------------------------------------------------
    # 5. Store CSV records while offline
    # ---------------------------------------------------------

    old = '''            else:

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
'''

    new = '''            else:

                # -------------------------------------------------
                # OFFLINE MODE
                # -------------------------------------------------
                #
                # CSV output intentionally stops while offline.
                #
                # Local processing DOES NOT stop.
                #
                # The complete CSV-compatible record is retained
                # locally for store-and-forward synchronization.

                self.pending_csv_records.append(
                    record
                )

                # -------------------------------------------------
                # Buffer actionable hazard event
                # -------------------------------------------------

                if self.is_actionable(
                    risk_result
                ):

                    event_to_buffer = (
                        event
                        if event is not None
                        else record
                    )

                    self.buffer_event(
                        event_to_buffer
                    )
'''

    text = replace_once(
        text,
        old,
        new,
        "offline record buffering",
    )

    # ---------------------------------------------------------
    # 6. Replace synchronization logic
    # ---------------------------------------------------------

    start_marker = '''    def synchronize_buffer(self):
'''

    start = text.find(start_marker)

    if start == -1:
        raise RuntimeError(
            "Could not find synchronize_buffer()"
        )

    next_section = text.find(
        '''    # =============================================================
    # DISPLAY
    # =============================================================
''',
        start,
    )

    if next_section == -1:
        raise RuntimeError(
            "Could not find DISPLAY section after synchronize_buffer()"
        )

    sync_method = '''    def synchronize_buffer(self):
        """
        Synchronize all locally retained data after network recovery.

        Two independent stores are synchronized:

            1. pending_csv_records
               Complete sensor/intelligence records.

            2. event_buffer
               Actionable hazard events.

        Both are cleared only after successful transmission/write.
        """

        csv_records = list(
            self.pending_csv_records
        )

        buffered_events = self.event_buffer.get_all()

        if not csv_records and not buffered_events:
            print(
                "[SYNC] No buffered data to synchronize."
            )
            return

        print()
        print("=" * 80)
        print(
            f"[SYNC] Synchronizing "
            f"{len(csv_records)} CSV record(s) "
            f"and "
            f"{len(buffered_events)} event(s)..."
        )
        print("=" * 80)

        # ---------------------------------------------------------
        # 1. Synchronize CSV records
        # ---------------------------------------------------------

        csv_synchronized = 0

        for record in csv_records:

            try:
                self.csv_logger.log_data(
                    record
                )

                csv_synchronized += 1

            except Exception as exc:

                print(
                    f"[SYNC] CSV synchronization failed: "
                    f"{exc}"
                )

                break

        if csv_synchronized == len(csv_records):

            self.pending_csv_records.clear()

        # ---------------------------------------------------------
        # 2. Synchronize actionable events
        # ---------------------------------------------------------

        event_synchronized = 0

        for event in buffered_events:

            try:

                transmitted = self.network.transmit(
                    event
                )

                if transmitted:
                    event_synchronized += 1

            except Exception as exc:

                print(
                    f"[SYNC] Event synchronization failed: "
                    f"{exc}"
                )

                break

        if event_synchronized == len(buffered_events):

            self.event_buffer.clear()

        print(
            f"[SYNC] CSV records synchronized: "
            f"{csv_synchronized}/{len(csv_records)}"
        )

        print(
            f"[SYNC] Events synchronized: "
            f"{event_synchronized}/{len(buffered_events)}"
        )

        print(
            f"[SYNC] Remaining CSV records: "
            f"{len(self.pending_csv_records)}"
        )

        print(
            f"[SYNC] Remaining events: "
            f"{self.event_buffer.count()}"
        )

        print()

'''

    text = (
        text[:start]
        + sync_method
        + text[next_section:]
    )

    # ---------------------------------------------------------
    # 7. Add Edge AI display
    # ---------------------------------------------------------

    old = '''        if risk_result["reasons"]:

            print("  Reasons:")
'''

    new = '''        edge_result = self.last_edge_ai_results.get(
            node.node_id
        )

        if edge_result is not None:

            print(
                f"  Needle Edge AI : "
                f"{edge_result['status']}"
            )

            if edge_result["response"] is not None:

                print(
                    f"  Local Response : "
                    f"{edge_result['response']}"
                )

        if risk_result["reasons"]:

            print("  Reasons:")
'''

    text = replace_once(
        text,
        old,
        new,
        "Edge AI terminal display",
    )

    # ---------------------------------------------------------
    # 8. Add synchronization information to step summary
    # ---------------------------------------------------------

    old = '''        print(
            f"Buffered Events: "
            f"{self.event_buffer.count()}"
        )

        print("-" * 80)
'''

    new = '''        print(
            f"Buffered Events: "
            f"{self.event_buffer.count()}"
        )

        print(
            f"Pending CSV Records: "
            f"{len(self.pending_csv_records)}"
        )

        print("-" * 80)
'''

    text = replace_once(
        text,
        old,
        new,
        "step summary",
    )

    # ---------------------------------------------------------
    # 9. Add cleanup
    # ---------------------------------------------------------

    marker = '''# =================================================================
# MAIN
# =================================================================
'''

    cleanup = '''    # =============================================================
    # CLEANUP
    # =============================================================

    def close(self):
        """
        Release the local Needle runtime.
        """

        if self.edge_ai is not None:

            self.edge_ai.close()

            self.edge_ai = None


# =================================================================
# MAIN
# =================================================================
'''

    text = replace_once(
        text,
        marker,
        cleanup,
        "cleanup section",
    )

    # ---------------------------------------------------------
    # 10. Close Needle runtime in main
    # ---------------------------------------------------------

    old = '''    simulation.set_scenario("CRITICAL")
    simulation.run(steps=15)

    print()
'''

    new = '''    simulation.set_scenario("CRITICAL")
    simulation.run(steps=15)

    simulation.close()

    print()
'''

    text = replace_once(
        text,
        old,
        new,
        "main cleanup",
    )

    RUNNER.write_text(
        text,
        encoding="utf-8",
    )

    print("[PASS] simulation_runner.py updated")


def write_integration_test():
    print("\nUpdating integration test...")

    backup = TEST.with_suffix(".py.before-stage1")
    if TEST.exists():
        backup_file(TEST, backup)

    test_code = r'''from pathlib import Path

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
'''

    TEST.write_text(
        test_code,
        encoding="utf-8",
    )

    print("[PASS] test_runner_integration.py updated")


def main():

    print("=" * 80)
    print("ENVIRONMENTAL INTELLIGENCE NETWORK")
    print("STAGE-1 EDGE AI INTEGRATION")
    print("=" * 80)

    if not RUNNER.exists():
        raise FileNotFoundError(
            f"Runner not found: {RUNNER}"
        )

    update_runner()
    write_integration_test()

    print("\n" + "=" * 80)
    print("UPDATE COMPLETE")
    print("=" * 80)
    print()
    print("Next:")
    print("  python -m py_compile simulation/simulation_runner.py")
    print("  python -m py_compile test_runner_integration.py")
    print("  python test_runner_integration.py")
    print()


if __name__ == "__main__":
    main()
