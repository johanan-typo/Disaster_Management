import React from 'react';
import { useSystemTime } from '../hooks/useSystemTime';
import { Activity, Radio, Cpu, Clock, ShieldAlert } from 'lucide-react';

export default function TopBar({ system = {}, simulation = {}, connectionStatus = 'CONNECTED' }) {
  const systemTime = useSystemTime();

  const isOnline = system.network === 'ONLINE';
  const isRunning = simulation.running;
  const simTimeFormatted = simulation.simulation_time
    ? simulation.simulation_time.replace('T', ' ')
    : 'Waiting for stream...';

  return (
    <header className="top-bar">
      {/* Brand & Project Identity */}
      <div className="brand-section">
        <Activity size={22} color="#38bdf8" />
        <div>
          <h1 className="brand-title">
            ENVIRONMENTAL INTELLIGENCE NETWORK
            <span className="brand-badge">SIH 2026 POC</span>
          </h1>
          <div style={{ fontSize: '0.68rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
            Autonomous Multi-Hazard Sensing & Offline-First Edge Response
          </div>
        </div>
      </div>

      {/* Top Bar Metrics & Dynamic Clock */}
      <div className="top-bar-metrics">
        {/* CRITICAL REQUIREMENT 4 & 26: DYNAMIC SYSTEM TIME vs SIMULATION TIME */}
        <div className="time-clock-display">
          <Clock size={18} color="#38bdf8" />
          <div className="clock-group">
            <span className="clock-title">SYSTEM TIME (ACTUAL LAPTOP)</span>
            <span className="clock-time">{systemTime.time}</span>
            <span className="clock-date">{systemTime.date}</span>
          </div>

          <div style={{ width: '1px', height: '36px', background: 'var(--border-subtle)', margin: '0 4px' }} />

          <div className="clock-group">
            <span className="clock-title" style={{ color: '#94a3b8' }}>SIMULATION TIME</span>
            <span className="clock-time" style={{ fontSize: '0.88rem', color: '#cbd5e1' }}>
              {simTimeFormatted}
            </span>
            <span className="clock-date">
              STEP: <strong style={{ color: '#38bdf8' }}>#{simulation.step ?? 0}</strong> ({simulation.scenario_phase ?? 'NORMAL'})
            </span>
          </div>
        </div>

        {/* Network Status Indicator */}
        <div className="metric-pill">
          <span className="metric-pill-label">NETWORK STATUS</span>
          <div className="metric-pill-value">
            <span className={`status-dot ${isOnline ? 'online' : 'offline'}`} />
            <span style={{ color: isOnline ? 'var(--emerald-accent)' : 'var(--amber-accent)' }}>
              {isOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>
        </div>

        {/* Local Edge Processing */}
        <div className="metric-pill">
          <span className="metric-pill-label">EDGE PROCESSING</span>
          <div className="metric-pill-value">
            <span className="status-dot active" />
            <span style={{ color: 'var(--cyan-accent)' }}>
              {system.edge_processing || 'ACTIVE'}
            </span>
          </div>
        </div>

        {/* Needle Edge AI */}
        <div className="metric-pill">
          <span className="metric-pill-label">NEEDLE EDGE AI</span>
          <div className="metric-pill-value">
            <Cpu size={14} color="#a855f7" />
            <span style={{ color: '#c084fc' }}>
              {system.needle_ai || 'ACTIVE'}
            </span>
          </div>
        </div>

        {/* Server WebSocket Connection */}
        <div className="metric-pill">
          <span className="metric-pill-label">API BACKEND</span>
          <div className="metric-pill-value" style={{ fontSize: '0.75rem' }}>
            {connectionStatus === 'CONNECTED' ? (
              <span style={{ color: 'var(--emerald-accent)' }}>CONNECTED</span>
            ) : connectionStatus === 'RECONNECTING' ? (
              <span style={{ color: 'var(--amber-accent)' }}>RECONNECTING...</span>
            ) : (
              <span style={{ color: 'var(--rose-accent)' }}>BACKEND OFFLINE</span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
