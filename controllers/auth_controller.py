from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import db

# Blueprint tanımlaması
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Form verilerini alıyoruz
        ad_soyad = request.form.get('name')
        email = request.form.get('email')
        sifre = request.form.get('password')
        sifre_tekrar = request.form.get('password_confirm')
        rol = request.form.get('rol')

        # Şifrelerin uyuşup uyuşmadığını kontrol ediyoruz
        if sifre != sifre_tekrar:
            flash('Şifreler uyuşmuyor!', 'danger')
            return redirect(url_for('auth.register'))

        # Patron kayıt sınırı kontrolü
        if rol == 'patron':
            patron_sayisi = User.query.filter_by(rol='patron').count()
            if patron_sayisi >= 3:
                flash('Zaten 3 patron kayıtlı. Başka patron kaydı yapılamaz.', 'danger')
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
        # Formdan email ve şifre alınıyor
        email = request.form.get('email')
        sifre = request.form.get('password')

        # Kullanıcı veritabanında bulunuyor mu kontrol ediyoruz
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(sifre):
            login_user(user)
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('file.upload_file'))  # Dosya yükleme sayfasına yönlendirme
        else:
            flash('Geçersiz giriş bilgileri!', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('auth.login'))
