from models import BeyannameKayitlari, Log
from extensions import db
from flask import send_file
import io

def upload_file_service(request, current_user):
    try:
        # Form verilerini alıyoruz
        kodu = request.form.get('kodu')
        urun_adi = request.form.get('urun_adi')
        cari_adi = request.form.get('cari_adi')
        cari_ulkesi = request.form.get('cari_ulkesi')
        miktar = request.form.get('miktar')
        doviz_cinsi = request.form.get('doviz_cinsi')
        kur = request.form.get('kur')
        doviz_tutari = request.form.get('doviz_tutari')
        tl_tutari = request.form.get('tl_tutari')
        gumruk = request.form.get('gumruk')
        intac_tarihi = request.form.get('intac_tarihi')
        ggb_tarihi = request.form.get('ggb_tarihi')
        kategori = request.form.get('kategori')
        atr_belgesi = request.files.get('pdf_dosyasi')

        # Mevcut dosya kontrolü
        existing_record = BeyannameKayitlari.query.filter_by(kodu=kodu).first()
        if existing_record:
            return False  # Mesajı controller katmanına bırakın

        # Dosya verisini oku ve yeni kayıt oluştur
        file_data = atr_belgesi.read()
        beyanname = BeyannameKayitlari(
            kodu=kodu,
            urun_adi=urun_adi,
            cari_adi=cari_adi,
            cari_ulkesi=cari_ulkesi,
            miktar=miktar,
            doviz_cinsi=doviz_cinsi,
            kur=kur,
            doviz_tutari=doviz_tutari,
            tl_tutari=tl_tutari,
            gumruk=gumruk,
            intac_tarihi=intac_tarihi,
            ggb_tarihi=ggb_tarihi,
            atr_belgesi=file_data,
            kategori=kategori
        )
        db.session.add(beyanname)

        # Log kaydı
        log = Log(
            user_id=current_user.id,
            action="Dosya Yüklendi",
            details=f"{kodu} kodlu dosya yüklendi."
        )
        db.session.add(log)

        db.session.commit()  # Tüm işlemleri aynı transaction içinde kaydet
        return True

    except Exception as e:
        db.session.rollback()  # Hata durumunda işlemi geri al
        return False

def delete_file_service(file_id, current_user):
    try:
        file = BeyannameKayitlari.query.get(file_id)
        if file:
            kodu = file.kodu  # Log için kodu bilgisini sakla
            db.session.delete(file)

            # Log kaydı oluştur
            log = Log(
                user_id=current_user.id,
                action="Dosya Silindi",
                details=f"{kodu} kodlu dosya silindi."
            )
            db.session.add(log)

            db.session.commit()
            return True
        return False  # Dosya bulunamadı

    except Exception as e:
        db.session.rollback()  # Hata durumunda işlemi geri al
        return False

def download_file_service(file_id):
    file = BeyannameKayitlari.query.get(file_id)
    if file:
        return send_file(
            io.BytesIO(file.atr_belgesi),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{file.kodu}.pdf"
        )
    return None  # Dosya bulunamadı
