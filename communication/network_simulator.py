class NetworkSimulator:
    """
    Simulates network connectivity for the environmental
    intelligence network.

    Local sensing and edge processing are independent
    of network availability.
    """

    def __init__(self):
        self.status = "ONLINE"

    def turn_off(self):
        """Simulate network failure."""
        self.status = "OFFLINE"

    def turn_on(self):
        """Restore network connectivity."""
        self.status = "ONLINE"

    def is_online(self):
        """Return whether the network is currently online."""
        return self.status == "ONLINE"

    def get_status(self):
        """Return the current network status."""
        return self.status

    def transmit(self, event):
        """
        Simulate transmission of an event.

        Returns True when the network is available,
        otherwise False.
        """

        if not self.is_online():
            return False

        return True
