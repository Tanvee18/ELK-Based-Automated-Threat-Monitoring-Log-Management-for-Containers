#!/bin/bash
echo "Waiting for Elasticsearch to be healthy..."
until curl -s http://elasticsearch:9200/_cluster/health | grep -q '"status":"\(green\|yellow\)"'; do
  sleep 5
done

echo "Elasticsearch is up. Configuring ILM Policy..."

# Create ILM policy: hot -> warm -> cold -> delete (delete after 90 days)
curl -s -X PUT "http://elasticsearch:9200/_ilm/policy/cyber_logs_policy" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "7d",
            "max_size": "50gb"
          }
        }
      },
      "warm": {
        "min_age": "14d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
'

echo "Configuring Index Template..."
curl -s -X PUT "http://elasticsearch:9200/_index_template/cyber_template" -H 'Content-Type: application/json' -d'
{
  "index_patterns": ["cyber-incidents-*"],
  "template": {
    "settings": {
      "index.lifecycle.name": "cyber_logs_policy",
      "index.lifecycle.rollover_alias": "cyber-incidents"
    }
  }
}
'

echo "Creating initial rollover index..."
curl -s -X PUT "http://elasticsearch:9200/%3Ccyber-incidents-%7Bnow%2Fd%7D-000001%3E" -H 'Content-Type: application/json' -d'
{
  "aliases": {
    "cyber-incidents": {
      "is_write_index": true
    }
  }
}
'

echo "ILM Setup Complete."
