import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kullaniciadi:parola@localhost:3306/veritabaniadi'  
SQLALCHEMY_TRACK_MODIFICATIONS = False  

SECRET_KEY = os.urandom(24)
