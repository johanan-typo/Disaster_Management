import React from 'react';
import { Wifi, WifiOff, RefreshCw, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function SyncStatusBanner({ 
  network = 'ONLINE', 
  bufferedEvents = 0, 
  isSyncing = false, 
  lastSync = null 
}) {
  const isOffline = network === 'OFFLINE';

  if (isSyncing) {
    return (
      <div className="network-banner syncing">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <RefreshCw size={14} className="spin" />
          <strong>SYNCHRONIZING WITH CENTRAL NETWORK...</strong>
          <span>Transmitting buffered events & records</span>
        </div>
        <div>
          <span>RESTORING SYNCHRONIZATION</span>
        </div>
      </div>
    );
  }

  if (isOffline) {
    return (
      <div className="network-banner offline">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <WifiOff size={14} />
          <strong>NETWORK OFFLINE (SIMULATED)</strong>
          <span>— Local Sensing, Sensor Fusion, RiskEngine & Needle Edge AI Active</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span>STORE-AND-FORWARD ACTIVE</span>
          <strong style={{ background: 'rgba(245, 158, 11, 0.25)', padding: '2px 8px', borderRadius: '4px', border: '1px solid rgba(245, 158, 11, 0.4)' }}>
            BUFFERED EVENTS: {bufferedEvents}
          </strong>
        </div>
      </div>
    );
  }

  return (
    <div className="network-banner online">
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Wifi size={14} />
        <strong>NETWORK ONLINE</strong>
        <span>— Direct Sensor Logging Active | Local Edge Intelligence Running Continuously</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ color: '#6ee7b7' }}>✓ STORE-AND-FORWARD READY</span>
        <span style={{ color: '#94a3b8' }}>Buffered Events: <strong>0</strong></span>
      </div>
    </div>
  );
}
