from models import User
from extensions import db
from flask import flash
from werkzeug.security import generate_password_hash

def register_user(name, email, password, role):
    # Patron sayısını kontrol et
    if role == 'patron':
        patron_count = User.query.filter_by(role='patron').count()
        if patron_count >= 3:
            flash('Zaten 3 patron kayıtlı. Başka patron kaydı yapılamaz.', 'danger')
            return False

    # Kullanıcının zaten var olup olmadığını kontrol et
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Bu email zaten kayıtlı!', 'danger')
        return False

    # Yeni kullanıcı kaydı
    new_user = User(name=name, email=email, role=role)
    new_user.password = generate_password_hash(password)
    db.session.add(new_user)
    db.session.commit()
    return True

def validate_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
