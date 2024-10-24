from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Kullanıcı bilgilerini saklamak için basit bir örnek (gerçek bir veritabanı kullanmalısınız)
users = {
    'admin': generate_password_hash('adminpass')
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        
        if user and check_password_hash(user, password):
            session['username'] = username  # Kullanıcı adını session'a kaydet
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('home'))  # Başka bir sayfaya yönlendir
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Kullanıcı kaydetme işlemi
        if username in users:
            flash('Bu kullanıcı adı zaten alınmış.', 'danger')
        else:
            users[username] = generate_password_hash(password)  # Yeni kullanıcıyı kaydet
            flash('Kayıt başarılı!', 'success')
            return redirect(url_for('auth.login'))  # Giriş sayfasına yönlendir

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)  # Kullanıcıyı çıkış yaptır
    flash('Çıkış başarılı!', 'success')
    return redirect(url_for('auth.login'))  # Login sayfasına yönlendir
