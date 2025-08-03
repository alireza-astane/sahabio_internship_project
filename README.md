# Sahab Internship Project: App Data Pipeline

This project is an end-to-end data pipeline designed to collect, process, and analyze app statistics and reviews from the Google Play Store. The pipeline integrates various technologies, including Django, PostgreSQL, Kafka, Docker, and Metabase, to provide a scalable and efficient solution for app data management and analysis.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Usage](#usage)
7. [Pipeline Workflow](#pipeline-workflow)
8. [Architecture](#architecture)
9. [Metabase Integration](#metabase-integration)
10. [Future Improvements](#future-improvements)

---

## Overview

The goal of this project was to build a data pipeline that collects app statistics and reviews from the Google Play Store, processes the data, and stores it in a PostgreSQL database for further analysis. The pipeline also includes sentiment analysis for app reviews and integrates with Metabase for data visualization.

This project was developed as part of an internship at **Sahab Company** and demonstrates the use of modern tools and technologies to solve real-world data engineering challenges.

---

## Features

- **Data Collection**: A crawler fetches app statistics and reviews from the Google Play Store.
- **Data Streaming**: Kafka is used to stream app data (statistics and reviews) in real-time.
- **Data Storage**: PostgreSQL is used to store app data, including statistics, reviews, and sentiment analysis results.
- **Sentiment Analysis**: Reviews are analyzed for sentiment (positive, neutral, negative) using VADER or TextBlob.
- **API**: A Django REST API provides endpoints for managing app data.
- **Visualization**: Metabase is integrated for creating dashboards and visualizing trends in app data.
- **Scalability**: Docker Compose is used to orchestrate services, and Kafka consumers can be scaled horizontally.

---

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Data Streaming**: Kafka, Zookeeper
- **Data Crawling**: `google-play-scraper`
- **Sentiment Analysis**: VADER/TextBlob
- **Visualization**: Metabase
- **Containerization**: Docker, Docker Compose
- **Task Scheduling**: Airflow (planned)
- **Programming Languages**: Python
- **Testing**: Django Test Framework, Kafka Consumer Simulation

---
## Project Structure

```
Sahab/
├── api/                  # Django API for managing app data
│   ├── apps/             # Django app for app data
│   │   ├── migrations/   # Database migrations
│   │   ├── models.py     # Database models
│   │   ├── serializers.py# DRF serializers
│   │   ├── tests.py      # Unit tests
│   │   ├── views.py      # API views
│   ├── config/           # Django project configuration
│   │   ├── settings.py   # Project settings
│   │   ├── urls.py       # URL routing
│   │   ├── wsgi.py       # WSGI entry point
│   ├── manage.py         # Django management script
│   ├── requirements.txt  # Python dependencies for the API
│   ├── Dockerfile        # Dockerfile for the Django API
├── crawler/              # Crawler for fetching app data
│   ├── requirements.txt  # Python dependencies for the crawler
├── docker/               # Docker-related files
│   ├── docker-compose.yml# Docker Compose configuration
│   ├── run.sh            # Script to start the pipeline
├── checklist.txt         # Development checklist
├── README.md             # Project documentation
```

# Project documentation


---

## Setup and Installation

### Prerequisites

Ensure the following tools are installed on your system:

- Docker
- Docker Compose
- Python 3.10+
- PostgreSQL

### Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Sahab

2. **Set Up Docker**:
    Start all services using Docker Compose:
    ```bash
    ./docker/run.sh
    ```

3. **Apply Migrations:**
    Run the following commands to set up the database schema
    ```bash
    docker compose exec api python manage.py makemigrations
    docker compose exec api python manage.py migrate
    ```

4. **Create aKafka Topic:**
   Kafka topics are automatically created by the run.sh script. If needed, you can manually create them:
   ```bash
    docker compose exec kafka kafka-topics.sh --create --topic app_stats --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
    docker compose exec kafka kafka-topics.sh --create --topic app_reviews --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092   
    ```

5. **Install Python Dependencies:**
   Install the required Python packages for the API and crawler:
   ```bash
   docker compose exec api pip install -r api/requirements.txt
   docker compose exec crawler pip install -r crawler/requirements.txt
   ```

## Usage

### Start the Pipeline

1. Run the pipeline using the provided script:
   ```bash
   ./docker/run.sh
   ```

2. Access the Django API at:
   ```
   http://localhost:8000
   ```

3. Access Metabase at:
   ```
   http://localhost:3000
   ```

### API Endpoints

The Django API provides the following endpoints:

- **Apps**:
  - `GET /api/apps/`: List all apps.
  - `POST /api/apps/`: Add a new app.
  - `GET /api/apps/<id>/`: Retrieve app details.
  - `PATCH /api/apps/<id>/`: Update app details.
  - `DELETE /api/apps/<id>/`: Delete an app.

- **Swagger Documentation**:
  - Access the API documentation at:
    ```
    http://localhost:8000/api/docs/
    ```

### Crawler

The crawler fetches app statistics and reviews from the Google Play Store and pushes them to Kafka topics (`app_stats` and `app_reviews`).

---

## Pipeline Workflow

1. **Data Collection**:
   - The crawler fetches app data using the `google-play-scraper` library.
   - Data is pushed to Kafka topics (`app_stats` and `app_reviews`).

2. **Data Processing**:
   - Kafka consumers read data from the topics and insert it into the PostgreSQL database.

3. **Sentiment Analysis**:
   - Reviews are analyzed for sentiment using VADER or TextBlob.
   - Sentiment results are stored in the database.

4. **Visualization**:
   - Metabase is used to create dashboards for analyzing app trends and review sentiments.

---

## Architecture

This project follows a **microservices architecture**. Each component of the pipeline is designed as an independent service, allowing for scalability and modularity. The key components are:

1. **Crawler**:
   - Fetches app data and pushes it to Kafka topics.

2. **Kafka**:
   - Acts as the message broker for streaming app data.

3. **Consumers**:
   - Processes data from Kafka topics and inserts it into the PostgreSQL database.

4. **Django API**:
   - Provides RESTful endpoints for managing and accessing app data.

5. **Metabase**:
   - Visualizes app data and trends.

6. **PostgreSQL**:
   - Stores app statistics, reviews, and sentiment analysis results.

---

## Metabase Integration

### Connecting to Metabase

1. Open your browser and go to:
   ```
   http://localhost:3000
   ```

2. Log in or sign up with the admin account (you’ll be prompted to create one on the first launch).

3. Connect your PostgreSQL database:
   - Go to **Settings** → **Databases** → **Add database**.
   - Fill in the following details:
     - **Database type**: PostgreSQL
     - **Host**: `db`
     - **Port**: `5432`
     - **Database name**: `sahab`
     - **Username**: `sahab`
     - **Password**: `sahab`

4. Start exploring your data and create dashboards.

---

## Testing

### Running Tests

To ensure the functionality of the project, you can run the tests provided for the API, Kafka consumers, and other components.

#### **1. Run Django API Tests**
To run the tests for the Django API:
1. Ensure the Docker services are running:
   ```bash
   ./docker/run.sh
   ```
2. Execute the tests inside the `api` service:
   ```bash
   docker compose exec api python manage.py test
   ```

#### **2. Run Kafka Consumer Tests**
If you have tests for Kafka consumers, you can run them as follows:
1. Ensure Kafka is running.
2. Execute the tests inside the `consumer` service:
   ```bash
   docker compose exec consumer pytest
   ```

#### **3. Run Crawler Tests**
To test the crawler:
1. Navigate to the `crawler` directory:
   ```bash
   cd crawler
   ```
2. Run the tests using `pytest`:
   ```bash
   pytest
   ```
   Alternatively, if running inside Docker:
   ```bash
   docker compose exec crawler pytest
   ```

### Checking Test Coverage (Optional)
To check the test coverage for the Django API:
1. Install `coverage`:
   ```bash
   pip install coverage
   ```
2. Run the tests with coverage:
   ```bash
   docker compose exec api coverage run manage.py test
   ```
3. Generate a coverage report:
   ```bash
   docker compose exec api coverage report
   ```

### Continuous Integration
The project includes a GitLab CI/CD pipeline that automatically runs tests during the `test` stage. The pipeline configuration is defined in the `.gitlab-ci.yml` file:
```yaml
test:
  stage: test
  script:
    - docker compose exec api python manage.py test
```
This ensures that all tests are executed before deployment.

---

By running these tests, you can verify that the project components are functioning as expected and maintain code quality.


---

## Future Improvements

- **Multilingual Sentiment Analysis**: Extend sentiment analysis to support multiple languages.
- **Airflow Integration**: Use Airflow for scheduling and monitoring the crawler.
- **Error Handling**: Add more robust error handling and logging mechanisms.
- **Dashboard Enhancements**: Create more detailed dashboards for app trends and review analysis.
- **Documentation**: Improve API documentation and add examples for common use cases.