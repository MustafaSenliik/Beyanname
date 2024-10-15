from flask import Flask, request, redirect, url_for, render_template, flash, send_file, make_response
from extensions import db
from models import UploadedFile
import io
from datetime import datetime
import csv

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

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        category = request.form.get('category')
        file = request.files.get('file')

        # Yeni alanlar
        declaration_number = request.form.get('declaration_number')
        customs_office_name = request.form.get('customs_office_name')
        registration_date = request.form.get('registration_date')

        if not category or not declaration_number or not customs_office_name or not registration_date:
            flash('Tüm alanlar doldurulmalıdır.')
            return redirect(request.url)

        if not file or not allowed_file(file.filename):
            flash('Lütfen geçerli bir dosya seçin.')
            return redirect(request.url)

        # Aynı dosya adı ve kategoriye göre veritabanını kontrol et
        existing_file = UploadedFile.query.filter_by(filename=file.filename, category=category).first()
        if existing_file:
            flash(f'Aynı dosya adı ({file.filename}) zaten {category} kategorisinde mevcut.')
            return redirect(request.url)

        # Dosya verisini okuma
        file_data = file.read()  # Dosyayı binary formatta okuma

        # Veritabanına kaydetme
        uploaded_file = UploadedFile(
            filename=file.filename,
            category=category,
            file_data=file_data,
            declaration_number=declaration_number,
            customs_office_name=customs_office_name,
            registration_date=datetime.strptime(registration_date, '%Y-%m-%d')
        )
        db.session.add(uploaded_file)
        db.session.commit()

        flash('Dosya başarıyla yüklendi.')
        return redirect(request.url)

    return render_template('upload.html')


@app.route('/search', methods=['GET'])
def search():
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    declaration_number = request.args.get('declaration_number')

    # Sorgu oluştur
    query = UploadedFile.query

    # Beyanname numarasına göre arama
    if declaration_number:
        query = query.filter_by(declaration_number=declaration_number)

    # Kategoriye göre arama
    if category:
        query = query.filter_by(category=category)

    # Tarih aralığına göre arama
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(UploadedFile.registration_date.between(start_date, end_date))
        except ValueError:
            flash('Geçersiz tarih formatı.')
            return redirect(url_for('index'))

    # Sonuçları al
    query_result = query.all()

    # Arama sonuçlarını listele
    results = [
        (
            file.id,
            file.filename,
            file.declaration_number,
            file.customs_office_name,
            file.registration_date.strftime('%d.%m.%Y') if file.registration_date else 'Boş',
            file.category
        ) for file in query_result
    ]

    return render_template('index.html', results=results, category=category)



# Dosya indirme
@app.route('/download/<int:file_id>')
def download_file(file_id):
    file = UploadedFile.query.get(file_id)
    if file:
        return send_file(
            io.BytesIO(file.file_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=file.filename
        )
    flash('Dosya bulunamadı.')
    return redirect(url_for('index'))

# CSV dosyası indirme
@app.route('/download_csv')
def download_csv():
    # Veritabanındaki tüm dosya bilgilerini al
    files = UploadedFile.query.all()

    # CSV dosyası hazırlama
    csv_data = []
    csv_data.append(['Beyanname Numarası', 'Gümrük Adı', 'Tescil Tarihi', 'Kategori'])

    for file in files:
        csv_data.append([
            file.declaration_number if file.declaration_number else 'Boş',  # Beyanname numarası varsa yaz, yoksa 'Boş'
            file.customs_office_name if file.customs_office_name else 'Boş',  # Gümrük adı varsa yaz, yoksa 'Boş'
            file.registration_date.strftime('%d.%m.%Y') if file.registration_date else 'Boş',  # Tescil tarihi varsa formatla, yoksa 'Boş'
            file.category if file.category else 'Boş'  # Kategori varsa yaz, yoksa 'Boş'
        ])

    # CSV dosyasını UTF-8 BOM ile oluştur
    si = io.StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cw.writerows(csv_data)
    
    output = make_response('\ufeff' + si.getvalue())  # UTF-8 BOM eklenmesi
    output.headers["Content-Disposition"] = "attachment; filename=dosya_listesi.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output



if __name__ == '__main__':
    app.run(debug=True)
