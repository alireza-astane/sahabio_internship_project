FROM python:3.10
WORKDIR /crawler
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]