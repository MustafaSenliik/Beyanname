from models import BeyannameKayitlari
from datetime import datetime
from flask import make_response
import csv
import io

def search_files_service(args):
    query = BeyannameKayitlari.query

    # Kategori filtresi
    if args.get('kategori'):
        query = query.filter(BeyannameKayitlari.kategori == args['kategori'])
    
    # Kodu filtresi
    if args.get('kodu'):
        query = query.filter(BeyannameKayitlari.kodu == args['kodu'])
    
    # İntaç tarihi filtresi
    if args.get('intac_start_date') and args.get('intac_end_date'):
        try:
            start_date = datetime.strptime(args['intac_start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(args['intac_end_date'], '%Y-%m-%d')
            query = query.filter(BeyannameKayitlari.intac_tarihi.between(start_date, end_date))
        except ValueError:
            print("Geçersiz İntaç tarihi formatı.")
            return []  # Geçersiz tarih formatında boş liste döndür
    
    # GGB tarihi filtresi
    if args.get('ggb_start_date') and args.get('ggb_end_date'):
        try:
            start_date = datetime.strptime(args['ggb_start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(args['ggb_end_date'], '%Y-%m-%d')
            query = query.filter(BeyannameKayitlari.ggb_tarihi.between(start_date, end_date))
        except ValueError:
            print("Geçersiz GGB tarihi formatı.")
            return []  # Geçersiz tarih formatında boş liste döndür

    return query.all()

def download_csv_service():
    # Tüm dosyaları veritabanından al
    files = BeyannameKayitlari.query.all()
    
    csv_data = [
        ['Kodu', 'Ürün Adı', 'Cari Adı', 'Cari Ülkesi', 'Miktar', 'Döviz Cinsi', 'Kur', 'DÖVİZ TUTARI', 'TL TUTARI', 'Gümrük', 'İntaç Tarihi', 'GGB Tarihi', 'Kategori', 'Eklenme Tarihi']
    ]

    for file in files:
        csv_data.append([
            file.kodu, file.urun_adi, file.cari_adi, file.cari_ulkesi,
            file.miktar, file.doviz_cinsi, "{:.4f}".format(file.kur) if file.kur else "Boş",
            file.doviz_tutari, file.tl_tutari, file.gumruk,
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else 'Boş',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else 'Boş',
            file.kategori, file.created_at.strftime('%d.%m.%Y %H:%M:%S')
        ])

    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)
    
    output = make_response('\ufeff' + si.getvalue())  # UTF-8 BOM ile çıktı
    output.headers["Content-Disposition"] = "attachment; filename=tum_dosyalar.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

def download_filtered_csv_service(files):
    if not files:
        print("Filtreleme sonucunda dosya bulunamadı.")
        return None  # Boş sonuç durumunda None döndürülür

    # CSV için başlıklar
    csv_headers = [
        'Kodu', 'Ürün Adı', 'Cari Adı', 'Cari Ülkesi', 'Miktar', 
        'Döviz Cinsi', 'Kur', 'DÖVİZ TUTARI', 'TL TUTARI', 
        'Gümrük', 'İntaç Tarihi', 'GGB Tarihi', 'Kategori', 
        'Eklenme Tarihi'
    ]

    # CSV içeriğini oluştur
    csv_data = [csv_headers]  # Başlıkları ekle

    for file in files:
        csv_data.append([
            file.kodu or 'Boş',
            file.urun_adi or 'Boş',
            file.cari_adi or 'Boş',
            file.cari_ulkesi or 'Boş',
            file.miktar or 0,
            file.doviz_cinsi or 'Boş',
            "{:.4f}".format(file.kur) if file.kur is not None else 'Boş',
            file.doviz_tutari or 0,
            file.tl_tutari or 0,
            file.gumruk or 'Boş',
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else 'Boş',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else 'Boş',
            file.kategori or 'Boş',
            file.created_at.strftime('%d.%m.%Y %H:%M:%S') if file.created_at else 'Boş'
        ])

    # CSV dosyasını hazırlama
    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)

    # CSV dosyasını UTF-8 BOM ile oluştur
    output = make_response('\ufeff' + si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=filtered_dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

