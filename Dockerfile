FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY app.py .
COPY *.sql .

EXPOSE 8000
CMD ["gunicorn", "app:app", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:8000"]
