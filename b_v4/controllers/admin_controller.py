from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user
from services import admin_services
from models import User
from werkzeug.security import check_password_hash
from extensions import db
from services import admin_services
from datetime import datetime, timedelta
import pytz

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

# Admin giriş ekranı
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        password = request.form.get('password')
        user = User.query.filter_by(ad_soyad=ad_soyad).first()
        
        if user and check_password_hash(user.sifre, password) and user.rol in ['müdür', 'patron', 'müdür_yardımcısı']:
            login_user(user)
            flash('Başarıyla giriş yaptınız.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Geçersiz giriş bilgileri veya yetkisiz kullanıcı.', 'danger')
            return redirect(url_for('admin.login'))
    
    return render_template('admin/admin_login.html')

# admin_controller.py dosyanızda dashboard endpoint'ini güncelleyin
@admin_blueprint.route('/dashboard')
@login_required
def dashboard():
    users_count = admin_services.get_users_count()
    logs_count = admin_services.get_logs_count()
    print("Total Users:", users_count)
    print("Total Logs:", logs_count)
    return render_template('admin/dashboard.html', users_count=users_count, logs_count=logs_count)

@admin_blueprint.route('/get_upload_data')
@login_required
def get_upload_data():
    weekly_data = admin_services.get_weekly_upload_count()
    monthly_data = admin_services.get_monthly_upload_count()
    return jsonify({
        "weekly": weekly_data,
        "monthly": monthly_data
    })

# Kullanıcı yönetimi sayfası
@admin_blueprint.route('/user-management')
@login_required
def user_management():
    users = admin_services.get_all_users()
    return render_template('admin/user_management.html', users=users)

# Yeni kullanıcı ekleme işlemi
@admin_blueprint.route('/add-user', methods=['POST'])
@login_required
def add_user():
    ad_soyad = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    rol = request.form.get('rol')
    
    if password != confirm_password:
        flash('Şifreler eşleşmiyor.', 'danger')
        return redirect(url_for('admin.user_management'))
    
    if ad_soyad and email and password and rol:
        admin_services.add_user(ad_soyad, email, password, rol)
        flash('Kullanıcı başarıyla eklendi.', 'success')
    else:
        flash('Kullanıcı eklenemedi. Lütfen tüm alanları doldurun.', 'danger')
    
    return redirect(url_for('admin.user_management'))

# Kullanıcı silme işlemi için onay ekranı
@admin_blueprint.route('/delete-user/<int:user_id>', methods=['GET'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/delete_user.html', user=user)

# Kullanıcı silme işlemini onaylama
@admin_blueprint.route('/confirm-delete-user/<int:user_id>', methods=['POST'])
@login_required
def confirm_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı başarıyla silindi.', 'success')
    return redirect(url_for('admin.user_management'))

# Kullanıcı silme sayfası (silinecek tüm kullanıcıların listesi)
@admin_blueprint.route('/delete-user-page', methods=['GET'])
@login_required
def delete_user_page():
    users = User.query.all()
    return render_template('admin/delete_user.html', users=users)

@admin_blueprint.route('/log-records')
@login_required
def log_records():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user_name = request.args.get('user_name')

    logs = []

    # Eğer tarih aralığı veya kullanıcı adı varsa arama yap
    if (start_date and end_date) or user_name:
        timezone = pytz.timezone('Europe/Istanbul')
        
        try:
            if start_date and end_date:
                # Başlangıç tarihini belirle
                start_date = timezone.localize(datetime.strptime(start_date, '%Y-%m-%d'))
                # Bitiş tarihine bir gün ekleyerek günün tamamını kapsamasını sağla
                end_date = timezone.localize(datetime.strptime(end_date, '%Y-%m-%d')) + timedelta(days=1)

            logs = admin_services.get_logs_filtered(start_date, end_date, user_name)
            
            # Eğer logs boşsa kullanıcı veya kayıt bulunamadı mesajı göster
            if not logs:
                flash("Belirtilen kriterlere uygun kayıt bulunamadı.", "warning")
                
        except ValueError:
            flash("Geçersiz tarih formatı. Lütfen YYYY-AA-GG formatında girin.", "warning")
    
    elif start_date or end_date:
        flash("Tarih aralığı ile arama yapmak için her iki tarihi de girin.", "warning")
    
    return render_template('admin/log_records.html', logs=logs)

# Admin panelinden çıkış yapma
@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('admin.login'))

# Kullanıcı yetkilendirme işlemi
@admin_blueprint.route('/authorize_user', methods=['GET', 'POST'])
@login_required
def authorize_user():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        role = request.form.get('role')

        # Geçersiz bir rol seçimini kontrol edin
        if role not in ['çalışan', 'müdür_yardımcısı', 'müdür', 'patron']:
            flash("Lütfen geçerli bir rol seçin.", "danger")
            return redirect(url_for('admin.authorize_user'))

        # Kullanıcıyı sorgula ve rol güncelle
        user = User.query.get(user_id)
        if user:
            user.rol = role
            db.session.commit()  # Güncellemeyi veritabanına kaydet
            flash("Rol başarıyla güncellendi.", "success")
        else:
            flash("Kullanıcı bulunamadı.", "danger")
        
        return redirect(url_for('admin.authorize_user'))

    users = User.query.all()
    return render_template('admin/authorize_user.html', users=users)
