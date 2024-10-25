from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from services.search_service import search_files_service, download_csv_service, download_filtered_csv_service

# Blueprint tanımlaması
search_bp = Blueprint('search', __name__)

@search_bp.route('/search_page')
@login_required
def search_page():
    return render_template('index.html')

@search_bp.route('/search', methods=['GET'])
@login_required
def search():
    kategori = request.args.get('kategori')
    kodu = request.args.get('kodu')
    intac_start_date = request.args.get('intac_start_date')
    intac_end_date = request.args.get('intac_end_date')
    ggb_start_date = request.args.get('ggb_start_date')
    ggb_end_date = request.args.get('ggb_end_date')

    # Filtreleme yapılmadıysa kullanıcıyı bilgilendir
    if not (kategori or kodu or intac_start_date or intac_end_date or ggb_start_date or ggb_end_date):
        flash('Lütfen en az bir filtre girin.', 'warning')
        return redirect(url_for('search.search_page'))

    try:
        results = search_files_service(request.args)
        if not results:  # Eğer sonuç yoksa
            flash('Sonuç bulunamadı.', 'info')
        return render_template('index.html', results=results)
    except Exception as e:
        flash(f'Arama sırasında bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('search.search_page'))

@search_bp.route('/download_csv')
@login_required
def download_csv():
    try:
        return download_csv_service()  # Tüm dosyaları CSV olarak indir
    except Exception as e:
        flash(f'CSV dosyası indirilirken hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('search.search_page'))

@search_bp.route('/download_filtered_csv')
@login_required
def download_filtered_csv():
    # Boş filtre kontrolü
    if not (request.args.get('kodu') or request.args.get('kategori') or 
            request.args.get('intac_start_date') or request.args.get('intac_end_date') or 
            request.args.get('ggb_start_date') or request.args.get('ggb_end_date')):
        flash('En az bir filtre girmeniz gerekiyor.', 'warning')
        return redirect(url_for('search.search_page'))

    try:
        # Filtrelenmiş dosyaları al
        results = search_files_service(request.args)  # Burada request.args kullanıyoruz
        return download_filtered_csv_service(results)  # results ile geçin
    except Exception as e:
        flash(f'CSV dosyası indirilirken hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('search.search_page'))


