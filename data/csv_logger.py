import csv
import os


class CSVLogger:
    def __init__(self, file_path="data/sensor_data.csv"):
        self.file_path = file_path

        self.fieldnames = [
            "timestamp",
            "node_id",
            "location",
            "rainfall_mm_h",
            "temperature_c",
            "humidity_pct",
            "soil_moisture_pct",
            "water_level_m",
            "wind_speed_m_s",
            "smoke_level",
            "gas_level",
            "soil_stability",
            "rate_of_rise_m_h",
            "trend",
            "risk_score",
            "risk_level",
            "hazard_state",
            "event_state",
            "network_status",
            "edge_processing",
        ]

        self.initialize_file()

    def initialize_file(self):
        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(
                self.file_path,
                mode="w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                )
                writer.writeheader()

    def log_data(self, data):
        with open(
            self.file_path,
            mode="a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames,
                extrasaction="ignore",
            )
            writer.writerow(data)
