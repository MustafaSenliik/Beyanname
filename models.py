from extensions import db
from datetime import datetime

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Dosya verisi BLOB olarak saklanacak

    def __init__(self, filename, category, file_data):
        self.filename = filename
        self.category = category
        self.file_data = file_data
