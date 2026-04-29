import random
import time

class DataSourceManager:
    """Simulates fetching mock cyber threat data from APIs."""
    
    def __init__(self):
        self.sources = ["CERT-In", "AbuseIPDB", "Simulated-Feed-A", "Simulated-Feed-B"]
        self.titles = [
            "Suspicious Login Attempt",
            "Malicious Payload Detected",
            "High Volume Traffic Spike",
            "Unauthorized Access",
            "Data Exfiltration Attempt",
            "Ransomware Encryption Activity",
            "Lateral Movement Detected",
            "Brute Force Attack"
        ]

    def fetch_mock_data(self):
        """Generates a raw threat event."""
        return {
            "raw_title": random.choice(self.titles),
            "source": random.choice(self.sources),
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        }
