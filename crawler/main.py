from google_play_scraper import app as gapp
from google_play_scraper import reviews as greviews
from google_play_scraper import Sort
from kafka import KafkaProducer
import json
import requests
import schedule
import time
import datetime


def convert_datetimes(obj):
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(i) for i in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


def run_crawler():
    for _ in range(20):
        try:
            response = requests.get("http://api:8000/api/apps/")
            if response.status_code == 200:
                print("response = ", response)
                break
        except Exception as e:
            print("Waiting for API to be ready...")
            time.sleep(10)

    apps = response.json()
    print("apps set")

    from kafka.errors import NoBrokersAvailable

    for _ in range(20):
        try:
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            break
        except NoBrokersAvailable:
            print("Waiting for Kafka to be ready...")
            time.sleep(3)

    for app in apps:
        package_name = app["package_name"]
        try:

            print(package_name)
            details = gapp(package_name)

            wanted_keys_package = [
                # "installs",
                "minInstalls",
                "score",
                "ratings",
                "reviews",
                "updated",
                "version",
                "adSupported",
            ]

            wanted_keys_reviews = [
                "reviewId",
                "userName",
                "content",
                "score",
                "thumbsUpCount",
                "at",
            ]
            details = {k: details[k] for k in wanted_keys_package if k in details}

            reviews, _ = greviews(
                package_name,
                sort=Sort.NEWEST,
                count=1000,
            )

            reviews = [
                {k: review[k] for k in wanted_keys_reviews if k in review}
                for review in reviews
            ]

            timestamp = datetime.datetime.now().isoformat()
            details["timestamp"] = timestamp
            details["app_id"] = app["id"]

            for review in reviews:
                review["timestamp"] = timestamp
                review["app_id"] = app["id"]

            details = convert_datetimes(details)
            reviews = convert_datetimes(reviews)

            producer.send("app_stats", details)

            for review in reviews:
                print("Sending review:", review)
                producer.send("app_reviews", review)

        except Exception as e:
            print(f"Error fetching {package_name}: {e}")

    producer.flush()
    producer.close()


run_crawler()
schedule.every().hour.do(run_crawler)

while True:
    schedule.run_pending()
    time.sleep(1)
