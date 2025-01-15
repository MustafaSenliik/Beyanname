from flask import flash
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

def register_user(name, email, password, role):
    # Patron sayısını kontrol et
    if role == 'patron':
        patron_count = User.query.filter_by(rol='patron').count()
        if patron_count >= 3:
            print("Patron sayısı 3'ten fazla olamaz.")
            return False, 'Zaten 3 patron kayıtlı. Başka patron kaydı yapılamaz.'

    # Kullanıcının zaten var olup olmadığını kontrol et
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print("Bu email zaten kayıtlı!")
        return False, 'Bu email zaten kayıtlı!'

    # Yeni kullanıcı kaydı
    new_user = User(ad_soyad=name, email=email, password=password, rol=role)
    try:
        db.session.add(new_user)
        db.session.commit()
        print("Kullanıcı başarıyla kaydedildi:", new_user)
        return True, 'Kayıt başarıyla tamamlandı!'
    except Exception as e:
        db.session.rollback()
        print("Kayıt sırasında bir hata oluştu:", str(e))
        return False, 'Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.'


def validate_login(ad_soyad, password):
    user = User.query.filter_by(ad_soyad=ad_soyad).first()
    if user:
        print("Kayıtlı kullanıcı bulundu:", user.ad_soyad)
        print("Veritabanındaki şifre:", user.password)
        print("Girilen şifre:", password)
        if user.password == password:
            access_token = create_access_token(identity=user.id)
            print("Giriş başarılı, token oluşturuldu.")
            return access_token, 'Giriş başarılı!'
        else:
            print("Şifreler eşleşmiyor.")
            return None, 'Geçersiz giriş bilgileri!'
    else:
        print("Kullanıcı bulunamadı.")
        return None, 'Geçersiz giriş bilgileri!'

