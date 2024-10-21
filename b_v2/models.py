from extensions import db
from datetime import datetime

class BeyannameKayitlari(db.Model):
    __tablename__ = 'beyanname_kayitlari'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kodu = db.Column(db.String(50), nullable=False)
    urun_adi = db.Column(db.String(50), nullable=False)
    cari_adi = db.Column(db.String(255), nullable=False)
    cari_ulkesi = db.Column(db.String(100))
    miktar = db.Column(db.Numeric(10, 2))
    doviz_cinsi = db.Column(db.String(10))
    kur = db.Column(db.Numeric(10, 4))
    doviz_tutari = db.Column(db.Numeric(15, 2))
    tl_tutari = db.Column(db.Numeric(15, 2))
    gumruk = db.Column(db.String(255))
    intac_tarihi = db.Column(db.Date)
    ggb_tarihi = db.Column(db.Date)
    atr_belgesi = db.Column(db.LargeBinary)  # ATR belgesi binary formatında
    kategori = db.Column(db.String(50))  # Kategori sütunu ekleniyor

    def __init__(self, kodu, urun_adi, cari_adi, cari_ulkesi, miktar, doviz_cinsi, kur, doviz_tutari, tl_tutari, gumruk,
                 intac_tarihi, ggb_tarihi, atr_belgesi, kategori):
        self.kodu = kodu
        self.urun_adi = urun_adi
        self.cari_adi = cari_adi
        self.cari_ulkesi = cari_ulkesi
        self.miktar = miktar
        self.doviz_cinsi = doviz_cinsi
        self.kur = kur
        self.doviz_tutari = doviz_tutari
        self.tl_tutari = tl_tutari
        self.gumruk = gumruk
        self.intac_tarihi = intac_tarihi
        self.ggb_tarihi = ggb_tarihi
        self.atr_belgesi = atr_belgesi
        self.kategori = kategori  # kategori buraya ekleniyor


    def __repr__(self):
        return f"<BeyannameKayitlari {self.kodu} - {self.urun_adi}>"
