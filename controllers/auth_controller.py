from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_login import login_user, logout_user, login_required, current_user
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
        email = request.form.get('email')
        sifre = request.form.get('password')

        user = User.query.filter_by(email=email, is_deleted=False).first()
        if user and user.sifre == sifre:
            login_user(user)
            # Şifre değiştirme durumu kontrolü
            if not user.password_changed:
                flash("Lütfen kendinize yeni bir şifre belirleyin.", "warning")
                return redirect(url_for('auth.change_password'))
            
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('file.upload_file'))

        else:
            flash('Geçersiz giriş bilgileri veya kullanıcı silinmiş!', 'danger')

    return render_template('login.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('auth.login'))
