from flask import Flask, request, redirect, url_for, render_template, flash, send_file, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from extensions import db
from models import BeyannameKayitlari, User, Log
import io
from datetime import datetime
import csv
import pytz
from pytz import timezone

app = Flask(__name__)

# Config dosyasını yükle
app.config.from_pyfile('config.py')
app.secret_key = 'supersecretkey'  # Güvenlik anahtarı

# Uzantıları başlat
db.init_app(app)

# Flask LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Kullanıcı yükleme fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Dosya türü kontrol fonksiyonu
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@app.route('/')
def index():
    if current_user.is_authenticated:  # Eğer kullanıcı giriş yapmışsa
        return redirect(url_for('upload_file'))  # Dosya yükleme sayfasına yönlendirme
    return redirect(url_for('login'))  # Giriş sayfasına yönlendirme

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ad_soyad = request.form.get('name')
        email = request.form.get('email')
        sifre = request.form.get('password')
        sifre_tekrar = request.form.get('password_confirm')
        rol = request.form.get('rol')

        # Şifre kontrolü
        if sifre != sifre_tekrar:
            flash('Şifreler uyuşmuyor!', 'danger')
            return redirect(url_for('register'))

        # Patron kayıt sınırını kontrol et
        if rol == 'patron':
            patron_sayisi = User.query.filter_by(rol='patron').count()
            if patron_sayisi >= 3:
                flash('Zaten 3 patron kayıtlı. Başka patron kaydı yapılamaz.', 'danger')
                return redirect(url_for('register'))

        # Kullanıcının zaten var olup olmadığını kontrol et
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Bu email zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))

        # Yeni kullanıcıyı kaydet
        new_user = User(ad_soyad=ad_soyad, email=email, rol=rol)
        new_user.set_password(sifre)  # Şifreyi hashleyip sakla
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarıyla tamamlandı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



# Kullanıcı giriş rotası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        sifre = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(sifre):
            login_user(user)
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('Geçersiz giriş bilgileri!', 'danger')

    return render_template('login.html')

# Kullanıcı çıkış rotası
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('login'))

# Dosya yükleme rotası
@app.route('/upload', methods=['GET', 'POST'])
@login_required
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
        kategori = request.form.get('kategori')

        # Zorunlu alanlar kontrolü
        if not kodu or not urun_adi or not cari_adi or not atr_belgesi or not kategori:
            flash('Lütfen tüm zorunlu alanları doldurun.', 'danger')
            return redirect(request.url)

        # Dosya tipi kontrolü
        if not allowed_file(atr_belgesi.filename):
            flash('Lütfen geçerli bir dosya seçin.', 'danger')
            return redirect(request.url)

        # 'kodu' daha önce var mı kontrol et
        existing_record = BeyannameKayitlari.query.filter_by(kodu=kodu).first()
        if existing_record:
            flash(f"{kodu} kodlu bir dosya zaten mevcut. Lütfen başka bir kod deneyin.", 'danger')
            return redirect(request.url)

        # Dosya verisini okuma
        file_data = atr_belgesi.read()

        # Veritabanına yeni kayıt ekleme
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

        # Başarı mesajı ve yönlendirme
        flash('Dosya başarıyla yüklendi.', 'success')
        return redirect(request.url)

    return render_template('upload.html')



# Dosya silme rotası
@app.route('/delete/<int:file_id>', methods=['GET', 'POST'])
@login_required
def delete_file(file_id):
    if current_user.rol not in ['admin', 'manager', 'assistant_manager']:
        flash('Dosya silme yetkiniz yok.', 'danger')
        return redirect(url_for('search_page'))

    file = BeyannameKayitlari.query.get(file_id)
    if file:
        kodu = file.kodu  # Burada file nesnesinden kodu bilgisini alıyoruz
        db.session.delete(file)
        db.session.commit()

        # Log kaydı oluşturma
        log = Log(user_id=current_user.id, action="Dosya Silindi", details=f"{kodu} kodlu dosya silindi. Kullanıcı: {current_user.ad_soyad}")
        db.session.add(log)
        db.session.commit()

        flash('Dosya başarıyla silindi.', 'success')
    else:
        flash('Dosya bulunamadı.', 'danger')

    return redirect(url_for('search_page'))




# Dosya indirme rotası
@app.route('/download/<int:file_id>')
@login_required
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

# Arama sayfası rotası
@app.route('/search_page')
@login_required
def search_page():
    return render_template('index.html')

# Arama işlemi rotası
@app.route('/search', methods=['GET'])
@login_required
def search():
    kategori = request.args.get('kategori')
    kodu = request.args.get('kodu')
    intac_start_date = request.args.get('intac_start_date')
    intac_end_date = request.args.get('intac_end_date')
    ggb_start_date = request.args.get('ggb_start_date')
    ggb_end_date = request.args.get('ggb_end_date')

    query = BeyannameKayitlari.query

    if kategori:
        query = query.filter_by(kategori=kategori)

    if kodu:
        query = query.filter_by(kodu=kodu)

    if intac_start_date and intac_end_date:
        try:
            intac_start_date = datetime.strptime(intac_start_date, '%Y-%m-%d')
            intac_end_date = datetime.strptime(intac_end_date, '%Y-%m-%d')
            query = query.filter(BeyannameKayitlari.intac_tarihi.between(intac_start_date, intac_end_date))
        except ValueError:
            flash('Geçersiz İntaç tarih formatı.')
            return redirect(url_for('search_page'))

    if ggb_start_date and ggb_end_date:
        try:
            ggb_start_date = datetime.strptime(ggb_start_date, '%Y-%m-%d')
            ggb_end_date = datetime.strptime(ggb_end_date, '%Y-%m-%d')
            query = query.filter(BeyannameKayitlari.ggb_tarihi.between(ggb_start_date, ggb_end_date))
        except ValueError:
            flash('Geçersiz GGB tarih formatı.')
            return redirect(url_for('search_page'))

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
            file.created_at.strftime('%d.%m.%Y %H:%M:%S') if file.created_at else 'Boş'
        ) for file in query_result
    ]

    return render_template('index.html', results=results)

# Tüm dosyaları CSV olarak indirme rotası
@app.route('/download_csv')
@login_required
def download_csv():
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
            created_at_turkey
        ])

    # CSV dosyasını UTF-8 BOM ile oluştur
    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)

    output = make_response('\ufeff' + si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

# Filtrelenmiş dosyaları CSV olarak indirme rotası
@app.route('/download_filtered_csv')
@login_required
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
            created_at_turkey
        ])

    # CSV dosyasını UTF-8 BOM ile oluştur
    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)

    output = make_response('\ufeff' + si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=filtered_dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

if __name__ == '__main__':
    app.run(debug=True)

