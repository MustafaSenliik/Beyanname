import os

# Çevresel değişkenlerden veritabanı bağlantısını al, eğer bulunmazsa localhost'a bağlan
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 'mysql+pymysql://root:root@localhost:3306/toren'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)

SESSION_COOKIE_NAME = 'your_session_cookie_name'
