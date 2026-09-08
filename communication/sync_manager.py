from communication.event_buffer import EventBuffer
from communication.network_simulator import NetworkSimulator


class SyncManager:
    """
    Handles store-and-forward communication.

    Events are transmitted immediately when the network
    is online. During an outage they remain in the local
    event buffer and are synchronized after recovery.
    """

    def __init__(self, network=None, buffer=None):
        self.network = network or NetworkSimulator()
        self.buffer = buffer or EventBuffer()

        self.total_transmitted = 0
        self.total_buffered = 0
        self.total_synchronized = 0

    def handle_event(self, event):
        """
        Transmit an event if online.
        Otherwise store it locally.
        """

        if self.network.is_online():

            transmitted = self.network.transmit(event)

            if transmitted:
                self.total_transmitted += 1

                return {
                    "status": "SENT",
                    "event": event,
                }

        self.buffer.add(event)
        self.total_buffered += 1

        return {
            "status": "BUFFERED",
            "event": event,
        }

    def synchronize(self):
        """
        Send all buffered events after network recovery.
        """

        if not self.network.is_online():
            return {
                "status": "WAITING_FOR_NETWORK",
                "synchronized": 0,
                "remaining": self.buffer.count(),
            }

        buffered_events = self.buffer.pop_all()

        synchronized = 0

        for event in buffered_events:

            if self.network.transmit(event):
                synchronized += 1
                self.total_synchronized += 1
            else:
                self.buffer.add(event)

        return {
            "status": (
                "SYNC_COMPLETE"
                if self.buffer.count() == 0
                else "PARTIAL_SYNC"
            ),
            "synchronized": synchronized,
            "remaining": self.buffer.count(),
        }

    def get_status(self):
        """Return communication statistics."""

        return {
            "network": self.network.get_status(),
            "buffered_events": self.buffer.count(),
            "total_transmitted": self.total_transmitted,
            "total_buffered": self.total_buffered,
            "total_synchronized": self.total_synchronized,
        }
