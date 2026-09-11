import React from 'react';
import { Play, Pause, StepForward, RotateCcw, Zap } from 'lucide-react';

export default function SimulationControls({ 
  simulation = {}, 
  onStart, 
  onStop, 
  onStep, 
  onReset, 
  onSelectScenario 
}) {
  const isRunning = simulation.running;
  const currentScenario = simulation.scenario_phase || 'NORMAL';
  const scenarios = ['NORMAL', 'DEVELOPING', 'SEVERE', 'CRITICAL', 'RECOVERY'];

  return (
    <div className="bottom-controls-bar">
      {/* Simulation Execution Controls */}
      <div className="control-btn-group">
        <span style={{ fontSize: '0.72rem', color: '#94a3b8', fontFamily: 'var(--font-mono)', marginRight: '4px' }}>
          SIMULATION CONTROLS:
        </span>

        {isRunning ? (
          <button className="btn btn-warning" onClick={onStop} title="Pause automated simulation">
            <Pause size={14} /> PAUSE
          </button>
        ) : (
          <button className="btn btn-primary" onClick={onStart} title="Run automated simulation">
            <Play size={14} /> START AUTO
          </button>
        )}

        <button className="btn" onClick={onStep} disabled={isRunning} title="Advance simulation by 1 timestep">
          <StepForward size={14} /> STEP (1 TIMESTEP)
        </button>

        <button className="btn btn-danger" onClick={onReset} title="Reset simulation to initial state">
          <RotateCcw size={14} /> RESET
        </button>
      </div>

      {/* Scenario Selection Buttons */}
      <div className="control-btn-group">
        <span style={{ fontSize: '0.72rem', color: '#94a3b8', fontFamily: 'var(--font-mono)', marginRight: '4px' }}>
          <Zap size={12} style={{ display: 'inline', marginRight: '2px', color: '#f59e0b' }} />
          DEMONSTRATION SCENARIO:
        </span>

        {scenarios.map((sc) => {
          const isSelected = currentScenario === sc;
          let btnClass = 'btn';
          if (isSelected) {
            btnClass = sc === 'CRITICAL' ? 'btn btn-danger' : sc === 'SEVERE' ? 'btn btn-warning' : 'btn btn-primary';
          }

          return (
            <button
              key={sc}
              className={btnClass}
              style={{
                borderWidth: isSelected ? '2px' : '1px',
                fontWeight: isSelected ? 700 : 500,
                opacity: isSelected ? 1 : 0.75,
              }}
              onClick={() => onSelectScenario(sc)}
            >
              {sc}
            </button>
          );
        })}
      </div>
    </div>
  );
}
