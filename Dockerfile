FROM python:3.11.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/etc/letsencrypt/live/domain/privkey.pem", "--ssl-certfile", "/etc/letsencrypt/live/domain/fullchain.pem"]