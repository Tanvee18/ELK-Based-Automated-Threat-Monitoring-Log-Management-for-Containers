import random

class IncidentAnalyzer:
    """Categorizes attack type and assigns severity."""
    
    def __init__(self):
        self.attack_types = ["phishing", "malware", "DDoS", "APT", "brute_force", "data_leak"]
        self.severities = ["Low", "Medium", "High", "Critical"]

    def analyze(self, raw_data):
        """Analyzes raw data to assign type and severity."""
        
        # Simple heuristic or random assignment for simulation
        title = raw_data.get("raw_title", "").lower()
        
        incident_type = random.choice(self.attack_types)
        severity = random.choice(self.severities)

        if "login" in title or "brute force" in title:
            incident_type = "brute_force"
        elif "payload" in title or "ransomware" in title:
            incident_type = "malware"
            severity = random.choice(["High", "Critical"])
        elif "traffic" in title:
            incident_type = "DDoS"
        elif "exfiltration" in title:
            incident_type = "data_leak"
            severity = "Critical"
        elif "lateral" in title:
            incident_type = "APT"
            severity = "Critical"

        return incident_type, severity
