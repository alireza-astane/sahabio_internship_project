#!/bin/bash
docker compose down
docker compose up -d



# docker compose run --rm airflow bash -c "airflow db migrate"
# docker compose run --rm airflow bash -c "airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin"

# sudo chown -R 500:500 ../airflow/logs
# sudo chmod -R 755 ../airflow/logs

# docker compose up -d airflow