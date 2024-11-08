from prometheus_client import Counter, Summary, Gauge
import psutil
from time import time

# İstek ve Yanıt Metrikleri
REQUEST_COUNT = Counter('request_count', 'Number of requests by endpoint', ['endpoint'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'Latency of requests in seconds', ['endpoint'])
RESPONSE_STATUS = Counter('response_status', 'Response status count by status code', ['status_code'])

# Kaynak Kullanım Metrikleri
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage in percent')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage in percent')

# Veritabanı Metrikleri
DB_QUERY_LATENCY = Summary('db_query_latency_seconds', 'Database query latency in seconds')
DB_QUERY_ERRORS = Counter('db_query_errors', 'Number of database query errors')

# Kullanıcı Oturumu ve Giriş İşlemleri Metrikleri
LOGIN_ATTEMPTS = Counter('login_attempts', 'Number of login attempts', ['status'])
ACTIVE_SESSIONS = Gauge('active_sessions', 'Current active user sessions')

# Dosya Yükleme ve İndirme İşlemleri
FILE_UPLOAD_COUNT = Counter('file_upload_count', 'Number of file uploads')
FILE_DOWNLOAD_COUNT = Counter('file_download_count', 'Number of file downloads')
FILE_OPERATION_ERRORS = Counter('file_operation_errors', 'File operation errors', ['operation'])

# Sistem Kaynaklarını Güncelleme
def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

# İstek Sayaç Fonksiyonu
def increment_request_count(endpoint):
    REQUEST_COUNT.labels(endpoint=endpoint).inc()

# Gecikme Ölçme Fonksiyonu
def track_request_latency(endpoint):
    return REQUEST_LATENCY.labels(endpoint=endpoint).time()

# Yanıt Durumu Sayacı
def increment_response_status(status_code):
    RESPONSE_STATUS.labels(status_code=status_code).inc()

# Veritabanı Sorgu Gecikmesini İzleme
def track_db_query_latency():
    return DB_QUERY_LATENCY.time()

# Veritabanı Sorgu Hatalarını İzleme
def increment_db_query_errors():
    DB_QUERY_ERRORS.inc()

# Giriş Denemeleri
def increment_login_attempt(success):
    LOGIN_ATTEMPTS.labels(status='success' if success else 'failure').inc()

# Aktif Oturum Sayısını Ayarlama
def set_active_sessions(count):
    ACTIVE_SESSIONS.set(count)

# Dosya Yükleme ve İndirme Sayaçları
def increment_file_upload():
    FILE_UPLOAD_COUNT.inc()

def increment_file_download():
    FILE_DOWNLOAD_COUNT.inc()

# Dosya İşlem Hatalarını İzleme
def increment_file_operation_errors(operation):
    FILE_OPERATION_ERRORS.labels(operation=operation).inc()
