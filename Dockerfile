FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir Flask==3.0.2 gunicorn==21.2.0
CMD ["python", "app.py"]
