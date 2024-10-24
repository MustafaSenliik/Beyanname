from models import BeyannameKayitlari
from datetime import datetime

def upload_file_service(kodu, urun_adi, cari_adi, atr_belgesi, **form_data):
    cari_ulkesi = form_data.get('cari_ulkesi')
    miktar = form_data.get('miktar')
    doviz_cinsi = form_data.get('doviz_cinsi')
    kur = form_data.get('kur')
    doviz_tutari = form_data.get('doviz_tutari')
    tl_tutari = form_data.get('tl_tutari')
    gumruk = form_data.get('gumruk')
    intac_tarihi = form_data.get('intac_tarihi')
    ggb_tarihi = form_data.get('ggb_tarihi')
    kategori = form_data.get('kategori')

    existing_record = BeyannameKayitlari.query.filter_by(kodu=kodu).first()
    if existing_record:
        return None  # Mevcut kayıt hatası

    # Veritabanına yeni kayıt ekleme
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
        intac_tarihi=datetime.strptime(intac_tarihi, '%Y-%m-%d') if intac_tarihi else None,
        ggb_tarihi=datetime.strptime(ggb_tarihi, '%Y-%m-%d') if ggb_tarihi else None,
        atr_belgesi=file_data,
        kategori=kategori
    )
    return beyanname

def delete_file_service(file, kodu):
    if file:
        return True
    return False

def download_file_service(file):
    file_data = io.BytesIO(file.atr_belgesi)
    file_name = f"{file.kodu}.pdf"
    return file_data, file_name

def prepare_csv(files):
    csv_data = []
    csv_data.append([
        'Kodu', 'Ürün Adı', 'Cari Adı', 'Cari Ülkesi', 'Miktar', 'Döviz Cinsi', 'Kur',
        'DÖVİZ TUTARI', 'TL TUTARI', 'Gümrük', 'İntaç Tarihi', 'GGB Tarihi', 'Kategori', 'Eklenme Tarihi'
    ])
    for file in files:
        csv_data.append([
            file.kodu, file.urun_adi, file.cari_adi, file.cari_ulkesi, file.miktar, file.doviz_cinsi,
            file.kur, file.doviz_tutari, file.tl_tutari, file.gumruk,
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else '',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else '',
            file.kategori, file.created_at.strftime('%d.%m.%Y %H:%M:%S') if file.created_at else ''
        ])
    return csv_data
