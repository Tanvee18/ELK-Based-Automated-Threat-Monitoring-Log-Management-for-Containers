CREATE DATABASE IF NOT EXISTS cyber_threats;
USE cyber_threats;

-- Table for raw feeds
CREATE TABLE IF NOT EXISTS feeds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    raw_title TEXT NOT NULL,
    ip_address VARCHAR(45),
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for categorized incidents
CREATE TABLE IF NOT EXISTS incidents (
    incident_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    incident_type VARCHAR(100),
    severity VARCHAR(50),
    sector VARCHAR(100),
    source VARCHAR(100),
    timestamp DATETIME
);

-- Table for alert configurations
CREATE TABLE IF NOT EXISTS alert_configs (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value VARCHAR(255) NOT NULL
);

-- Default configurations
INSERT IGNORE INTO alert_configs (config_key, config_value) VALUES ('min_alert_severity', 'Critical');
INSERT IGNORE INTO alert_configs (config_key, config_value) VALUES ('alert_cooldown_seconds', '60');
