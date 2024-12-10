from flask import Flask, redirect, url_for, render_template, Response
from flask_jwt_extended import JWTManager
from extensions import db
from flask_login import LoginManager, current_user
from models import User
import os
import requests
from datetime import timedelta
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Controller Blueprint'lerini yükleyin
from controllers.auth_controller import auth_bp
from controllers.file_controller import file_bp
from controllers.search_controller import search_bp
from controllers.log_controller import log_bp
from controllers.admin_controller import admin_blueprint
# Uygulamayı başlatma
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

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

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# HTML tablosu için yeni endpoint
@app.route('/metrics_html')
def show_metrics():
    # /metrics endpoint'inden ham metrik verisini çekin
    metrics_response = requests.get("http://localhost:5000/metrics").text
    metrics_data = parse_metrics(metrics_response)
    return render_template('metrics.html', metrics_data=metrics_data)

def parse_metrics(metrics_text):
    # Metrik verisini satır satır ayrıştırma
    metrics = []
    for line in metrics_text.splitlines():
        # "HELP" ve "TYPE" gibi açıklama satırlarını atla
        if line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) > 1:
            metrics.append({"name": parts[0], "value": parts[1]})
    return metrics

# Kullanıcı yükleme fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Blueprintleri kaydet
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_bp, url_prefix='/file')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(log_bp, url_prefix='/logs')  # Log işlemleri için blueprint
app.register_blueprint(admin_blueprint)

# Veritabanını başlatma
with app.app_context():
    db.create_all()

# Uygulama bağlamı sonlandığında veritabanı bağlantısını kapatma
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

# Uygulamayı çalıştırma
if __name__ == '__main__':
    app.run(debug=True)