import docker
import sqlite3
import threading
import os
from datetime import datetime

LOG_DB_PATH = "/logs/central_logs.sqlite"
CONTAINERS = [
    "api",
    "crawler",
    "consumer",
    "kafka",
    "zookeeper",
    "airflow",
    "metabase",
]  # Update as needed


def setup_db():
    conn = sqlite3.connect(LOG_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS docker_logs (
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
                    "INSERT INTO docker_logs (container, log, created) VALUES (?, ?, ?)",
                    (container_name, log_line, datetime.now()),
                )
                conn.commit()
                conn.close()
    except Exception as e:
        print(f"Error tailing {container_name}: {e}")


if __name__ == "__main__":
    setup_db()
    threads = []
    for name in CONTAINERS:
        t = threading.Thread(target=tail_logs, args=(name,))
        t.daemon = True
        t.start()
        threads.append(t)
    # Keep the main thread alive
    for t in threads:
        t.join()
