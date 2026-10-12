FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir Flask==3.0.2 gunicorn==21.2.0
CMD gunicorn --bind 0.0.0.0:$PORT app:app
