import React from 'react';
import { useSimulationStream } from './hooks/useSimulationStream';
import TopBar from './components/TopBar';
import SyncStatusBanner from './components/SyncStatusBanner';
import NodeCard from './components/NodeCard';
import FloodWater3D from './three/FloodWater3D';
import RiskOverview from './components/RiskOverview';
import AlertPanel from './components/AlertPanel';
import NetworkController from './components/NetworkController';
import SimulationControls from './components/SimulationControls';
import { Radio, AlertOctagon } from 'lucide-react';

export default function App() {
  const {
    data,
    connectionStatus,
    isSyncing,
    lastSyncBanner,
    triggerStep,
    startSimulation,
    stopSimulation,
    resetSimulation,
    setScenario,
    setNetworkOn,
    setNetworkOff,
  } = useSimulationStream();

  // If backend is disconnected or offline, show clear status without fake values
  if (!data) {
    return (
      <div className="app-container" style={{ alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <div style={{
          background: 'var(--bg-surface)',
          padding: '36px 48px',
          borderRadius: '8px',
          border: '1px solid var(--border-subtle)',
          textAlign: 'center',
          maxWidth: '480px',
        }}>
          <AlertOctagon size={48} color="#f59e0b" style={{ margin: '0 auto 16px' }} />
          <h2 style={{ fontFamily: 'var(--font-mono)', fontSize: '1.25rem', marginBottom: '8px', color: '#fff' }}>
            {connectionStatus === 'BACKEND_OFFLINE' ? 'BACKEND OFFLINE' : 'CONNECTING TO SIMULATION API...'}
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '20px' }}>
            {connectionStatus === 'BACKEND_OFFLINE'
              ? 'The Environmental Intelligence Network backend is not running or unreachable on port 8000. Please start the backend service.'
              : 'Connecting to WebSocket on ws://localhost:8000/ws...'}
          </p>
          <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: '#64748b' }}>
            No synthetic sensor values displayed. Authoritative backend connection required.
          </div>
        </div>
      </div>
    );
  }

  const { system, simulation, nodes, events, risk_overview } = data;

  return (
    <div className="app-container">
      {/* 1. Header Bar: System Time (Live Laptop) & Network / AI Indicators */}
      <TopBar 
        system={system} 
        simulation={simulation} 
        connectionStatus={connectionStatus} 
      />

      {/* 2. Prominent Offline-First Resilience Status Banner */}
      <SyncStatusBanner 
        network={system.network}
        bufferedEvents={system.buffered_events}
        isSyncing={isSyncing}
        lastSync={system.last_sync}
      />

      {/* 3. Main Command Center Grid */}
      <main className="main-dashboard-grid">
        {/* LEFT COLUMN: 5 Live Virtual Nodes */}
        <section className="dashboard-panel" style={{ height: 'calc(100vh - 175px)' }}>
          <div className="panel-header">
            <span className="panel-title">
              <Radio size={14} color="#38bdf8" />
              VIRTUAL SENSOR NODES (5)
            </span>
            <span style={{ fontSize: '0.68rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
              LOCAL EDGE SENSING
            </span>
          </div>

          <div className="panel-body">
            {nodes && nodes.map((node) => (
              <NodeCard key={node.node_id} node={node} />
            ))}
          </div>
        </section>

        {/* CENTER COLUMN: 3D Scientific Flood Fluid Visualization */}
        <section className="center-column" style={{ height: 'calc(100vh - 175px)' }}>
          <FloodWater3D 
            nodes={nodes} 
            scenario={simulation.scenario_phase} 
          />
        </section>

        {/* RIGHT COLUMN: Risk Overview, Network Controller & Active Alerts */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '14px', height: 'calc(100vh - 175px)', overflowY: 'auto' }}>
          {/* Risk Tally & Highest Risk Node */}
          <RiskOverview 
            riskOverview={risk_overview} 
            bufferedCount={system.buffered_events} 
          />

          {/* Software Network Simulation Control & Buffer Status */}
          <NetworkController 
            system={system}
            isSyncing={isSyncing}
            lastSyncBanner={lastSyncBanner}
            onTurnOn={setNetworkOn}
            onTurnOff={setNetworkOff}
          />

          {/* Active Authoritative Hazard Events */}
          <AlertPanel 
            events={events} 
          />
        </section>
      </main>

      {/* 4. Bottom Simulation & Scenario Controls */}
      <SimulationControls 
        simulation={simulation}
        onStart={startSimulation}
        onStop={stopSimulation}
        onStep={triggerStep}
        onReset={resetSimulation}
        onSelectScenario={setScenario}
      />

      {/* 5. Scientific Proof-of-Concept Disclaimer */}
      <footer className="disclaimer-bar">
        SIH 2026 Proof-of-Concept | Environmental Intelligence Network | Deterministic RiskEngine is Authoritative | Needle Edge AI Selects Local Action | Downstream flow represents monitored hazard progression
      </footer>
    </div>
  );
}
