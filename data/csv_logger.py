import csv
import os


class CSVLogger:

    def __init__(self, file_path="data/sensor_data.csv"):

        self.file_path = file_path

        self.fieldnames = [

            # Node identity
            "timestamp",
            "node_id",
            "location",

            # Common environmental observations
            "rainfall_mm_h",
            "temperature_c",
            "humidity_pct",
            "soil_moisture_pct",

            # Flood-related observation
            "water_level_m",

            # Fire-related observations
            "wind_speed_m_s",
            "smoke_level",

            # Gas-related observation
            "gas_level",

            # Landslide-related observation
            "soil_stability",

            # Local intelligence state
            "rate_of_rise_m_h",
            "trend",
            "risk_score",
            "risk_level",
            "hazard_state",
            "event_state",

            # System state
            "network_status",
            "edge_processing"
        ]

        self.initialize_file()


    def initialize_file(self):

        # Create directory if it does not exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Create CSV file with headers if it doesn't exist
        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                mode="w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames
                )

                writer.writeheader()


    def log_data(self, data):

        with open(
            self.file_path,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames,
                extrasaction="ignore"
            )

            writer.writerow(data)

        print("Data logged to CSV.")