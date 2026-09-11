# Environmental Intelligence Network

### Offline-First Multi-Hazard Environmental Intelligence & Local Risk Inference

An offline-first environmental intelligence system designed for **rural, remote, and connectivity-constrained deployments**.

The system combines virtual environmental sensing, temporal reasoning, sensor fusion, deterministic risk assessment, local Edge AI decision support, and store-and-forward communication into a single resilient architecture.

> **SIH 2026 — Phase 1 Prototype**

---

## 🌍 Problem Statement

Environmental monitoring systems often depend on continuous internet connectivity for centralized processing, visualization, and alert generation.

In rural and disaster-prone regions, network connectivity may be unreliable exactly when critical decisions are required.

This project explores an alternative approach:

> **Environmental intelligence should continue locally even when communication fails.**

The network therefore separates:

- Local sensing
- Local intelligence
- Risk assessment
- Local response selection
- Communication
- Cloud/network synchronization

This allows a node to continue detecting and responding to hazards during temporary network outages.

---

# 🎯 Objectives

- Monitor environmental conditions across distributed nodes.
- Analyze environmental measurements over time.
- Combine multiple sensor parameters using sensor fusion.
- Calculate deterministic hazard risk locally.
- Detect developing and critical environmental events.
- Continue local processing during network failure.
- Buffer actionable events while offline.
- Synchronize buffered events when connectivity returns.
- Provide a real-time browser dashboard.
- Visualize flood conditions in 3D.
- Provide an extensible architecture for multiple hazards.

---

# 🧠 System Architecture

```text
                 ┌──────────────────────────┐
                 │   Environmental Inputs   │
                 │ Rainfall / Water / Soil  │
                 │ Temperature / Humidity   │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │      Virtual Nodes       │
                 │     A B C D E            │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   Temporal Intelligence  │
                 │ Trend / Rate / Persistence│
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │      Sensor Fusion       │
                 │ Multi-parameter evidence │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │       Risk Engine        │
                 │ NORMAL / WATCH / WARNING │
                 │        / CRITICAL         │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │        Edge AI            │
                 │ Local response selection  │
                 └────────────┬─────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │ Network ONLINE  │       │ Network OFFLINE │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │ Transmit Event  │       │ Local Buffer    │
        │ + CSV Logging   │       │ Store & Forward │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     Web Dashboard        │
                 │ React + FastAPI + WS     │
                 └──────────────────────────┘
