import mysql.connector
import os
import time
from datetime import datetime

class DatabaseManager:
    """Handles persistent storage of cyber threats in MySQL."""
    
    def __init__(self):
        self.host = os.environ.get("MYSQL_HOST", "mysql")
        self.user = os.environ.get("MYSQL_USER", "root")
        self.password = os.environ.get("MYSQL_PASSWORD", "rootpassword")
        self.database = os.environ.get("MYSQL_DATABASE", "cyber_threats")
        self.conn = None
        self._connect()

    def _connect(self):
        """Attempts to connect to MySQL with retries."""
        for i in range(10):
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                print("MySQL Connected successfully.")
                return
            except mysql.connector.Error as err:
                print(f"MySQL Connection attempt {i+1} failed: {err}")
                time.sleep(5)
        raise Exception("Could not connect to MySQL after multiple attempts.")

    def save_feed(self, raw_data):
        """Saves raw threat feed data."""
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO feeds (source, raw_title, ip_address) VALUES (%s, %s, %s)"
            cursor.execute(query, (raw_data['source'], raw_data['raw_title'], raw_data.get('ip_address')))
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error saving feed: {err}")

    def save_incident(self, incident):
        """Saves a processed incident object."""
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO incidents (incident_id, title, incident_type, severity, sector, source, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # Convert ISO timestamp to MySQL datetime format
            dt = datetime.fromisoformat(incident.timestamp.replace('Z', '+00:00'))
            mysql_ts = dt.strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute(query, (
                incident.id, 
                incident.title, 
                incident.type, 
                incident.severity, 
                incident.sector, 
                incident.source, 
                mysql_ts
            ))
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error saving incident to MySQL: {err}")

    def get_alert_config(self, key):
        """Retrieves an alert configuration value."""
        try:
            cursor = self.conn.cursor()
            query = "SELECT config_value FROM alert_configs WHERE config_key = %s"
            cursor.execute(query, (key,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error getting alert config: {err}")
            return None
