from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

def register_user(name, email, password, role):
    # Patron sayısını kontrol et
    if role == 'patron':
        patron_count = User.query.filter_by(rol='patron').count()
        if patron_count >= 3:
            return False, 'Zaten 3 patron kayıtlı. Başka patron kaydı yapılamaz.'  # Hata mesajı döndür

    # Kullanıcının zaten var olup olmadığını kontrol et
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False, 'Bu email zaten kayıtlı!'  # Hata mesajı döndür

    # Yeni kullanıcı kaydı
    new_user = User(ad_soyad=name, email=email, rol=role)
    new_user.password = generate_password_hash(password)  # Şifreyi hashleyip kaydediyoruz
    try:
        db.session.add(new_user)
        db.session.commit()
        return True, 'Kayıt başarıyla tamamlandı!'  # Başarı mesajı döndür
    except Exception as e:
        db.session.rollback()  # Hata durumunda rollback
        return False, 'Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.'  # Hata mesajı döndür


def validate_login(ad_soyad, password):
    user = User.query.filter_by(ad_soyad=ad_soyad).first()
    if user and check_password_hash(user.password, password):  # Şifre doğrulama
        # JWT token oluştur
        access_token = create_access_token(identity=user.id)
        return access_token, 'Giriş başarılı!'  # Başarı mesajı ve token döndür
    else:
        return None, 'Geçersiz giriş bilgileri!'  # Hata mesajı döndür
