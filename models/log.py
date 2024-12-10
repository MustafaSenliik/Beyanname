from extensions import db
from datetime import datetime
import pytz

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Istanbul')))

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"<Log {self.action} by User {self.user_id} on {self.timestamp}>"
