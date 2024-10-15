from extensions import db
from datetime import datetime

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Dosya verisi BLOB olarak saklanacak

    # Yeni eklenen alanlar
    declaration_number = db.Column(db.String(50), nullable=False)  # Beyanname numarası
    customs_office_name = db.Column(db.String(100), nullable=False)  # Gümrük adı
    registration_date = db.Column(db.Date, nullable=False)  # Tescil tarihi

    def __init__(self, filename, category, file_data, declaration_number, customs_office_name, registration_date):
        self.filename = filename
        self.category = category
        self.file_data = file_data
        self.declaration_number = declaration_number
        self.customs_office_name = customs_office_name
        self.registration_date = registration_date
