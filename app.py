from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from extensions import db
from flask_login import LoginManager, current_user
from models import User
import os

# Controller Blueprint'lerini yükleyin
from controllers.auth_controller import auth_bp
from controllers.file_controller import file_bp
from controllers.search_controller import search_bp
from controllers.log_controller import log_bp

# Uygulamayı başlatma
app = Flask(__name__)
app.config.from_pyfile('config.py')

# JWT ayarlarını yapın
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')  # JWT için gizli anahtar
jwt = JWTManager(app)

# Uzantıları başlat
db.init_app(app)

# Flask-Login yapılandırması
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Giriş yapma sayfası

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('file.upload_file'))
    return redirect(url_for('auth.login'))

# Kullanıcı yükleme fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Blueprintleri kaydet
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_bp, url_prefix='/file')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(log_bp, url_prefix='/logs')  # Log işlemleri için blueprint

# Veritabanını başlatma
with app.app_context():
    db.create_all()

# Uygulama bağlamı sonlandığında veritabanı bağlantısını kapatma
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# Uygulamayı çalıştırma
if __name__ == '__main__':
    app.run(debug=True)