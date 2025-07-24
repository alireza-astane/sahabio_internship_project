from kafka import KafkaConsumer
import json
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Connect to PostgreSQL
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

for message in consumer:
    data = message.value
    if message.topic == "app_stats":
        print(f"Received app stats: {data}")
        # Insert into appstatssnapshot table (adjust fields as needed)
        cur.execute(
            "INSERT INTO apps_appstatsnapshot (app_id, timestamp, score, installs, reviews) VALUES (%s, %s, %s, %s, %s)",
            (
                data.get("app_id"),
                data.get("timestamp"),
                data.get("score"),
                data.get("minInstalls"),
                data.get("reviews"),
            ),
        )
    elif message.topic == "app_reviews":
        print(f"Received app review: {data}")
        # Sentiment analysis
        content = data.get("content", "")
        sentiment_score = analyzer.polarity_scores(content)["compound"]
        if sentiment_score >= 0.05:
            sentiment = "positive"
        elif sentiment_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        # Insert into appreview table (adjust fields as needed)
        cur.execute(
            "INSERT INTO apps_appreview (reviewid, app_id, timestamp, content, score, thumbsupcount, username) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (reviewid) DO NOTHING",
            (
                data.get("reviewId"),
                data.get("app_id"),
                data.get("timestamp"),
                data.get("content"),
                data.get("score"),
                data.get("thumbsUpCount"),
                data.get("userName"),
                sentiment,
            ),
        )
    conn.commit()
