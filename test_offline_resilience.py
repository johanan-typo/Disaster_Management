from simulation.simulation_runner import EnvironmentalIntelligenceNetwork


simulation = EnvironmentalIntelligenceNetwork()

print()
print("=" * 80)
print("STAGE-1 OFFLINE RESILIENCE TEST")
print("=" * 80)

# -------------------------------------------------------------
# 1. Generate a developing flood condition
# -------------------------------------------------------------

simulation.set_scenario("DEVELOPING")
simulation.run(steps=4)

# -------------------------------------------------------------
# 2. Simulate network failure
# -------------------------------------------------------------

print()
print("=" * 80)
print("SIMULATING NETWORK FAILURE")
print("=" * 80)

simulation.network_off()

print(f"Network status      : {simulation.network.get_status()}")
print("Edge processing     : ACTIVE")
print("Local alerts        : ACTIVE")

# -------------------------------------------------------------
# 3. Continue severe/critical conditions while offline
# -------------------------------------------------------------

simulation.set_scenario("SEVERE")
simulation.run(steps=4)

simulation.set_scenario("CRITICAL")
simulation.run(steps=4)

print()
print(f"Network status      : {simulation.network.get_status()}")
print(f"Buffered events     : {simulation.event_buffer.count()}")

# -------------------------------------------------------------
# 4. Restore network
# -------------------------------------------------------------

print()
print("=" * 80)
print("RESTORING NETWORK")
print("=" * 80)

simulation.network_on()

print(f"Network status      : {simulation.network.get_status()}")
print(f"Buffered events     : {simulation.event_buffer.count()}")

print()
print("=" * 80)
print("OFFLINE RESILIENCE TEST COMPLETE")
print("=" * 80)
