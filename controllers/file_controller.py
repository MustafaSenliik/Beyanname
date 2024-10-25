from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from services.file_service import upload_file_service, delete_file_service, download_file_service

# Blueprint tanımlaması
file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Zorunlu alan kontrolü
        if not all([request.form.get('kodu'), request.form.get('urun_adi'), request.form.get('cari_adi')]):
            flash('Lütfen tüm zorunlu alanları doldurun.', 'danger')
            return redirect(request.url)

        try:
            upload_file_service(request, current_user)
            flash('Dosya başarıyla yüklendi.', 'success')
        except Exception as e:
            flash(f'Dosya yüklenirken hata oluştu: {str(e)}', 'danger')
        return redirect(request.url)

    return render_template('upload.html')

@file_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    if current_user.rol not in ['patron', 'müdür', 'müdür_yardımcısı']:
        flash('Dosya silme yetkiniz yok.', 'danger')
        return redirect(url_for('search.search_page'))

    try:
        delete_file_service(file_id, current_user)
        flash('Dosya başarıyla silindi.', 'success')
    except Exception as e:
        flash(f'Dosya silinirken hata oluştu: {str(e)}', 'danger')

    return redirect(url_for('search.search_page'))

@file_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file_data = download_file_service(file_id)
    if file_data:
        return file_data
    flash('Dosya bulunamadı veya erişim izniniz yok.', 'danger')
    return redirect(url_for('search.search_page'))
