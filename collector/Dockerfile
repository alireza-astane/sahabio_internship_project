FROM python:3.10-slim
WORKDIR /app
COPY log_collector.py .
RUN pip install docker
VOLUME ["/logs"]
CMD ["python", "log_collector.py"]