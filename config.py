import os

# Veritabanı bağlantısı URI'si
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 'mysql+pymysql://root:root@localhost:3306/toren'
)

# SQLAlchemy için takip modifikasyonları kapalı
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask uygulaması için gizli anahtar
SECRET_KEY = os.urandom(24)

# Session ayarları
SESSION_COOKIE_NAME = 'your_session_cookie_name'

# Bağlantı havuzu ve diğer SQLAlchemy ayarları
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,  # Bağlantı havuzundaki maksimum bağlantı sayısı
    "max_overflow": 5,  # Gerekirse açılabilecek ek bağlantılar
    "pool_timeout": 30,  # Havuz dolduğunda bekleme süresi
    "pool_recycle": 1800,  # Bağlantıların yeniden başlatılma süresi
}
