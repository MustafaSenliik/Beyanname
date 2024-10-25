from models import BeyannameKayitlari, Log
from extensions import db
from flask import flash, send_file
import io
from datetime import datetime

def upload_file_service(request, current_user):
    kodu = request.form.get('kodu')
    urun_adi = request.form.get('urun_adi')
    # Diğer form alanları...

    # Dosya var mı kontrolü
    existing_record = BeyannameKayitlari.query.filter_by(kodu=kodu).first()
    if existing_record:
        flash(f"{kodu} kodlu bir dosya zaten mevcut.", 'danger')
        return False

    # Dosya yükleme işlemi
    file_data = request.files['pdf_dosyasi'].read()
    beyanname = BeyannameKayitlari(
        kodu=kodu,
        urun_adi=urun_adi,
        # Diğer alanlar...
        atr_belgesi=file_data
    )
    db.session.add(beyanname)
    db.session.commit()

    # Log kaydı ekleme
    log = Log(user_id=current_user.id, action="Dosya Yüklendi", details=f"{kodu} kodlu dosya yüklendi.")
    db.session.add(log)
    db.session.commit()
    return True

def delete_file_service(file_id, current_user):
    file = BeyannameKayitlari.query.get(file_id)
    if file:
        db.session.delete(file)
        db.session.commit()

        # Log kaydı oluşturma
        log = Log(user_id=current_user.id, action="Dosya Silindi", details=f"{file.kodu} kodlu dosya silindi.")
        db.session.add(log)
        db.session.commit()

def download_file_service(file_id):
    file = BeyannameKayitlari.query.get(file_id)
    if file:
        return send_file(
            io.BytesIO(file.atr_belgesi),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{file.kodu}.pdf"
        )
    flash('Dosya bulunamadı.', 'danger')
    return None
