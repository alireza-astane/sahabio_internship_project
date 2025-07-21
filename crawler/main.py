from google_play_scraper import app as gapp
from google_play_scraper import reviews as greviews
from google_play_scraper import Sort
from kafka import KafkaProducer
import json
import requests

# timestap
import datetime

response = requests.get("http://localhost:8000/api/apps/")
apps = response.json()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

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
            count=10,
        )

        reviews = [
            {k: review[k] for k in wanted_keys_reviews if k in review}
            for review in reviews
        ]

        print(details)
        print(reviews)
        print(reviews[0])

        # TODO: Push details and reviews to Kafka topics

        # add time stamps
        timestamp = datetime.datetime.now().isoformat()
        details["timestamp"] = timestamp
        for review in reviews:
            review["timestamp"] = timestamp

        # Send app stats
        producer.send("app_stats", details)
        # Send reviews
        for review in reviews:
            producer.send("app_reviews", review)

        break

    except Exception as e:
        print(f"Error fetching {package_name}: {e}")
