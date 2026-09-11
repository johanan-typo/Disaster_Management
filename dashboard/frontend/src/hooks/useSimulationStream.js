import { useState, useEffect, useRef, useCallback } from 'react';

const WS_PATH = '/ws';
const API_BASE = '/api';

export function useSimulationStream() {
  const [data, setData] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('CONNECTING'); // CONNECTED, RECONNECTING, BACKEND_OFFLINE
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncBanner, setLastSyncBanner] = useState(null);

  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const retryCountRef = useRef(0);
  const isMountedRef = useRef(true);

  // Direct REST fetch to populate/update state
  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/status`);
      if (res.ok) {
        const payload = await res.json();
        if (payload && payload.system) {
          setData(payload);
          setConnectionStatus('CONNECTED');
        }
      }
    } catch (e) {
      // Handled by connectionStatus
    }
  }, []);

  // Connect WebSocket
  const connect = useCallback(() => {
    if (!isMountedRef.current) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}${WS_PATH}`;

    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        if (!isMountedRef.current) return;
        setConnectionStatus('CONNECTED');
        retryCountRef.current = 0;
      };

      ws.onmessage = (event) => {
        if (!isMountedRef.current) return;
        try {
          const payload = JSON.parse(event.data);
          if (payload.system) {
            setData(payload);

            // Handle sync banner updates
            const syncInfo = payload.system.last_sync;
            if (syncInfo && syncInfo.status === 'SYNC_COMPLETE') {
              setLastSyncBanner({
                status: 'SYNC_COMPLETE',
                synced_events: syncInfo.synced_events,
                synced_records: syncInfo.synced_records,
                timestamp: syncInfo.timestamp,
              });
            }
          }
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      ws.onerror = () => {
        // Socket error handled in onclose
      };

      ws.onclose = () => {
        if (!isMountedRef.current) return;
        setConnectionStatus(retryCountRef.current > 3 ? 'BACKEND_OFFLINE' : 'RECONNECTING');
        retryCountRef.current += 1;

        const delay = Math.min(1000 * Math.pow(1.5, retryCountRef.current), 4000);
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, delay);
      };
    } catch (err) {
      if (isMountedRef.current) {
        setConnectionStatus('BACKEND_OFFLINE');
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      }
    }
  }, []);

  useEffect(() => {
    isMountedRef.current = true;
    
    // Initial fetch via REST immediately
    fetchStatus();
    
    // Connect WebSocket
    connect();

    // Fallback polling interval every 2.5 seconds to ensure live sync even if WS lags
    const pollTimer = setInterval(() => {
      fetchStatus();
    }, 2500);

    return () => {
      isMountedRef.current = false;
      clearInterval(pollTimer);
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect, fetchStatus]);

  // REST API Actions with IMMEDIATE state updates
  const triggerStep = async () => {
    try {
      const res = await fetch(`${API_BASE}/simulation/step`, { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
      }
      return payload;
    } catch (e) {
      console.error('Failed to trigger step:', e);
    }
  };

  const startSimulation = async () => {
    try {
      const res = await fetch(`${API_BASE}/simulation/start`, { method: 'POST' });
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
      }
      return payload;
    } catch (e) {
      console.error('Failed to start simulation:', e);
    }
  };

  const stopSimulation = async () => {
    try {
      const res = await fetch(`${API_BASE}/simulation/stop`, { method: 'POST' });
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
      }
      return payload;
    } catch (e) {
      console.error('Failed to stop simulation:', e);
    }
  };

  const resetSimulation = async () => {
    try {
      const res = await fetch(`${API_BASE}/simulation/reset`, { method: 'POST' });
      setLastSyncBanner(null);
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
      }
      return payload;
    } catch (e) {
      console.error('Failed to reset simulation:', e);
    }
  };

  const setScenario = async (scenario) => {
    try {
      const res = await fetch(`${API_BASE}/scenario/${scenario}`, { method: 'POST' });
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
      }
      return payload;
    } catch (e) {
      console.error('Failed to set scenario:', e);
    }
  };

  const setNetworkOn = async () => {
    try {
      setIsSyncing(true);
      const res = await fetch(`${API_BASE}/network/on`, { method: 'POST' });
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
        const syncInfo = payload.system.last_sync;
        if (syncInfo && syncInfo.status === 'SYNC_COMPLETE') {
          setLastSyncBanner({
            status: 'SYNC_COMPLETE',
            synced_events: syncInfo.synced_events,
            synced_records: syncInfo.synced_records,
            timestamp: syncInfo.timestamp,
          });
        }
      }
      setTimeout(() => {
        setIsSyncing(false);
      }, 1200);
      return payload;
    } catch (e) {
      setIsSyncing(false);
      console.error('Failed to turn network ON:', e);
    }
  };

  const setNetworkOff = async () => {
    try {
      const res = await fetch(`${API_BASE}/network/off`, { method: 'POST' });
      const payload = await res.json();
      if (payload && payload.system) {
        setData(payload);
      }
      return payload;
    } catch (e) {
      console.error('Failed to turn network OFF:', e);
    }
  };

  return {
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
  };
}
