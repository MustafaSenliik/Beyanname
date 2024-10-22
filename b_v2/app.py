from flask import Flask, request, redirect, url_for, render_template, flash, send_file, make_response
from extensions import db
from models import BeyannameKayitlari  # Updated to match the new model name
import io
from datetime import datetime
import csv
import pytz  # Zaman dilimi ayarları için pytz kütüphanesini ekleyin.
from pytz import timezone  # timezone fonksiyonunu içe aktarın.


app = Flask(__name__)

# Config dosyasını yükle
app.config.from_pyfile('config.py')

# Uzantıları başlat
db.init_app(app)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Dosya türü kontrol fonksiyonu
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

# Ana sayfayı upload sayfasına yönlendir
@app.route('/')
def index():
    return redirect(url_for('upload_file'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Form alanlarından verileri alıyoruz
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
        atr_belgesi = request.files.get('pdf_dosyasi')
        kategori = request.form.get('kategori')  # Kategori formdan alınıyor

        # Alanların boş olup olmadığını kontrol ediyoruz
        if not kodu or not urun_adi or not cari_adi or not atr_belgesi or not kategori:
            flash('Lütfen tüm zorunlu alanları doldurun.')
            return redirect(request.url)

        if not allowed_file(atr_belgesi.filename):
            flash('Lütfen geçerli bir dosya seçin.')
            return redirect(request.url)

        # Dosya verisini okuma
        file_data = atr_belgesi.read()  # Dosyayı binary formatta okuma

        # Veritabanına kaydetme
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
            kategori=kategori,
            
        )
        db.session.add(beyanname)
        db.session.commit()

        flash('Dosya başarıyla yüklendi.')
        return redirect(request.url)

    return render_template('upload.html')

@app.route('/delete/<int:file_id>', methods=['GET', 'POST'])
def delete_file(file_id):
    file = BeyannameKayitlari.query.get(file_id)
    if file:
        db.session.delete(file)
        db.session.commit()
        flash('Dosya başarıyla silindi.')
    else:
        flash('Dosya bulunamadı.')
    return redirect(url_for('search_page'))


@app.route('/download/<int:file_id>')
def download_file(file_id):
    file = BeyannameKayitlari.query.get(file_id)
    if file:
        return send_file(
            io.BytesIO(file.atr_belgesi),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{file.kodu}.pdf"
        )
    flash('Dosya bulunamadı.')
    return redirect(url_for('search_page'))


@app.route('/search_page')
def search_page():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    kategori = request.args.get('kategori')
    kodu = request.args.get('kodu')
    intac_start_date = request.args.get('intac_start_date')
    intac_end_date = request.args.get('intac_end_date')
    ggb_start_date = request.args.get('ggb_start_date')
    ggb_end_date = request.args.get('ggb_end_date')

    # Sorgu oluştur
    query = BeyannameKayitlari.query

    # Kategoriye göre arama
    if kategori:
        query = query.filter_by(kategori=kategori)

    # Koduya göre arama
    if kodu:
        query = query.filter_by(kodu=kodu)

    # İntaç tarihi aralığına göre arama
    if intac_start_date and intac_end_date:
        try:
            intac_start_date = datetime.strptime(intac_start_date, '%Y-%m-%d')
            intac_end_date = datetime.strptime(intac_end_date, '%Y-%m-%d')
            query = query.filter(BeyannameKayitlari.intac_tarihi.between(intac_start_date, intac_end_date))
        except ValueError:
            flash('Geçersiz İntaç tarih formatı.')
            return redirect(url_for('search_page'))

    # GGB tarihi aralığına göre arama
    if ggb_start_date and ggb_end_date:
        try:
            ggb_start_date = datetime.strptime(ggb_start_date, '%Y-%m-%d')
            ggb_end_date = datetime.strptime(ggb_end_date, '%Y-%m-%d')
            query = query.filter(BeyannameKayitlari.ggb_tarihi.between(ggb_start_date, ggb_end_date))
        except ValueError:
            flash('Geçersiz GGB tarih formatı.')
            return redirect(url_for('search_page'))

    # Sonuçları al
    query_result = query.all()

    results = [
        (
            file.id,
            file.kodu,
            file.urun_adi,
            file.cari_adi,
            file.cari_ulkesi,
            file.miktar,
            file.doviz_cinsi,
            file.kur,
            file.doviz_tutari,
            file.tl_tutari,
            file.gumruk,
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else 'Boş',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else 'Boş',
            file.kategori,
            file.created_at.strftime('%d.%m.%Y %H:%M:%S') if file.created_at else 'Boş'  # Eklenme tarihi
        ) for file in query_result
    ]

    return render_template('index.html', results=results)

@app.route('/download_csv')
def download_csv():
    # Veritabanındaki tüm dosya bilgilerini al
    files = BeyannameKayitlari.query.all()

    # CSV dosyası hazırlama
    csv_data = []
    csv_data.append([
        'Kodu', 'Ürün Adı', 'Cari Adı', 'Cari Ülkesi', 'Miktar', 'Döviz Cinsi', 'Kur',
        'DÖVİZ TUTARI', 'TL TUTARI', 'Gümrük', 'İntaç Tarihi', 'GGB Tarihi', 'Kategori', 'Eklenme Tarihi'
    ])

    # Türkiye saat dilimi
    turkey_tz = timezone('Europe/Istanbul')

    for file in files:
        created_at_turkey = file.created_at.astimezone(turkey_tz).strftime('%d.%m.%Y %H:%M:%S') if file.created_at else 'Boş'
        csv_data.append([
            file.kodu if file.kodu else 'Boş',
            file.urun_adi if file.urun_adi else 'Boş',
            file.cari_adi if file.cari_adi else 'Boş',
            file.cari_ulkesi if file.cari_ulkesi else 'Boş',
            file.miktar if file.miktar else 'Boş',
            file.doviz_cinsi if file.doviz_cinsi else 'Boş',
            file.kur if file.kur else 'Boş',
            file.doviz_tutari if file.doviz_tutari else 'Boş',
            file.tl_tutari if file.tl_tutari else 'Boş',
            file.gumruk if file.gumruk else 'Boş',
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else 'Boş',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else 'Boş',
            file.kategori if file.kategori else 'Boş',
            created_at_turkey  # Türkiye saat dilimine göre eklenme tarihi
        ])

    # CSV dosyasını UTF-8 BOM ile oluştur
    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)
    
    output = make_response('\ufeff' + si.getvalue())  # UTF-8 BOM eklenmesi
    output.headers["Content-Disposition"] = "attachment; filename=dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

