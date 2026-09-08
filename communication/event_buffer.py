class EventBuffer:
    """
    Stores important hazard events locally when network
    connectivity is unavailable.
    """

    def __init__(self):
        self.events = []

    def add(self, event):
        """Store an event locally."""

        self.events.append(event)

    def get_all(self):
        """Return all buffered events."""

        return list(self.events)

    def count(self):
        """Return the number of buffered events."""

        return len(self.events)

    def clear(self):
        """Remove all buffered events."""

        self.events.clear()

    def pop_all(self):
        """
        Return all buffered events and clear the buffer.
        """

        events = list(self.events)
        self.events.clear()

        return events
