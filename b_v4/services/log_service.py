from models import Log
from extensions import db
from datetime import datetime
from flask_login import current_user

def create_log(user_id, action, details):
    try:
        log = Log(user_id=user_id, action=action, details=details, timestamp=datetime.utcnow())
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Hata durumunda rollback
        print(f"Log kaydedilirken hata oluştu: {e}")

def get_logs_by_user(user_id):
    try:
        return Log.query.filter_by(user_id=user_id).all()
    except Exception as e:
        print(f"Kullanıcı logları alınırken hata oluştu: {e}")
        return []

def get_all_logs():
    try:
        return Log.query.all()
    except Exception as e:
        print(f"Tüm loglar alınırken hata oluştu: {e}")
        return []

def fetch_logs_by_role():
    """
    Kullanıcının rolüne göre logları döndürür. 
    Patron, Müdür ve Müdür Yardımcısı rolleri tüm logları görebilir.
    Diğer roller yalnızca kendi loglarını görebilir.
    """
    if current_user.is_authenticated:  # Kullanıcı oturum kontrolü
        try:
            if current_user.rol in ['patron', 'müdür', 'müdür_yardımcısı']:
                # Tüm logları getir
                return Log.query.all()
            else:
                # Sadece kullanıcının kendi loglarını getir
                return Log.query.filter_by(user_id=current_user.id).all()
        except Exception as e:
            print(f"Loglar alınırken hata oluştu: {e}")
            return []
    else:
        return []  # Kullanıcı giriş yapmamışsa boş liste döndür
