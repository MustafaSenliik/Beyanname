from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.log import Log

@login_required
def view_logs():
    # Only 'patron', 'müdür', or 'müdür_yardımcısı' roles can view logs
    if current_user.rol not in ['patron', 'müdür', 'müdür_yardımcısı']:
        flash('Bu işlemi gerçekleştirmek için yetkiniz yok.', 'danger')
        return redirect(url_for('index'))

    # Fetch logs from the database
    logs = Log.query.order_by(Log.timestamp.desc()).all()

    # Render logs page
    return render_template('logs.html', logs=logs)
