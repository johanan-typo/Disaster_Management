class NetworkSimulator:
    def __init__(self):
        self.network_status = True

    def turn_on(self):
        self.network_status = True
        print("Network is ONLINE")

    def turn_off(self):
        self.network_status = False
        print("Network is OFFLINE")

    def get_status(self):
        return self.network_status