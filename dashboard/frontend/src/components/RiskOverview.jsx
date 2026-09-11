import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle, Database } from 'lucide-react';

export default function RiskOverview({ riskOverview = {}, bufferedCount = 0 }) {
  const tally = riskOverview.tally || { NORMAL: 5, WATCH: 0, WARNING: 0, CRITICAL: 0 };
  const highestNode = riskOverview.highest_risk_node || 'None';
  const highestScore = riskOverview.highest_risk_score ?? 0;
  const activeEventsCount = riskOverview.active_events_count ?? 0;

  return (
    <div className="dashboard-panel">
      <div className="panel-header">
        <span className="panel-title">
          <ShieldAlert size={14} color="#38bdf8" />
          SYSTEM RISK OVERVIEW
        </span>
        <span style={{ fontSize: '0.7rem', color: '#94a3b8', fontFamily: 'var(--font-mono)' }}>
          HAZARD: {riskOverview.current_hazard || 'FLOOD'}
        </span>
      </div>

      <div className="panel-body">
        {/* Risk Level Tally Bar */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px' }}>
          <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.25)', borderRadius: '4px', padding: '6px 8px', textAlign: 'center' }}>
            <div style={{ fontSize: '0.62rem', color: '#34d399', fontFamily: 'var(--font-mono)' }}>NORMAL</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>{tally.NORMAL}</div>
          </div>

          <div style={{ background: 'rgba(234, 179, 8, 0.1)', border: '1px solid rgba(234, 179, 8, 0.25)', borderRadius: '4px', padding: '6px 8px', textAlign: 'center' }}>
            <div style={{ fontSize: '0.62rem', color: '#facc15', fontFamily: 'var(--font-mono)' }}>WATCH</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>{tally.WATCH}</div>
          </div>

          <div style={{ background: 'rgba(249, 115, 22, 0.1)', border: '1px solid rgba(249, 115, 22, 0.25)', borderRadius: '4px', padding: '6px 8px', textAlign: 'center' }}>
            <div style={{ fontSize: '0.62rem', color: '#fb923c', fontFamily: 'var(--font-mono)' }}>WARNING</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>{tally.WARNING}</div>
          </div>

          <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '4px', padding: '6px 8px', textAlign: 'center' }}>
            <div style={{ fontSize: '0.62rem', color: '#f87171', fontFamily: 'var(--font-mono)' }}>CRITICAL</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>{tally.CRITICAL}</div>
          </div>
        </div>

        {/* Dynamic Key Indicators */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'rgba(0,0,0,0.25)', borderRadius: '4px', fontSize: '0.75rem' }}>
            <span style={{ color: '#94a3b8' }}>HIGHEST RISK NODE</span>
            <strong style={{ color: highestScore >= 0.75 ? '#f87171' : highestScore >= 0.55 ? '#fbbf24' : '#fff' }}>
              {highestNode}
            </strong>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'rgba(0,0,0,0.25)', borderRadius: '4px', fontSize: '0.75rem' }}>
            <span style={{ color: '#94a3b8' }}>MAX EVIDENCE SCORE</span>
            <strong style={{ color: '#38bdf8' }}>{(highestScore * 100).toFixed(1)}%</strong>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'rgba(0,0,0,0.25)', borderRadius: '4px', fontSize: '0.75rem' }}>
            <span style={{ color: '#94a3b8' }}>ACTIVE HAZARD EVENTS</span>
            <strong style={{ color: activeEventsCount > 0 ? '#fb923c' : '#34d399' }}>
              {activeEventsCount} Active
            </strong>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'rgba(0,0,0,0.25)', borderRadius: '4px', fontSize: '0.75rem' }}>
            <span style={{ color: '#94a3b8' }}>BUFFERED OFFLINE EVENTS</span>
            <strong style={{ color: bufferedCount > 0 ? '#f59e0b' : '#94a3b8' }}>
              {bufferedCount} in Local Buffer
            </strong>
          </div>
        </div>
      </div>
    </div>
  );
}
