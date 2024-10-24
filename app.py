from flask import Flask, redirect, url_for, render_template, session  # Gerekli içe aktarımlar
from extensions import db
from flask_login import LoginManager, login_required  # login_required içe aktarıldı
from controllers.auth_controller import login, logout, auth_bp, register  # register'ı içe aktar
from controllers.file_controller import upload_file, delete_file, download_file, download_csv
from models import User  # User modelini içe aktar

# Flask uygulaması oluştur
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'supersecretkey'  # Güvenlik için gizli anahtar

# Veritabanı ve login manager uzantılarını başlat
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Giriş yapılmamışsa yönlendirilecek sayfa

app.register_blueprint(auth_bp)  # Blueprint'i kaydedin

# Kullanıcı yükleme fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Uygulama rotaları
@app.route('/')
def index():
    return redirect(url_for('auth.login'))  # Giriş sayfasına yönlendirme

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=session['username'])

# URL rotalarını ekle
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/upload', 'upload_file', upload_file, methods=['GET', 'POST'])  # Hem GET hem de POST ekleyin
app.add_url_rule('/delete/<int:file_id>', 'delete_file', delete_file, methods=['GET', 'POST'])
app.add_url_rule('/download/<int:file_id>', 'download_file', download_file)
app.add_url_rule('/download_csv', 'download_csv', download_csv, methods=['GET'])  # GET metodunu ekleyin

# Arama sayfası rotası
@app.route('/search_page')
@login_required
def search_page():
    return render_template('index.html')  # Arama sonuçlarını gösterecek şablon

# Uygulamayı çalıştır
if __name__ == '__main__':
    app.run(debug=True)  # debug=True geliştirici modu için
