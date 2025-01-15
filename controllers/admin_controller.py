from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from services import admin_services
from models import User
from werkzeug.security import check_password_hash
from extensions import db
from services import admin_services
from services.admin_services import get_yearly_currency_data, get_monthly_currency_data, get_beyanname_by_kodu, update_beyanname
from services.metrics_service import increment_request_count, track_request_latency, increment_file_operation_errors
from datetime import datetime, timedelta
import pytz

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/login', methods=['GET', 'POST'])
@track_request_latency('/admin/login')  # Gecikme süresini izler
def login():
    increment_request_count('/admin/login')  # İstek sayısını artırır
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        password = request.form.get('password')
        
        user = User.query.filter_by(ad_soyad=ad_soyad, is_deleted=False).first()
        
        if user and check_password_hash(user.sifre, password) and user.rol in ['müdür', 'patron', 'müdür_yardımcısı', 'admin']:
            login_user(user)
            flash('Başarıyla giriş yaptınız.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            increment_file_operation_errors('login')  # Hata sayısını artırır
            flash('Geçersiz giriş bilgileri, yetkisiz kullanıcı veya kullanıcı silinmiş.', 'danger')
            return redirect(url_for('admin.login'))
    
    return render_template('admin/admin_login.html')

# admin_controller.py dosyanızda dashboard endpoint'ini güncelleyin
@admin_blueprint.route('/dashboard')
@login_required
@track_request_latency('/admin/dashboard')  # Gecikme süresini izler
def dashboard():
    increment_request_count('/admin/dashboard')  # İstek sayısını artırır
    users_count = admin_services.get_users_count()
    logs_count = admin_services.get_logs_count()
    return render_template('admin/dashboard.html', users_count=users_count, logs_count=logs_count)

@admin_blueprint.route('/get_upload_data')
@login_required
@track_request_latency('/admin/get_upload_data')  # Gecikme süresini izler
def get_upload_data():
    increment_request_count('/admin/get_upload_data')  # İstek sayısını artırır
    weekly_data = admin_services.get_weekly_upload_count()
    monthly_data = admin_services.get_monthly_upload_count()
    return jsonify({
        "weekly": weekly_data,
        "monthly": monthly_data
    })

@admin_blueprint.route('/user-management')
@login_required
@track_request_latency('/admin/user-management')  # Gecikme süresini izler
def user_management():
    increment_request_count('/admin/user-management')  # İstek sayısını artırır
    users = admin_services.get_all_users()
    return render_template('admin/user_management.html', users=users)

# Yeni kullanıcı ekleme işlemi
@admin_blueprint.route('/add-user', methods=['POST'])
@login_required
@track_request_latency('/admin/add-user')  # Gecikme süresini izler
def add_user():
    increment_request_count('/admin/add-user')  # İstek sayısını artırır
    ad_soyad = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    rol = request.form.get('rol')
    
    if password != confirm_password:
        flash('Şifreler eşleşmiyor.', 'danger')
        return redirect(url_for('admin.user_management'))
    
    try:
        admin_services.add_user(ad_soyad, email, password, rol)
        flash('Kullanıcı başarıyla eklendi.', 'success')
    except Exception as e:
        increment_file_operation_errors('add_user')  # Hata sayısını artırır
        flash('Kullanıcı eklenemedi.', 'danger')
    
    return redirect(url_for('admin.user_management'))


# Page listing all users for deletion
@admin_blueprint.route('/delete-user-page', methods=['GET'])
@login_required
def delete_user_page():
    users = User.query.filter_by(is_deleted=False).all()
    return render_template('admin/delete_user.html', users=users)

# Kullanıcı silme işlemini onaylama
@admin_blueprint.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@track_request_latency('/admin/delete-user')  # Gecikme süresini izler
def delete_user(user_id):
    increment_request_count('/admin/delete-user')  # İstek sayısını artırır
    if current_user.rol != 'admin':
        flash("Bu işlemi sadece admin yapabilir.", "danger")
        return redirect(url_for('admin.user_management'))
    
    try:
        user = User.query.get_or_404(user_id)
        user.is_deleted = True
        db.session.commit()
        flash(f"{user.ad_soyad} başarıyla silindi.", 'success')
    except Exception as e:
        increment_file_operation_errors('delete_user')  # Hata sayısını artırır
        flash('Kullanıcı silinemedi.', 'danger')
    
    return redirect(url_for('admin.user_management'))


@admin_blueprint.route('/log-records')
@login_required
@track_request_latency('/admin/log-records')  # Gecikme süresini izler
def log_records():
    increment_request_count('/admin/log-records')  # İstek sayısını artırır
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user_name = request.args.get('user_name')

    logs = []

    if (start_date and end_date) or user_name:
        timezone = pytz.timezone('Europe/Istanbul')
        
        try:
            if start_date and end_date:
                start_date = timezone.localize(datetime.strptime(start_date, '%Y-%m-%d'))
                end_date = timezone.localize(datetime.strptime(end_date, '%Y-%m-%d')) + timedelta(days=1)

            logs = admin_services.get_logs_filtered(start_date, end_date, user_name)
            if not logs:
                flash("Belirtilen kriterlere uygun kayıt bulunamadı.", "warning")
                
        except ValueError:
            increment_file_operation_errors('log_records')  # Hata sayısını artırır
            flash("Geçersiz tarih formatı. Lütfen YYYY-AA-GG formatında girin.", "warning")
    
    elif start_date or end_date:
        flash("Tarih aralığı ile arama yapmak için her iki tarihi de girin.", "warning")
    
    return render_template('admin/log_records.html', logs=logs)

# Admin panelinden çıkış yapma
@admin_blueprint.route('/logout')
@login_required
@track_request_latency('/admin/logout')  # Gecikme süresini izler
def logout():
    increment_request_count('/admin/logout')  # İstek sayısını artırır
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('admin.login'))

