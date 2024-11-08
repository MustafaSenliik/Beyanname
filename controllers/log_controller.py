from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from services.log_service import fetch_logs_by_role
from services.metrics_service import increment_request_count, track_request_latency, increment_file_operation_errors

# Blueprint tanımlaması
log_bp = Blueprint('log', __name__)

@log_bp.route('/logs')
@login_required
@track_request_latency('/logs')  # Gecikme süresini izler
def view_logs():
    increment_request_count('/logs')  # İstek sayısını artırır
    try:
        logs = fetch_logs_by_role(current_user)  # Kullanıcı rolüne göre log kayıtlarını çekiyoruz
        return render_template('logs.html', logs=logs)
    except Exception as e:
        increment_file_operation_errors('view_logs')  # Hata sayısını artırır
        flash(f'Log kayıtları alınırken hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('file.upload_file'))
