from kafka import KafkaConsumer
import json
import psycopg2

from deep_translator import GoogleTranslator
from transformers import pipeline


translator = GoogleTranslator(source="auto", target="en")
sentiment = sentiment = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
)


def sentiment_analysis(text):
    try:
        translated = translator.translate(text)
        return sentiment(translated)[0].get("label")
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return None


conn = psycopg2.connect(
    dbname="sahab",
    user="sahab",
    password="sahab",
    host="db",  # or "localhost" if running outside Docker
    port="5432",
)
cur = conn.cursor()

consumer = KafkaConsumer(
    "app_stats",
    "app_reviews",
    bootstrap_servers="kafka:9092",  # or 'localhost:9092' if running outside Docker
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="sahab_consumer",
)


BATCH_SIZE = 100

review_batch = []

for message in consumer:
    data = message.value
    if message.topic == "app_stats":
        print(f"Processing app stats for app_id: {data.get('app_id')}")
        cur.execute(
            "INSERT INTO apps_appstat (app_id, timestamp, min_installs, score, ratings, reviews, updated, version, ad_supported) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (app_id, timestamp) DO NOTHING",
            (
                data.get("app_id"),
                data.get("timestamp"),
                data.get("minInstalls"),
                data.get("score"),
                data.get("ratings"),
                data.get("reviews"),
                data.get("updated"),
                data.get("version"),
                data.get("adSupported"),
            ),
        )
        conn.commit()
        print(f"Inserted app stats for app_id: {data.get('app_id')}")
    elif message.topic == "app_reviews":
        print(f"Processing review for app_id: {data.get('app_id')}")
        content = data.get("content", "")
        if content:
            sentiment_result = sentiment_analysis(content)
        else:
            sentiment_result = None
        review_batch.append(
            (
                data.get("reviewId"),
                data.get("app_id"),
                data.get("timestamp"),
                data.get("userName"),
                data.get("score"),
                data.get("content"),
                data.get("thumbsUpCount"),
                sentiment_result,
            )
        )
        if len(review_batch) >= BATCH_SIZE:
            cur.executemany(
                "INSERT INTO apps_appreview (review_id, app_id, timestamp, user_name, score, content, thumbs_up, sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (review_id) DO NOTHING",
                review_batch,
            )
            conn.commit()
            review_batch = []
            print(
                f"Inserted {BATCH_SIZE} reviews into the database for app_id: {data.get('app_id')}"
            )

# At the end, insert any remaining reviews
if review_batch:
    cur.executemany(
        "INSERT INTO apps_appreview (review_id, app_id, timestamp, user_name, score, content, thumbs_up, sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (review_id) DO NOTHING",
        review_batch,
    )
    conn.commit()
