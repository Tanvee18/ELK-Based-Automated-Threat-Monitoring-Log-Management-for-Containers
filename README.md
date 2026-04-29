# ELK-Based Automated Cyber Threat Monitoring

This project is a complete containerized security stack that simulates cyber threats, processes them using a modular Python application (OOP), and monitors them using ELK (Elasticsearch, Logstash, Filebeat) with a Streamlit dashboard for visualization.

## Architecture
1. **Python App**: Generates mock cyber incidents, analyzes them (severity/type), and logs them as structured JSON.
2. **Filebeat**: Harvests logs from the Python app and forwards them to Logstash.
3. **Logstash**: Parses JSON logs, enriches fields, and routes them to Elasticsearch.
4. **Elasticsearch**: Stores incident logs and critical alerts.
5. **Streamlit**: Provides a real-time visual dashboard for threat analysis. While the assignment mentions Kibana (port 5601), Streamlit was chosen for its superior flexibility in creating custom security metrics and interactive Python-based analytics.
6. **MySQL**: Serves as the persistent DBMS for long-term audit logs, incident triage, and alert configurations.
7. **ILM Policy**: Automatically manages log lifecycle in Elasticsearch (Hot -> Warm -> Cold -> Delete after 90 days).

## Folder Structure
- `app/`: Python OOP application code.
- `elk/`: Configurations for Logstash, Filebeat, and ILM setup.
- `streamlit/`: Streamlit dashboard code.
- `docker-compose.yml`: Main orchestration file.

## Features
- **OOP Design**: Modular Python classes for Incidents, Analysts, and Alerting.
- **Log Lifecycle**: ILM policy deletes logs after 90 days.
- **Real-time Alerting**: Critical incidents are sent to a separate `alerts` index in Elasticsearch.
- **Visual Analytics**: Streamlit dashboard showing sector distribution, severity trends, and top sources.

## How to Run

### 1. Prerequisites
- Docker and Docker Compose installed.

### 2. Start the Stack
Navigate to the project folder and run:
```bash
docker-compose up -d
```

### 3. Access the Dashboard
Once the containers are healthy (wait about 1-2 minutes for ELK to initialize), open your browser to:
- **Streamlit Dashboard**: `http://localhost:8501`

### 4. Verify Components
- **Elasticsearch**: `http://localhost:9200`
- **MySQL**: Accessible on port `3306`

## Testing with Sample Data
The Python application (`cyber-app`) starts generating incidents automatically every 2 seconds. You will see these appearing on the Streamlit dashboard as they are processed by Logstash.

## Log Lifecycle (ILM)
The `elk-setup` container automatically configures a policy named `cyber_logs_policy` that handles:
- **Hot**: Rollover after 7 days or 50GB.
- **Warm**: Shrink shards after 14 days.
- **Cold**: After 30 days.
- **Delete**: Remove data after 90 days.
