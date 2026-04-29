import json
import uuid
from datetime import datetime

class Incident:
    def __init__(self, title, incident_type, severity, sector, source, id=None, timestamp=None):
        self.id = id if id else str(uuid.uuid4())
        self.title = title
        self.type = incident_type
        self.severity = severity
        self.sector = sector
        self.source = source
        # Output timestamp in ISO 8601 format suitable for Elasticsearch
        self.timestamp = timestamp if timestamp else datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "severity": self.severity,
            "sector": self.sector,
            "source": self.source,
            "timestamp": self.timestamp
        }

    def to_json(self):
        return json.dumps(self.to_dict())
