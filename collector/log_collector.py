import docker
import sqlite3
import threading
import os
from datetime import datetime

LOG_DB_PATH = "/logs/central_logs.sqlite"
CONTAINERS = [
    "docker-api-1",
    "docker-crawler-1",
    "docker-consumer-1",
    "docker-kafka-1",
    "docker-zookeeper-1",
    "docker-airflow-1",
    "docker-metabase-1",
]


def setup_db():
    conn = sqlite3.connect(LOG_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            container TEXT,
            log TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def tail_logs(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        for line in container.logs(stream=True, follow=True, tail=0):
            log_line = line.decode(errors="replace").strip()
            if log_line:
                conn = sqlite3.connect(LOG_DB_PATH)
                conn.execute(
                    "INSERT INTO logs (container, log, created) VALUES (?, ?, ?)",
                    (container_name, log_line, datetime.now()),
                )
                conn.commit()
                conn.close()
                print(f"{container_name}: {log_line}")
    except Exception as e:
        print(f"Error tailing {container_name}: {e}")


import schedule
import time


def start_log_collection():
    setup_db()
    threads = []
    for name in CONTAINERS:
        t = threading.Thread(target=tail_logs, args=(name,))
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == "__main__":
    schedule.every(1).minutes.do(start_log_collection)
    while True:
        schedule.run_pending()
        time.sleep(1)
