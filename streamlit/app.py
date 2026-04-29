import streamlit as st
import pandas as pd
from elasticsearch import Elasticsearch
import mysql.connector
import plotly.express as px
import os
from datetime import datetime

# Page config
st.set_page_config(page_title="Cyber Threat Monitor", layout="wide")

# Connection to Elasticsearch
ES_HOST = os.environ.get("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
es = Elasticsearch([ES_HOST])

# Connection to MySQL
def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "mysql"),
            user=os.environ.get("MYSQL_USER", "cyber_user"),
            password=os.environ.get("MYSQL_PASSWORD", "cyber_password"),
            database=os.environ.get("MYSQL_DATABASE", "cyber_threats")
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def fetch_es_data(index_pattern):
    try:
        res = es.search(index=index_pattern, body={"query": {"match_all": {}}, "size": 10000})
        hits = res['hits']['hits']
        data = [hit['_source'] for hit in hits]
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

def fetch_mysql_data(table):
    conn = get_mysql_connection()
    if conn:
        try:
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching data from MySQL {table}: {e}")
    return pd.DataFrame()

st.title("🛡️ Cyber Threat Monitoring Dashboard")

# Sidebar for controls
st.sidebar.header("Controls")
if st.sidebar.button("Refresh Data"):
    st.rerun()

# Tabs for different views
tab_realtime, tab_mysql = st.tabs(["Real-time (ELK)", "Audit Logs (MySQL)"])

with tab_realtime:
    # Fetch data from incidents and alerts
    df_incidents = fetch_es_data("cyber-incidents-*")
    df_alerts = fetch_es_data("alerts")

    if not df_incidents.empty:
        # Standardize incident_type field (Logstash might not have processed yet)
        if 'incident_type' not in df_incidents.columns and 'type' in df_incidents.columns:
            df_incidents['incident_type'] = df_incidents['type']
        
        # Top Row Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Incidents", len(df_incidents))
        m2.metric("Critical Alerts", len(df_alerts) if not df_alerts.empty else 0)
        m3.metric("Active Sectors", df_incidents['sector'].nunique() if 'sector' in df_incidents.columns else 0)
        m4.metric("Attack Types", df_incidents['incident_type'].nunique() if 'incident_type' in df_incidents.columns else 0)

        st.divider()

        # Visualizations
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Incident Count by Sector")
            if 'sector' in df_incidents.columns:
                sector_counts = df_incidents['sector'].value_counts().reset_index()
                sector_counts.columns = ['Sector', 'Count']
                fig_sector = px.pie(sector_counts, values='Count', names='Sector', hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_sector, use_container_width=True)

        with c2:
            st.subheader("Attack Type Distribution")
            if 'incident_type' in df_incidents.columns:
                type_counts = df_incidents['incident_type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                fig_type = px.bar(type_counts, x='Type', y='Count', color='Type',
                                  color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(fig_type, use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:
            st.subheader("Severity Trends")
            # Ensure timestamp is datetime
            ts_field = 'incident_timestamp' if 'incident_timestamp' in df_incidents.columns else 'timestamp'
            if ts_field in df_incidents.columns:
                df_incidents[ts_field] = pd.to_datetime(df_incidents[ts_field])
                df_incidents['hour'] = df_incidents[ts_field].dt.strftime('%H:00')
                severity_trend = df_incidents.groupby(['hour', 'severity']).size().reset_index(name='Count')
                fig_trend = px.line(severity_trend, x='hour', y='Count', color='severity', markers=True)
                st.plotly_chart(fig_trend, use_container_width=True)

        with c4:
            st.subheader("Top Attacking Sources")
            source_field = 'source_api' if 'source_api' in df_incidents.columns else 'source'
            if source_field in df_incidents.columns:
                top_sources = df_incidents[source_field].value_counts().nlargest(10).reset_index()
                top_sources.columns = ['Source', 'Count']
                fig_source = px.bar(top_sources, y='Source', x='Count', orientation='h', color='Count')
                st.plotly_chart(fig_source, use_container_width=True)

        st.subheader("Recent Critical Alerts")
        if not df_alerts.empty:
            st.table(df_alerts.sort_values(by='timestamp', ascending=False).head(10))
        else:
            st.info("No critical alerts triggered yet.")

    else:
        st.warning("No incident data found in Elasticsearch. Please ensure the Python app is running and Logstash is processing logs.")

with tab_mysql:
    st.subheader("Persistent Audit Logs (MySQL)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Structured Incidents")
        df_sql_incidents = fetch_mysql_data("incidents")
        if not df_sql_incidents.empty:
            st.dataframe(df_sql_incidents.sort_values(by='timestamp', ascending=False), use_container_width=True)
        else:
            st.info("No incidents stored in MySQL yet.")
            
    with col2:
        st.write("### Raw Threat Feeds")
        df_sql_feeds = fetch_mysql_data("feeds")
        if not df_sql_feeds.empty:
            st.dataframe(df_sql_feeds.sort_values(by='fetched_at', ascending=False), use_container_width=True)
        else:
            st.info("No raw feeds stored in MySQL yet.")
    
    st.divider()
    st.write("### Alert Configurations")
    df_sql_configs = fetch_mysql_data("alert_configs")
    if not df_sql_configs.empty:
        st.table(df_sql_configs)
