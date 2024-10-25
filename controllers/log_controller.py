from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Log
from services.log_service import fetch_logs_by_role

# Blueprint tanımlaması
log_bp = Blueprint('log', __name__)

@log_bp.route('/logs')
@login_required
def view_logs():
    # Sadece patron, müdür ve müdür yardımcısı rolleri görebilir
    if current_user.rol not in ['patron', 'müdür', 'müdür_yardımcısı']:
        flash('Log kayıtlarına erişim yetkiniz yok.', 'danger')
        return redirect(url_for('file.upload_file'))

    # Log kayıtlarını kullanıcı rolüne göre getir
    logs = fetch_logs_by_role(current_user.rol)
    return render_template('logs.html', logs=logs)
