#!/bin/bash
docker compose down
docker compose up -d

# Create topics if they don't exist
docker compose exec kafka kafka-topics.sh --create --topic app_stats --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092 || true
docker compose exec kafka kafka-topics.sh --create --topic app_reviews --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092 || true

# Alter partitions for the topics
docker compose exec kafka kafka-topics.sh --alter --topic app_stats --partitions 3 --bootstrap-server localhost:9092
docker compose exec kafka kafka-topics.sh --alter --topic app_reviews --partitions 3 --bootstrap-server localhost:9092

# Scale consumers
docker compose up -d --scale consumer=3