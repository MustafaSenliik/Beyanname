from models import User, Log  # Veritabanı modellerinizle uyumlu hale getirin
from werkzeug.security import generate_password_hash 
from app import db
# Tüm kullanıcıları getiren fonksiyon
def get_all_users():
    # Veritabanından tüm kullanıcıları getirir
    return User.query.all()

# Tüm log kayıtlarını getiren fonksiyon
def get_all_logs():
    # Veritabanından tüm log kayıtlarını getirir
    return Log.query.order_by(Log.timestamp.desc()).all()

def get_users_count():
    """Toplam kullanıcı sayısını döndürür."""
    return User.query.count()

def get_logs_count():
    """Toplam log kaydı sayısını döndürür."""
    return Log.query.count()

def add_user(ad_soyad, email, password, rol):
    new_user = User(ad_soyad=ad_soyad, email=email, rol=rol)
    new_user.set_password(password)  # Şifreyi hashleyerek kaydeder
    db.session.add(new_user)
    db.session.commit()

# Kullanıcı silme fonksiyonu
def delete_user(user_id):
    # Belirtilen kullanıcıyı veritabanından siler
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

def update_user_rol(user_id, new_rol):
    user = User.query.get(user_id)
    if user:
        user.rol = new_rol
        db.session.commit()