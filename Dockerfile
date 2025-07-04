FROM python:3.10-slim

# Çalışma dizini oluştur
WORKDIR /app

# Gerekli bağımlılıkları yükle
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    apt-get clean

# Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

RUN pip install gunicorn

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "--timeout", "300", "--keep-alive", "120", "--max-requests", "1000", "--max-requests-jitter", "50", "app:app"]

