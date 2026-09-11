import React from 'react';
import { Wifi, WifiOff, RefreshCw, Database } from 'lucide-react';

export default function NetworkController({ 
  system = {}, 
  isSyncing = false, 
  lastSyncBanner = null,
  onTurnOn, 
  onTurnOff 
}) {
  const isOnline = system.network === 'ONLINE';
  const bufferedEvents = system.buffered_events ?? 0;
  const pendingRecords = system.pending_csv_records ?? 0;
  const loggingStatus = system.csv_logging || 'ACTIVE';

  return (
    <div className="dashboard-panel">
      <div className="panel-header">
        <span className="panel-title">
          {isOnline ? <Wifi size={14} color="#10b981" /> : <WifiOff size={14} color="#f59e0b" />}
          NETWORK & OFFLINE RESILIENCE
        </span>
        <span className={`status-dot ${isOnline ? 'online' : 'offline'}`} />
      </div>

      <div className="panel-body">
        {/* Network Toggle Button */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: '#94a3b8' }}>
              SIMULATED CONNECTIVITY:
            </span>
            <span style={{ 
              fontFamily: 'var(--font-mono)', 
              fontWeight: 700, 
              fontSize: '0.85rem',
              color: isOnline ? 'var(--emerald-accent)' : 'var(--amber-accent)' 
            }}>
              ● {isOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>

          {isOnline ? (
            <button 
              className="btn btn-warning" 
              onClick={onTurnOff}
              style={{ width: '100%', justifyContent: 'center' }}
            >
              <WifiOff size={14} />
              TURN NETWORK OFF (SIMULATE OUTAGE)
            </button>
          ) : (
            <button 
              className="btn btn-primary" 
              onClick={onTurnOn}
              style={{ width: '100%', justifyContent: 'center' }}
            >
              <RefreshCw size={14} className={isSyncing ? 'spin' : ''} />
              RESTORE NETWORK & SYNCHRONIZE
            </button>
          )}
        </div>

        {/* Offline Store-and-Forward Stats */}
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '6px', 
          background: 'rgba(0, 0, 0, 0.3)', 
          padding: '10px', 
          borderRadius: '4px',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.72rem'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: '#94a3b8' }}>Buffered Events:</span>
            <strong style={{ color: bufferedEvents > 0 ? '#f59e0b' : '#34d399' }}>
              {bufferedEvents}
            </strong>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: '#94a3b8' }}>Buffered CSV Records:</span>
            <strong style={{ color: pendingRecords > 0 ? '#f59e0b' : '#34d399' }}>
              {pendingRecords}
            </strong>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: '#94a3b8' }}>CSV Logger Mode:</span>
            <strong style={{ color: isOnline ? 'var(--emerald-accent)' : '#fbbf24' }}>
              {isOnline ? 'DIRECT ACTIVE' : 'STORE-AND-FORWARD'}
            </strong>
          </div>

          {/* Sync status notification */}
          {lastSyncBanner && (
            <div style={{ 
              marginTop: '4px', 
              padding: '6px 8px', 
              background: 'rgba(56, 189, 248, 0.12)', 
              borderRadius: '4px', 
              border: '1px solid rgba(56, 189, 248, 0.3)',
              color: '#38bdf8',
              fontSize: '0.68rem',
              textAlign: 'center'
            }}>
              ✓ SYNC COMPLETE: {lastSyncBanner.synced_events} events & {lastSyncBanner.synced_records} records transmitted
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
