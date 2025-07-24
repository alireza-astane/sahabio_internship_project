from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sqlite3


def print_recent_logs():
    conn = sqlite3.connect("/logs/central_logs.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT created, service, level, message FROM logs ORDER BY created DESC LIMIT 10"
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()


with DAG(
    "show_recent_logs",
    default_args={"owner": "airflow"},
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    show_logs = PythonOperator(
        task_id="show_recent_logs",
        python_callable=print_recent_logs,
    )
