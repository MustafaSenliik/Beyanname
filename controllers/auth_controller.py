from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from extensions import db
from datetime import timedelta
from services.metrics_service import increment_request_count, track_request_latency, increment_login_attempt

# Blueprint tanımlaması
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
@track_request_latency('/register')  # Gecikme süresini izler
def register():
    increment_request_count('/register')  # İstek sayısını artırır
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

@auth_bp.route('/check_session', methods=['GET'])
@login_required
@track_request_latency('/check_session')  # Gecikme süresini izler
def check_session():
    increment_request_count('/check_session')  # İstek sayısını artırır
    if current_user.is_authenticated:
        return jsonify({'isValid': True})
    else:
        return jsonify({'isValid': False})

@auth_bp.route('/login', methods=['GET', 'POST'])
@track_request_latency('/login')  # Gecikme süresini izler
def login():
    increment_request_count('/login')  # İstek sayısını artırır
    if request.method == 'POST':
        email = request.form.get('email')
        sifre = request.form.get('password')

        user = User.query.filter_by(email=email, is_deleted=False).first()
        if user and user.sifre == sifre:
            # Oturumu kalıcı hale getir
            session.permanent = True
            login_user(user, remember=True)
            increment_login_attempt(success=True)  # Başarılı giriş sayısını artırır

            # Şifre değiştirme durumu kontrolü
            if not user.password_changed:
                flash("Lütfen kendinize yeni bir şifre belirleyin.", "warning")
                return redirect(url_for('auth.change_password'))

            flash('Giriş başarılı!', 'success')
            return redirect(url_for('file.upload_file'))

        else:
            increment_login_attempt(success=False)  # Başarısız giriş sayısını artırır
            flash('Geçersiz giriş bilgileri veya kullanıcı silinmiş!', 'danger')

    return render_template('login.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
@track_request_latency('/change-password')  # Gecikme süresini izler
def change_password():
    increment_request_count('/change-password')  # İstek sayısını artırır
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Şifreler uyuşmuyor!', 'danger')
            return redirect(url_for('auth.change_password'))

        # Şifreyi güncelle ve password_changed alanını True yap
        current_user.sifre = new_password  # Hashleme eklenebilir
        current_user.password_changed = True
        db.session.commit()

        flash('Şifreniz başarıyla güncellendi!', 'success')
        return redirect(url_for('file.upload_file'))

    return render_template('change_password.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
@track_request_latency('/logout')  # Gecikme süresini izler
def logout():
    increment_request_count('/logout')  # İstek sayısını artırır
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('auth.login'))