@app.route('/download_filtered_csv')
def download_filtered_csv():
    kategori = request.args.get('kategori')
    kodu = request.args.get('kodu')
    intac_start_date = request.args.get('intac_start_date')
    intac_end_date = request.args.get('intac_end_date')
    ggb_start_date = request.args.get('ggb_start_date')
    ggb_end_date = request.args.get('ggb_end_date')

    # Sorgu oluştur
    query = BeyannameKayitlari.query

    if kategori:
        query = query.filter_by(kategori=kategori)

    if kodu:
        query = query.filter_by(kodu=kodu)

    if intac_start_date and intac_end_date:
        intac_start_date = datetime.strptime(intac_start_date, '%Y-%m-%d')
        intac_end_date = datetime.strptime(intac_end_date, '%Y-%m-%d')
        query = query.filter(BeyannameKayitlari.intac_tarihi.between(intac_start_date, intac_end_date))

    if ggb_start_date and ggb_end_date:
        ggb_start_date = datetime.strptime(ggb_start_date, '%Y-%m-%d')
        ggb_end_date = datetime.strptime(ggb_end_date, '%Y-%m-%d')
        query = query.filter(BeyannameKayitlari.ggb_tarihi.between(ggb_start_date, ggb_end_date))

    files = query.all()

    # Türkiye saat dilimi
    turkey_tz = timezone('Europe/Istanbul')

    # CSV dosyası hazırlama
    csv_data = []
    csv_data.append([
        'Kodu', 'Ürün Adı', 'Cari Adı', 'Cari Ülkesi', 'Miktar', 'Döviz Cinsi', 'Kur',
        'DÖVİZ TUTARI', 'TL TUTARI', 'Gümrük', 'İntaç Tarihi', 'GGB Tarihi', 'Kategori', 'Eklenme Tarihi'
    ])

    for file in files:
        created_at_turkey = file.created_at.astimezone(turkey_tz).strftime('%d.%m.%Y %H:%M:%S') if file.created_at else 'Boş'
        csv_data.append([
            file.kodu if file.kodu else 'Boş',
            file.urun_adi if file.urun_adi else 'Boş',
            file.cari_adi if file.cari_adi else 'Boş',
            file.cari_ulkesi if file.cari_ulkesi else 'Boş',
            file.miktar if file.miktar else 'Boş',
            file.doviz_cinsi if file.doviz_cinsi else 'Boş',
            file.kur if file.kur else 'Boş',
            file.doviz_tutari if file.doviz_tutari else 'Boş',
            file.tl_tutari if file.tl_tutari else 'Boş',
            file.gumruk if file.gumruk else 'Boş',
            file.intac_tarihi.strftime('%d.%m.%Y') if file.intac_tarihi else 'Boş',
            file.ggb_tarihi.strftime('%d.%m.%Y') if file.ggb_tarihi else 'Boş',
            file.kategori if file.kategori else 'Boş',
            created_at_turkey  # Türkiye saat dilimine göre eklenme tarihi
        ])

    # CSV dosyasını UTF-8 BOM ile oluştur
    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)
    
    output = make_response('\ufeff' + si.getvalue())  # UTF-8 BOM eklenmesi
    output.headers["Content-Disposition"] = "attachment; filename=filtered_dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output
if __name__ == '__main__':
    app.run(debug=True)

