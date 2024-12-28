FROM python:3.10-slim

# Çalışma dizini oluştur
WORKDIR /app

# Gerekli bağımlılıkları yükle
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Flask uygulamasını başlat
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
