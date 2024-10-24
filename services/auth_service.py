from models import User
from flask import flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

def login_user_service(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.sifre, password):
        login_user(user)
        flash('Giriş başarılı!', 'success')
        return redirect(url_for('upload_file'))
    else:
        flash('Geçersiz giriş bilgileri!', 'danger')
        return redirect(url_for('login'))

def register_user_service(ad_soyad, email, password, password_confirm, rol):
    if password != password_confirm:
        flash('Şifreler uyuşmuyor!', 'danger')
        return None

    if rol == 'patron':
        patron_count = User.query.filter_by(rol='patron').count()
        if patron_count >= 3:
            flash('3 patron kaydı zaten mevcut.', 'danger')
            return None

    if User.query.filter_by(email=email).first():
        flash('Bu email zaten kayıtlı.', 'danger')
        return None

    new_user = User(ad_soyad=ad_soyad, email=email, rol=rol)
    new_user.set_password(password)
    return new_user
