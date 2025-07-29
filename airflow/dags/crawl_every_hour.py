from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import timedelta


default_args = {
    "owner": "sahab",
    "depends_on_past": False,
    "email": ["apoorhass@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    "run_crawler_hourly",
    default_args=default_args,
    description="Run crawler every hour",
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    run_crawler = BashOperator(
        task_id="run_crawler",
        bash_command="python /opt/airflow/crawler/main.py",
    )
