from models import Log
from extensions import db
from datetime import datetime

def create_log(user_id, action, details):
    log = Log(user_id=user_id, action=action, details=details, timestamp=datetime.now())
    db.session.add(log)
    db.session.commit()

def get_logs_by_user(user_id):
    return Log.query.filter_by(user_id=user_id).all()

def get_all_logs():
    return Log.query.all()

from models import Log
from flask_login import current_user

def fetch_logs_by_role():
    """
    Kullanıcının rolüne göre logları döndürür. 
    Patron, Müdür ve Müdür Yardımcısı rolleri tüm logları görebilir.
    Diğer roller yalnızca kendi loglarını görebilir.
    """
    if current_user.rol in ['patron', 'müdür', 'müdür_yardımcısı']:
        # Tüm logları getir
        return Log.query.all()
    else:
        # Sadece kullanıcının kendi loglarını getir
        return Log.query.filter_by(user_id=current_user.id).all()
