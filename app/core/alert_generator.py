import json
import logging
from elasticsearch import Elasticsearch
import os
import time

class AlertGenerator:
    """Triggers alerts based on severity thresholds and sends them to Elasticsearch."""
    
    def __init__(self):
        self.es_host = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:9200")
        self.es = Elasticsearch([self.es_host], request_timeout=30)
        self.alert_index = "alerts"

        # Create logger for alerts
        self.logger = logging.getLogger("alerts")
        self.logger.setLevel(logging.INFO)
        # Assuming the main app sets up handlers, but we'll add one here just in case
        handler = logging.FileHandler("/app/logs/alerts.log")
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def trigger_alert(self, incident, min_severity="Critical"):
        """Triggers an alert if severity matches or exceeds threshold."""
        # Simple string comparison for this mock-up
        if incident.severity == min_severity:
            alert_data = {
                "alert_type": "CRITICAL_INCIDENT",
                "incident_id": incident.id,
                "incident_title": incident.title,
                "sector": incident.sector,
                "timestamp": incident.timestamp,
                "message": f"Critical incident detected: {incident.title} in {incident.sector} sector."
            }
            
            # Log the alert locally
            self.logger.info(json.dumps(alert_data))
            
            # Send to Elasticsearch directly
            try:
                self.es.index(index=self.alert_index, document=alert_data)
                print(f"Alert sent to ES: {incident.id}")
            except Exception as e:
                print(f"Failed to send alert to ES: {e}")
