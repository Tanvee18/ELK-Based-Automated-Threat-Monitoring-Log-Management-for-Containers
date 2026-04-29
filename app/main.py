import time
import logging
import os
import sys

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.incident import Incident
from core.data_source import DataSourceManager
from core.analyzer import IncidentAnalyzer
from core.categorizer import SectorCategorizer
from core.alert_generator import AlertGenerator
from core.database import DatabaseManager

# Setup main application logging
log_dir = "/app/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger("cyber_incidents")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{log_dir}/cyber_threats.log")
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)

def main():
    print("Starting Cyber Threat Monitoring System...")
    
    # Initialize components
    data_source = DataSourceManager()
    analyzer = IncidentAnalyzer()
    categorizer = SectorCategorizer()
    db_manager = None
    alert_generator = None
    
    # Wait for connections
    print("Waiting for database connections...")
    time.sleep(20) 
    
    try:
        db_manager = DatabaseManager()
    except Exception as e:
        print(f"Error: DatabaseManager failed to initialize: {e}")

    try:
        alert_generator = AlertGenerator()
    except Exception as e:
        print(f"Warning: AlertGenerator failed to initialize: {e}")

    print("Generating incidents...")
    
    while True:
        try:
            # 1. Fetch raw data
            raw_data = data_source.fetch_mock_data()
            
            # 2. Persist raw data to MySQL
            if db_manager:
                db_manager.save_feed(raw_data)
            
            # 3. Analyze data (type and severity)
            incident_type, severity = analyzer.analyze(raw_data)
            
            # 4. Categorize sector
            sector = categorizer.categorize(raw_data)
            
            # 5. Create Incident object
            incident = Incident(
                title=raw_data["raw_title"],
                incident_type=incident_type,
                severity=severity,
                sector=sector,
                source=raw_data["source"]
            )
            
            # 6. Log the incident as JSON (for Filebeat -> ELK)
            logger.info(incident.to_json())
            print(f"Logged Incident: {incident.id} - {incident.severity}")
            
            # 7. Persist categorized incident to MySQL
            if db_manager:
                db_manager.save_incident(incident)
            
            # 8. Trigger alert if needed (uses threshold from MySQL)
            if alert_generator:
                min_severity = "Critical"
                if db_manager:
                    db_val = db_manager.get_alert_config("min_alert_severity")
                    if db_val:
                        min_severity = db_val
                alert_generator.trigger_alert(incident, min_severity=min_severity)
                
            # Wait before generating next incident
            time.sleep(2)
            
        except Exception as e:
            print(f"Error generating incident: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
