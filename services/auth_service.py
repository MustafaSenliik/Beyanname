from models import User
from extensions import db
from werkzeug.security import generate_password_hash

def register_user(name, email, password, role):
    # Patron sayısını kontrol et
    if role == 'patron':
        patron_count = User.query.filter_by(role='patron').count()
        if patron_count >= 3:
            return False  # Hata mesajları controller katmanına bırakılmalı

    # Kullanıcının zaten var olup olmadığını kontrol et
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False

    # Yeni kullanıcı kaydı
    new_user = User(name=name, email=email, role=role)
    new_user.password = generate_password_hash(password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()  # Hata durumunda rollback
        return False

def validate_login(ad_soyad, password):
    user = User.query.filter_by(ad_soyad=ad_soyad).first()
    if user and user.check_password(password):
        return user
    return None
