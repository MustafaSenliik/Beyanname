from models import Log
from flask_login import current_user
from datetime import datetime

def log_action(action, details):
    log = Log(
        user_id=current_user.id,
        action=action,
        details=details,
        timestamp=datetime.now()
    )
    return log