# Kullanıcı rol seviyelerini tanımlama
ROLE_HIERARCHY = {
    "çalışan": 1,
    "müdür_yardımcısı": 2,
    "müdür": 3,
    "patron": 4,
    "admin": 5
}

@admin_blueprint.route('/authorize_user', methods=['GET', 'POST'])
@login_required
def authorize_user():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')

        # Yeni rolün geçerli bir rol olup olmadığını kontrol et
        if new_role not in ROLE_HIERARCHY:
            flash("Lütfen geçerli bir rol seçin.", "danger")
            return redirect(url_for('admin.authorize_user'))

        # Güncellemek istenen kullanıcıyı sorgula
        user = User.query.get(user_id)
        if user:
            # Giriş yapan kullanıcının rol seviyesini ve hedef kullanıcının rol seviyesini kontrol et
            current_user_role_level = ROLE_HIERARCHY.get(current_user.rol, 0)
            target_user_role_level = ROLE_HIERARCHY.get(user.rol, 0)
            new_role_level = ROLE_HIERARCHY.get(new_role, 0)

            # Eğer giriş yapan kullanıcı, hedef kullanıcıdan daha alt seviyedeyse değişiklik yapmasına izin verme
            if target_user_role_level >= current_user_role_level:
                flash("Kendi seviyenizden veya üst seviyedeki bir kullanıcının yetkisini değiştiremezsiniz.", "danger")
                return redirect(url_for('admin.authorize_user'))

            # Kullanıcı, kendisinden yüksek bir role atama yapamaz
            if new_role_level > current_user_role_level:
                flash("Kendi seviyenizden yüksek bir role atama yapamazsınız.", "danger")
                return redirect(url_for('admin.authorize_user'))

            # Kullanıcı rolünü güncelle
            user.rol = new_role
            db.session.commit()  # Güncellemeyi veritabanına kaydet
            flash("Rol başarıyla güncellendi.", "success")
        else:
            flash("Kullanıcı bulunamadı.", "danger")
        
        return redirect(url_for('admin.authorize_user'))

    # Tüm kullanıcıları getir
    users = User.query.filter_by(is_deleted=False).all()
    return render_template('admin/authorize_user.html', users=users, ROLE_HIERARCHY=ROLE_HIERARCHY)

@admin_blueprint.route('/admin/get_currency_data')
def get_currency_data():
    data = {
        'yearly': get_yearly_currency_data(),
        'monthly': get_monthly_currency_data()
    }
    return jsonify(data)

@admin_blueprint.route('/edit_file', methods=['GET', 'POST'])
@login_required
def edit_file():
    """
    Dosya arama ve düzenleme işlemlerini aynı sayfada gerçekleştirir.
    """
    beyanname = None

    if request.method == 'POST':
        # Düzenleme işlemi
        kodu = request.form.get('kodu')  # POST'tan gelen kodu al

        if not kodu:
            flash('Kodu alınamadı. Lütfen formu doğru şekilde doldurduğunuzdan emin olun.', 'danger')
            return redirect(url_for('admin.edit_file'))

        try:
            intac_tarihi = request.form.get('intac_tarihi')
            # Beyanname kaydını güncelle
            update_beyanname(kodu, intac_tarihi)
            flash('Beyanname kaydı başarıyla güncellendi.', 'success')
            return redirect(url_for('admin.edit_file') + f"?kodu={kodu}")
        except ValueError as e:
            flash(f'Hata: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Bilinmeyen bir hata oluştu: {str(e)}', 'danger')

    elif request.method == 'GET':
        # Arama işlemi
        kodu = request.args.get('kodu')
        if kodu:
            try:
                beyanname = get_beyanname_by_kodu(kodu)
            except ValueError as e:
                flash(f'Hata: {str(e)}', 'danger')

    # Şablonu render et
    return render_template('admin/edit_file.html', file=beyanname)





