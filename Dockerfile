FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY content_dashboard.py .

EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "content_dashboard:app"]
