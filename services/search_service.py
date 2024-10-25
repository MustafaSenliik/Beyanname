from models import BeyannameKayitlari
from datetime import datetime
from flask import make_response
import csv
import io

def search_files(args):
    query = BeyannameKayitlari.query

    if args.get('kategori'):
        query = query.filter(BeyannameKayitlari.kategori == args['kategori'])
    if args.get('kodu'):
        query = query.filter(BeyannameKayitlari.kodu == args['kodu'])
    if args.get('intac_start_date') and args.get('intac_end_date'):
        start_date = datetime.strptime(args['intac_start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(args['intac_end_date'], '%Y-%m-%d')
        query = query.filter(BeyannameKayitlari.intac_tarihi.between(start_date, end_date))
    if args.get('ggb_start_date') and args.get('ggb_end_date'):
        start_date = datetime.strptime(args['ggb_start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(args['ggb_end_date'], '%Y-%m-%d')
        query = query.filter(BeyannameKayitlari.ggb_tarihi.between(start_date, end_date))
    
    return query.all()

def download_filtered_csv_service(args):
    files = search_files(args)
    csv_data = [
        ['Kodu', 'Ürün Adı', 'Cari Adı', 'Cari Ülkesi', 'Miktar', 'Döviz Cinsi', 'Kur', 'DÖVİZ TUTARI', 'TL TUTARI', 'Gümrük', 'İntaç Tarihi', 'GGB Tarihi', 'Kategori', 'Eklenme Tarihi']
    ]

    for file in files:
        csv_data.append([
            file.kodu, file.urun_adi, file.cari_adi, file.cari_ulkesi,
            file.miktar, file.doviz_cinsi, "{:.4f}".format(file.kur),
            file.doviz_tutari, file.tl_tutari, file.gumruk,
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else 'Boş',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else 'Boş',
            file.kategori, file.created_at.strftime('%d.%m.%Y %H:%M:%S')
        ])

    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)
    output = make_response('\ufeff' + si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=filtered_dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output
