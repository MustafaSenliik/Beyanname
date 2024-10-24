from extensions import db
from datetime import datetime
import pytz
from pytz import timezone 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class BeyannameKayitlari(db.Model):
    __tablename__ = 'beyanname_kayitlari'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kodu = db.Column(db.String(50), nullable=False)
    urun_adi = db.Column(db.String(50), nullable=False)
    cari_adi = db.Column(db.String(255), nullable=False)
    cari_ulkesi = db.Column(db.String(100))
    miktar = db.Column(db.Numeric(10, 2))
    doviz_cinsi = db.Column(db.String(10))
    kur = db.Column(db.Numeric(10, 4))
    doviz_tutari = db.Column(db.Numeric(15, 2))
    tl_tutari = db.Column(db.Numeric(15, 2))
    gumruk = db.Column(db.String(255))
    intac_tarihi = db.Column(db.Date)
    ggb_tarihi = db.Column(db.Date)
    atr_belgesi = db.Column(db.LargeBinary)
    kategori = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Istanbul')))  # Zaman dilimi ayarlı

    def __init__(self, kodu, urun_adi, cari_adi, cari_ulkesi, miktar, doviz_cinsi, kur, doviz_tutari, tl_tutari, gumruk,
                 intac_tarihi, ggb_tarihi, atr_belgesi, kategori):
        self.kodu = kodu
        self.urun_adi = urun_adi
        self.cari_adi = cari_adi
        self.cari_ulkesi = cari_ulkesi
        self.miktar = miktar
        self.doviz_cinsi = doviz_cinsi
        self.kur = kur
        self.doviz_tutari = doviz_tutari
        self.tl_tutari = tl_tutari
        self.gumruk = gumruk
        self.intac_tarihi = intac_tarihi
        self.ggb_tarihi = ggb_tarihi
        self.atr_belgesi = atr_belgesi
        self.kategori = kategori

    def __repr__(self):
        return f"<BeyannameKayitlari {self.kodu} - {self.urun_adi}>"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    sifre = db.Column(db.String(255), nullable=False)
    kayit_tarihi = db.Column(db.DateTime, default=lambda: datetime.now(timezone('Europe/Istanbul'))) 

    def set_password(self, password):
        self.sifre = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.sifre, password)


    def __repr__(self):
        return f"<User {self.name}>"


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Kullanıcıyla ilişkilendirilmiş
    action = db.Column(db.String(255), nullable=False)  # Yapılan işlem (silme, yükleme vs.)
    details = db.Column(db.String(255), nullable=True)  # İşlem hakkında ek bilgiler
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Istanbul')))  # Zaman dilimi ayarlı
    
    user = db.relationship('User', backref=db.backref('logs', lazy=True))  # Kullanıcı ile ilişki

    def __repr__(self):
        return f"<Log {self.action} by User {self.user_id} on {self.timestamp}>"
