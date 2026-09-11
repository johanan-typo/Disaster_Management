import React from 'react';
import { 
  Droplet, 
  CloudRain, 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  Thermometer, 
  ShieldAlert, 
  Cpu, 
  Wifi, 
  WifiOff 
} from 'lucide-react';

export default function NodeCard({ node }) {
  if (!node) return null;

  const {
    node_id,
    location,
    water_level_m,
    rainfall_mm_h,
    rate_of_rise_m_h,
    soil_moisture_pct,
    temperature_c,
    humidity_pct,
    trend,
    risk_score,
    risk_level,
    hazard_state,
    event_state,
    network_status,
    edge_ai_response,
  } = node;

  const isCritical = risk_level === 'CRITICAL';
  const isWarning = risk_level === 'WARNING';
  const isWatch = risk_level === 'WATCH';

  const badgeClass = isCritical 
    ? 'badge badge-critical' 
    : isWarning 
    ? 'badge badge-warning' 
    : isWatch 
    ? 'badge badge-watch' 
    : 'badge badge-normal';

  const cardBorderClass = isCritical 
    ? 'node-card border-critical' 
    : isWarning 
    ? 'node-card border-warning' 
    : 'node-card';

  // Trend icon
  const renderTrendIcon = () => {
    if (trend === 'RISING') return <TrendingUp size={13} color="#f87171" />;
    if (trend === 'FALLING') return <TrendingDown size={13} color="#34d399" />;
    return <Minus size={13} color="#94a3b8" />;
  };

  // Edge AI action badge style
  const getAiActionStyle = (action) => {
    if (action === 'CRITICAL_LOCAL_ALERT') return { color: '#f87171', bg: 'rgba(239, 68, 68, 0.15)' };
    if (action === 'LOCAL_ALERT') return { color: '#fbbf24', bg: 'rgba(245, 158, 11, 0.15)' };
    return { color: '#94a3b8', bg: 'rgba(255, 255, 255, 0.05)' };
  };

  const aiStyle = getAiActionStyle(edge_ai_response);

  return (
    <div className={cardBorderClass}>
      {/* Node Header */}
      <div className="node-card-header">
        <div className="node-title-group">
          <div className="node-name">
            NODE {node_id}
            <span style={{ fontSize: '0.75rem', fontWeight: 'normal', color: '#94a3b8', marginLeft: '6px' }}>
              — {location.toUpperCase()}
            </span>
          </div>
          <div className="node-location">
            Hazard: <strong style={{ color: '#fff' }}>{hazard_state}</strong> | Event: <strong style={{ color: '#fff' }}>{event_state}</strong>
          </div>
        </div>

        {/* Risk Badge */}
        <div className={badgeClass}>
          <ShieldAlert size={11} />
          {risk_level} ({(risk_score * 100).toFixed(0)}%)
        </div>
      </div>

      {/* Primary Sensor Grid */}
      <div className="node-grid-metrics">
        <div className="node-metric-box">
          <span className="box-label">WATER LEVEL</span>
          <div className="box-value" style={{ color: isCritical ? '#f87171' : isWarning ? '#fbbf24' : '#38bdf8' }}>
            <Droplet size={13} style={{ display: 'inline', marginRight: '4px' }} />
            {water_level_m.toFixed(3)} m
          </div>
        </div>

        <div className="node-metric-box">
          <span className="box-label">RAINFALL</span>
          <div className="box-value">
            <CloudRain size={13} style={{ display: 'inline', marginRight: '4px', color: '#60a5fa' }} />
            {rainfall_mm_h.toFixed(1)} mm/h
          </div>
        </div>

        <div className="node-metric-box">
          <span className="box-label">RATE OF RISE</span>
          <div className="box-value" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            {renderTrendIcon()}
            <span>{rate_of_rise_m_h >= 0 ? `+${rate_of_rise_m_h.toFixed(3)}` : rate_of_rise_m_h.toFixed(3)} m/h</span>
          </div>
        </div>

        <div className="node-metric-box">
          <span className="box-label">SOIL MOISTURE</span>
          <div className="box-value">
            {soil_moisture_pct.toFixed(1)}%
          </div>
        </div>

        <div className="node-metric-box">
          <span className="box-label">TEMP & HUMIDITY</span>
          <div className="box-value" style={{ fontSize: '0.78rem' }}>
            <Thermometer size={12} style={{ display: 'inline', marginRight: '2px', color: '#f59e0b' }} />
            {temperature_c.toFixed(1)}°C | {humidity_pct.toFixed(0)}%
          </div>
        </div>

        <div className="node-metric-box">
          <span className="box-label">TREND / PERSISTENCE</span>
          <div className="box-value" style={{ fontSize: '0.78rem' }}>
            {trend}
          </div>
        </div>
      </div>

      {/* Footer: Network & Needle Edge AI Action */}
      <div className="node-footer">
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {network_status === 'ONLINE' ? (
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--emerald-accent)' }}>
              <Wifi size={12} /> NET ONLINE
            </span>
          ) : (
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--amber-accent)' }}>
              <WifiOff size={12} /> NET BUFFERED
            </span>
          )}
        </div>

        {/* Local Needle Edge AI Selected Response */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <Cpu size={12} color="#c084fc" />
          <span 
            style={{
              fontSize: '0.66rem',
              fontWeight: 700,
              padding: '2px 6px',
              borderRadius: '3px',
              color: aiStyle.color,
              background: aiStyle.bg,
              border: `1px solid ${aiStyle.color}40`,
            }}
          >
            {edge_ai_response || 'NO_ACTION'}
          </span>
        </div>
      </div>
    </div>
  );
}
