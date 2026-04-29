import random

class SectorCategorizer:
    """Classifies incidents into sectors."""
    
    def __init__(self):
        self.sectors = ["financial", "healthcare", "government", "telecom", "education", "retail"]

    def categorize(self, raw_data):
        """Assigns a sector to the incident."""
        # Random assignment to simulate target sector
        return random.choice(self.sectors)
