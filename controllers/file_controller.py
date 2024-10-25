from flask import Blueprint, request, redirect, url_for, flash, render_template, send_file
from flask_login import login_required, current_user
from models import BeyannameKayitlari, Log
from services.file_service import upload_file_service, delete_file_service, download_file_service
import io

# Blueprint tanımlaması
file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Dosya yükleme işlemleri
        if not all([request.form.get('kodu'), request.form.get('urun_adi'), request.form.get('cari_adi')]):
            flash('Lütfen tüm zorunlu alanları doldurun.', 'danger')
            return redirect(request.url)
        upload_file_service(request, current_user)
        flash('Dosya başarıyla yüklendi.', 'success')
        return redirect(request.url)
    return render_template('upload.html')

@file_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    if current_user.rol not in ['patron', 'müdür', 'müdür_yardımcısı']:
        flash('Dosya silme yetkiniz yok.', 'danger')
        return redirect(url_for('search.search_page'))
    delete_file_service(file_id, current_user)
    flash('Dosya başarıyla silindi.', 'success')
    return redirect(url_for('search.search_page'))

@file_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    return download_file_service(file_id)
