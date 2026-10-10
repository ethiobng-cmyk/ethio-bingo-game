FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask==3.0.3 pyTelegramBotAPI==4.16.1 gunicorn==21.2.0

COPY . .

CMD gunicorn app:app --bind 0.0.0.0:$PORT
