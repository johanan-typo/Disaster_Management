import React from 'react';
import { AlertCircle, Bell, CheckCircle2 } from 'lucide-react';

export default function AlertPanel({ events = [] }) {
  return (
    <div className="dashboard-panel" style={{ flex: 1 }}>
      <div className="panel-header">
        <span className="panel-title">
          <Bell size={14} color="#f59e0b" />
          ACTIVE HAZARD ALERTS ({events.length})
        </span>
        <span style={{ fontSize: '0.68rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
          AUTHORITATIVE EVENT STATE
        </span>
      </div>

      <div className="panel-body" style={{ maxHeight: '340px' }}>
        {events.length === 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '30px 10px', color: '#64748b', textAlign: 'center', gap: '8px' }}>
            <CheckCircle2 size={24} color="#10b981" />
            <div style={{ fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>All Nodes Operating Normally</div>
            <div style={{ fontSize: '0.7rem' }}>No active WATCH, WARNING or CRITICAL conditions detected by RiskEngine.</div>
          </div>
        ) : (
          events.map((evt) => {
            const isCritical = evt.risk_level === 'CRITICAL';
            const isWarning = evt.risk_level === 'WARNING';
            const itemClass = isCritical 
              ? 'event-item critical' 
              : isWarning 
              ? 'event-item warning' 
              : 'event-item';

            return (
              <div key={evt.event_id || `${evt.node_id}-${evt.timestamp}`} className={itemClass}>
                <div className="event-item-top">
                  <span style={{ fontWeight: 700, color: isCritical ? '#f87171' : '#fb923c' }}>
                    [{evt.risk_level}] Node {evt.node_id} — {evt.location}
                  </span>
                  <span style={{ fontSize: '0.68rem', color: '#94a3b8' }}>
                    {evt.hazard_state}
                  </span>
                </div>

                <div className="event-desc">
                  Risk Score: {(evt.risk_score * 100).toFixed(1)}% | Event: <strong>{evt.event_state}</strong>
                </div>

                {evt.reasons && evt.reasons.length > 0 && (
                  <div className="event-reasons">
                    {evt.reasons.map((r, i) => (
                      <div key={i}>• {r}</div>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
