from extensions import db
from datetime import datetime
from pytz import timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    sifre = db.Column(db.String(255), nullable=False)
    kayit_tarihi = db.Column(db.DateTime, default=lambda: datetime.now(timezone('Europe/Istanbul')))
    password_changed = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def is_active(self):
        # Kullanıcının aktif olup olmadığını kontrol eder
        return not self.is_deleted

    def set_password(self, password):
        self.sifre = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.sifre, password)

    def __repr__(self):
        return f"<User {self.ad_soyad}>"
