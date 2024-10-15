from flask import Flask, request, redirect, url_for, render_template, flash, send_file
from extensions import db
from models import UploadedFile
import io

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

        if not category:
            flash('Kategori seçimi zorunludur.')
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
            file_data=file_data
        )
        db.session.add(uploaded_file)
        db.session.commit()

        flash('Dosya başarıyla yüklendi.')
        return redirect(request.url)

    return render_template('upload.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    category = request.args.get('category')
    results = []

    # Kullanıcıdan gelen dosya adı sorgusuna .pdf ekleyelim
    if query:
        query = query.strip() + '.pdf'

    # Veritabanında kategori ve dosya adına göre arama yap
    if category and query:  # Hem kategori hem de dosya adı girilmişse
        query_result = UploadedFile.query.filter(
            (UploadedFile.category == category) &
            (UploadedFile.filename == query)  # Dosya adı tam eşleşme
        ).all()
    elif category:  # Sadece kategori seçilmişse
        query_result = UploadedFile.query.filter_by(category=category).all()
    elif query:  # Sadece dosya adı girilmişse
        query_result = UploadedFile.query.filter_by(filename=query).all()  # Dosya adı tam eşleşme
    else:
        flash('Lütfen bir kategori seçin veya dosya adı girin.')
        return redirect(url_for('index'))

    # Arama sonuçlarını listele
    if query_result:
        results = [(file.id, file.filename) for file in query_result]

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

if __name__ == '__main__':
    app.run(debug=True)
