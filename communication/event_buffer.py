import json
import os


class EventBuffer:

    def __init__(self):
        self.file_path = "storage/buffered_events.json"

        # Create storage file if it does not exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def add_event(self, event):
        events = self.get_events()

        events.append(event)

        with open(self.file_path, "w") as file:
            json.dump(events, file, indent=4)

        print("Event added to local buffer.")

    def get_events(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def clear_events(self):
        with open(self.file_path, "w") as file:
            json.dump([], file, indent=4)

        print("Event buffer cleared.")