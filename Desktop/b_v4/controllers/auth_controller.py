from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from extensions import db
from werkzeug.security import check_password_hash
import datetime

# Blueprint tanımlaması
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ad_soyad = request.form.get('name')
        email = request.form.get('email')
        sifre = request.form.get('password')
        sifre_tekrar = request.form.get('password_confirm')
        rol = request.form.get('rol')

        # Şifrelerin uyuşup uyuşmadığını kontrol ediyoruz
        if sifre != sifre_tekrar:
            flash('Şifreler uyuşmuyor!', 'danger')
            return redirect(url_for('auth.register'))

        # Emailin zaten kayıtlı olup olmadığını kontrol ediyoruz
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Bu email zaten kayıtlı!', 'danger')
            return redirect(url_for('auth.register'))

        # Yeni kullanıcıyı veritabanına ekleme
        new_user = User(ad_soyad=ad_soyad, email=email, rol=rol)
        new_user.set_password(sifre)  # Şifreyi hashleyerek kaydediyoruz
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarıyla tamamlandı!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        sifre = request.form.get('password')

        user = User.query.filter_by(ad_soyad=ad_soyad).first()
        if user and user.sifre == sifre:  # `password` yerine `sifre` özniteliğini kullanın
            # Kullanıcıyı oturum açmış olarak işaretle
            login_user(user)

            # JWT token oluştur
            access_token = create_access_token(identity=user.id)
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('file.upload_file'))  # Yükleme sayfasına yönlendirme

        else:
            flash('Geçersiz giriş bilgileri!', 'danger')

    return render_template('login.html')



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('auth.login'))
