import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/toren'  
SQLALCHEMY_TRACK_MODIFICATIONS = False  

SECRET_KEY = os.urandom(24)