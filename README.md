# 📁 Flask ile Geliştirilen Dosya Yönetim Sistemi

Bu proje, kullanıcıların dosya yüklemesi, yönetmesi ve detaylı loglama yapabilmesi için Flask ile geliştirilmiş bir dosya yönetim sistemi sağlar.



## 🚀 Özellikler
- **Kullanıcı Yönetimi**: Kayıt, giriş, şifre belirleme ve değiştirme.
- **Yetkilendirme**: Rol bazlı erişim kontrolü (Çalışan, Müdür Yardımcısı, Müdür, Patron, Admin).
- **Dosya Yükleme ve Yönetimi**: Dosya yükleme, arama ve loglama.
- **Detaylı Loglama**: Kullanıcı aktivitelerinin kaydını tutarak yöneticiye raporlama imkanı sağlar.
- **Yönetici Paneli**: Yönetici rolündeki kullanıcılar için kullanıcı ve log kayıtlarını yönetme arayüzü.

---


## ⚙️ Kurulum

### Gereksinimler
- **Python 3.8+**
- **pip** (Python paket yöneticisi)
- **Git** (Opsiyonel, projeyi klonlamak için)

## Bağımlılıkların Yüklenmesi
Projeyi Klonlayın:
```
git clone https://https://github.com/MustafaSenliik/Beyanname.git
```

## Sanal Ortam Oluşturun ve Etkinleştirin
```
python -m venv venv
```
## Windows için
```
venv\Scripts\activate
```

## Mac/Linux için
```
source venv/bin/activate
```

## Bağımlılıkları Yükleyin:
```
pip install -r requirements.txt
```
## Tabloların Kurulması


- **Projede** kullanacağınız veritabanı tablolarını hazırlayın(mysql)
- **3** ayrı tablo mevcuttur bunlar sırasıyla beyanname_kayitlari, logs ve users olarak veritabanına tablo olarak eklenmeldir.

```
CREATE TABLE beyanname_kayitlari (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kodu VARCHAR(50) NOT NULL,
    urun_adi VARCHAR(50) NOT NULL,
    cari_adi VARCHAR(255) NOT NULL,
    cari_ulkesi VARCHAR(100),
    miktar DECIMAL(10, 2),
    doviz_cinsi VARCHAR(10),
    kur DECIMAL(10, 4),
    doviz_tutari DECIMAL(15, 2),
    tl_tutari DECIMAL(15, 2),
    gumruk VARCHAR(255),
    intac_tarihi DATE,
    ggb_tarihi DATE,
    atr_belgesi LONGBLOB,
    kategori VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
```
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    details VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
```
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad_soyad VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sifre VARCHAR(255) NOT NULL,
    kayit_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP
);
```


Yapılandırma
config.py dosyasında veritabanı bağlantı bilgilerini ve JWT gibi diğer yapılandırma ayarlarını tanımlayın.
```
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gizli_anahtar')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt_gizli_anahtar'
```
## 🧑‍💻 Kullanım
Yönetici Paneli
Kullanıcı Yönetimi: Yeni kullanıcı ekleme, silme ve yetki değiştirme işlemlerini buradan yapabilirsiniz.
Dosya Yönetimi: Dosya yükleme, arama ve silme işlemlerini gerçekleştirebilirsiniz.

## 🛠️ Hata Ayıklama
Sanal Ortam: Sanal ortamın (venv) aktif olduğundan emin olun.

Bağımlılıkların Güncellenmesi: Yeni bir modül eklediyseniz pip freeze > requirements.txt komutuyla requirements.txt dosyanızı güncelleyin.

Veritabanı Problemleri: Veritabanı migrasyonlarını tekrar kontrol edin veya veritabanını sıfırlamak için:

```
flask db downgrade
flask db upgrade
```

Port Sorunları: Proje bir port üzerinde çalışıyorsa başka bir port ile çalıştırmayı deneyin:
```
flask run --port=5001
```
## 🤝 Katkıda Bulunma

Bu projeyi forklayın.
Yeni bir dal (branch) oluşturun: git checkout -b özellik-adi.
Değişikliklerinizi işleyin: git commit -m 'Özellik ekle'.
Dalınıza push edin: git push origin özellik-adi.
Bir Pull Request gönderin.

## 📜 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

