from flask import Blueprint, render_template
from flask_login import login_required
from services.log_service import fetch_logs_by_role

# Blueprint tanımlaması
log_bp = Blueprint('log', __name__)

@log_bp.route('/logs')
@login_required
def view_logs():
    # Kullanıcı rolüne göre log kayıtlarını çekiyoruz
    try:
        logs = fetch_logs_by_role(current_user)
        return render_template('logs.html', logs=logs)
    except Exception as e:
        flash(f'Log kayıtları alınırken hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('file.upload_file'))
