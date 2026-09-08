from communication.event_buffer import EventBuffer
from data.csv_logger import CSVLogger


class SyncManager:

    def __init__(self):
        self.buffer = EventBuffer()
        self.logger = CSVLogger()

    def synchronize(self):

        events = self.buffer.get_events()

        if not events:
            print("No buffered events to synchronize.")
            return

        print(f"Synchronizing {len(events)} buffered event(s)...")

        for event in events:
            self.logger.log_data(event)

        self.buffer.clear_events()

        print("Synchronization completed successfully.")