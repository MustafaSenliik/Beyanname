from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from services.file_service import upload_file_service
from services.log_service import log_action
from models import BeyannameKayitlari

@login_required
def upload_file():
    if request.method == 'POST':
        kodu = request.form.get('kodu')
        urun_adi = request.form.get('urun_adi')
        cari_adi = request.form.get('cari_adi')
        atr_belgesi = request.files.get('pdf_dosyasi')

        # Dosya yükleme işlemini gerçekleştirin
        beyanname = upload_file_service(kodu, urun_adi, cari_adi, atr_belgesi, **request.form)
        
        if beyanname:
            db.session.add(beyanname)
            db.session.commit()

            log = log_action("Dosya Yüklendi", f"{kodu} kodlu dosya yüklendi.")
            db.session.add(log)
            db.session.commit()

            flash('Dosya başarıyla yüklendi.', 'success')
        return redirect(url_for('upload_file'))  # Yükleme işleminden sonra tekrar yükleme sayfasına yönlendirin

    # GET isteği için formu render et
    return render_template('upload.html')


@login_required
def delete_file(file_id):
    file = BeyannameKayitlari.query.get(file_id)
    if delete_file_service(file, file.kodu):
        log = log_action("Dosya Silindi", f"{file.kodu} kodlu dosya silindi.")
        db.session.add(log)
        db.session.commit()
        flash('Dosya başarıyla silindi.', 'success')
    else:
        flash('Dosya bulunamadı.', 'danger')
    return redirect(url_for('search_page'))

@login_required
def download_file(file_id):
    file = BeyannameKayitlari.query.get(file_id)
    if file:
        file_data, file_name = download_file_service(file)
        return send_file(file_data, mimetype='application/pdf', as_attachment=True, download_name=file_name)
    flash('Dosya bulunamadı.')
    return redirect(url_for('search_page'))

def download_csv():
    files = BeyannameKayitlari.query.all()
    csv_data = prepare_csv(files)

    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)

    output = make_response('\ufeff' + si.getvalue())  # UTF-8 BOM eklenmesi
    output.headers["Content-Disposition"] = "attachment; filename=dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output
