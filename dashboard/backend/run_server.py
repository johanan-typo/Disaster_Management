"""
Runner script for the Environmental Intelligence Network API backend.
Starts uvicorn on 0.0.0.0:8000.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

if __name__ == "__main__":
    print("=" * 80)
    print("STARTING ENVIRONMENTAL INTELLIGENCE NETWORK API BACKEND")
    print("Binding to http://0.0.0.0:8000 (WebSocket at ws://0.0.0.0:8000/ws)")
    print("=" * 80)
    uvicorn.run(
        "dashboard.backend.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
