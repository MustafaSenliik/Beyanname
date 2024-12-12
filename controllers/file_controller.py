from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from services.file_service import upload_file_service, delete_file_service, download_file_service
from services.metrics_service import increment_request_count, track_request_latency, increment_file_upload, increment_file_operation_errors, increment_file_download

# Blueprint tanımlaması
file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@track_request_latency('/upload')  # Gecikme süresini otomatik olarak izler
def upload_file():
    increment_request_count('/upload')  # İstek sayısını artırır
    if request.method == 'POST':
        # Zorunlu alan kontrolü
        if not all([request.form.get('kodu'), request.form.get('urun_adi'), request.form.get('cari_adi')]):
            flash('Lütfen tüm zorunlu alanları doldurun.', 'danger')
            return redirect(request.url)

        try:
            success = upload_file_service(request, current_user)
            if success:
                increment_file_upload()  # Başarılı dosya yükleme sayısını artırır
                flash('Dosya başarıyla yüklendi.', 'success')
        except ValueError as ve:
            flash(str(ve), 'warning')  # Aynı kod hatası
        except Exception as e:
            increment_file_operation_errors('upload')  # Yükleme işlemi hata sayısını artırır
            flash(f'Dosya yüklenirken beklenmeyen bir hata oluştu: {str(e)}', 'danger')
        return redirect(request.url)

    return render_template('upload.html')


@file_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
@track_request_latency('/delete')  # Gecikme süresini otomatik olarak izler
def delete_file(file_id):
    increment_request_count('/delete')  # İstek sayısını artırır
    if current_user.rol not in ['patron', 'müdür', 'müdür_yardımcısı','admin']:
        flash('Dosya silme yetkiniz yok.', 'danger')
        return redirect(url_for('search.search_page'))

    try:
        delete_file_service(file_id, current_user)
        flash('Dosya başarıyla silindi.', 'success')
    except Exception as e:
        increment_file_operation_errors('delete')  # Silme işlemi hata sayısını artırır
        flash(f'Dosya silinirken hata oluştu: {str(e)}', 'danger')

    return redirect(url_for('search.search_page'))

@file_bp.route('/download/<int:file_id>')
@login_required
@track_request_latency('/download')  # Gecikme süresini otomatik olarak izler
def download_file(file_id):
    increment_request_count('/download')  # İstek sayısını artırır
    file_data = download_file_service(file_id)
    if file_data:
        increment_file_download()  # Başarılı dosya indirme sayısını artırır
        return file_data
    increment_file_operation_errors('download')  # İndirme işlemi hata sayısını artırır
    flash('Dosya bulunamadı veya erişim izniniz yok.', 'danger')
    return redirect(url_for('search.search_page'))