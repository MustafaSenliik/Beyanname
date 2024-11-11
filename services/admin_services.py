from models import User, Log, BeyannameKayitlari  
from werkzeug.security import generate_password_hash
from app import db
from datetime import datetime, timedelta
import pytz
from sqlalchemy import func, and_, extract


def get_file_upload_count():
    return db.session.query(func.count(BeyannameKayitlari.id)).scalar()

def get_recent_uploads(limit=5):

    return BeyannameKayitlari.query.order_by(BeyannameKayitlari.created_at.desc()).limit(limit).all()

# Yalnızca aktif (is_deleted=False) kullanıcıları getiren fonksiyon
def get_all_users():
    """Veritabanından yalnızca aktif kullanıcıları getirir."""
    return User.query.filter_by(is_deleted=False).all()


# Tüm log kayıtlarını getiren fonksiyon
def get_all_logs():
    """Veritabanından tüm log kayıtlarını getirir ve zamana göre sıralar."""
    return Log.query.order_by(Log.timestamp.desc()).all()


def get_logs_filtered(start_date=None, end_date=None, user_name=None):
    """Tarih aralığı veya kullanıcı adına göre log kayıtlarını filtreler."""
    query = db.session.query(Log)
    
    # Kullanıcı adına göre filtrele
    if user_name:
        user = User.query.filter_by(ad_soyad=user_name).first()
        if user:
            query = query.filter(Log.user_id == user.id)
        else:
            return []  # Kullanıcı bulunamazsa boş liste döndür
    
    # Saat dilimini Europe/Istanbul olarak ayarla
    timezone = pytz.timezone('Europe/Istanbul')
    
    # Tarih aralığına göre filtrele
    if isinstance(start_date, str) and start_date:
        start_date = timezone.localize(datetime.strptime(start_date, "%Y-%m-%d"))
    if isinstance(end_date, str) and end_date:
        end_date = timezone.localize(datetime.strptime(end_date, "%Y-%m-%d"))

    if start_date and end_date:
        query = query.filter(and_(Log.timestamp >= start_date, Log.timestamp <= end_date))
    elif start_date:
        query = query.filter(Log.timestamp >= start_date)
    elif end_date:
        query = query.filter(Log.timestamp <= end_date)

    return query.order_by(Log.timestamp.desc()).all()


    
# Toplam kullanıcı sayısını döndürür
def get_users_count():
    """Toplam kullanıcı sayısını döndürür."""
    return User.query.filter_by(is_deleted=False).count()

# Toplam log kaydı sayısını döndürür
def get_logs_count():
    """Toplam log kaydı sayısını döndürür."""
    return Log.query.count()

# Yeni kullanıcı ekleme fonksiyonu (şifreyi düz metin olarak kaydetmek için güncellendi)
def add_user(ad_soyad, email, password, rol):
    """Yeni bir kullanıcı ekler. Şifreyi hashlemeden kaydeder."""
    new_user = User(ad_soyad=ad_soyad, email=email, sifre=password, rol=rol)  # Şifreyi hashlemeden kaydeder
    db.session.add(new_user)
    db.session.commit()

# Kullanıcı silme fonksiyonu
def delete_user(user_id):
    """Belirtilen kullanıcıyı veritabanından siler."""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

# Kullanıcı rolünü güncelleme fonksiyonu
def update_user_rol(user_id, new_rol):
    """Belirtilen kullanıcının rolünü günceller."""
    user = User.query.filter_by(id=user_id, is_deleted=False).first()
    if user:
        user.rol = new_rol
        db.session.commit()

def get_weekly_upload_count():
    one_week_ago = datetime.now() - timedelta(days=7)
    weekly_data = (
        db.session.query(BeyannameKayitlari.kategori, func.count(BeyannameKayitlari.id))
        .filter(BeyannameKayitlari.created_at >= one_week_ago)
        .group_by(BeyannameKayitlari.kategori)
        .all()
    )
    return dict(weekly_data)

# Son bir ay içinde yüklenen dosya sayısını döndüren fonksiyon
def get_monthly_upload_count():
    one_month_ago = datetime.now() - timedelta(days=30)
    monthly_data = (
        db.session.query(BeyannameKayitlari.kategori, func.count(BeyannameKayitlari.id))
        .filter(BeyannameKayitlari.created_at >= one_month_ago)
        .group_by(BeyannameKayitlari.kategori)
        .all()
    )
    return dict(monthly_data)

def get_yearly_currency_data():
    current_year = datetime.now().year
    yearly_data = (
        db.session.query(
            BeyannameKayitlari.doviz_cinsi,
            func.sum(BeyannameKayitlari.doviz_tutari).label('total_doviz'),
            func.sum(BeyannameKayitlari.tl_tutari).label('total_tl')
        )
        .filter(extract('year', BeyannameKayitlari.created_at) == current_year)
        .group_by(BeyannameKayitlari.doviz_cinsi)
        .all()
    )
    # Veriyi dictionary formatına dönüştürme
    return {item.doviz_cinsi: {'doviz': item.total_doviz, 'tl': item.total_tl} for item in yearly_data}


# Aylık döviz verisini döndüren fonksiyon
def get_monthly_currency_data():
    current_year = datetime.now().year
    current_month = datetime.now().month
    monthly_data = (
        db.session.query(
            BeyannameKayitlari.doviz_cinsi,
            func.sum(BeyannameKayitlari.doviz_tutari).label('total_doviz'),
            func.sum(BeyannameKayitlari.tl_tutari).label('total_tl')
        )
        .filter(extract('year', BeyannameKayitlari.created_at) == current_year)
        .filter(extract('month', BeyannameKayitlari.created_at) == current_month)
        .group_by(BeyannameKayitlari.doviz_cinsi)
        .all()
    )
    # Veriyi dictionary formatına dönüştürme
    return {item.doviz_cinsi: {'doviz': item.total_doviz, 'tl': item.total_tl} for item in monthly_data}