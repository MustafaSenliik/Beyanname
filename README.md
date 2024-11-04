# 📁 Flask ile Geliştirilen Dosya Yönetim Sistemi

Bu proje, kullanıcıların dosya yüklemesi, yönetmesi ve detaylı loglama yapabilmesi için Flask ile geliştirilmiş bir dosya yönetim sistemi sağlar.

---

## 📜 İçindekiler
- [Özellikler](#özellikler)
- [Ekran Görüntüleri](#ekran-görüntüleri)
- [Kurulum](#kurulum)
  - [Gereksinimler](#gereksinimler)
  - [Bağımlılıkların Yüklenmesi](#bağımlılıkların-yüklenmesi)
  - [Tablo Yapılarının Kurulması](#tablo-yapılarının-kurulması)
  - [Yapılandırma](#yapılandırma)
- [Kullanım](#kullanım)
- [API Endpointleri](#api-endpointleri)
- [Hata Ayıklama](#hata-ayıklama)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

---

## 🚀 Özellikler
- **Kullanıcı Yönetimi**: Kayıt, giriş, şifre belirleme ve değiştirme.
- **Yetkilendirme**: Rol bazlı erişim kontrolü (Çalışan, Müdür Yardımcısı, Müdür, Patron, Admin).
- **Dosya Yükleme ve Yönetimi**: Dosya yükleme, arama ve loglama.
- **Detaylı Loglama**: Kullanıcı aktivitelerinin kaydını tutarak yöneticiye raporlama imkanı sağlar.
- **Yönetici Paneli**: Yönetici rolündeki kullanıcılar için kullanıcı ve log kayıtlarını yönetme arayüzü.

---

## 🖼️ Ekran Görüntüleri
- **Giriş Ekranı**  
  ![Giriş Ekranı](link_to_login_screen_image)

- **Yönetici Paneli**  
  ![Yönetici Paneli](link_to_admin_panel_image)

---

## ⚙️ Kurulum

### Gereksinimler
- **Python 3.8+**
- **pip** (Python paket yöneticisi)
- **Git** (Opsiyonel, projeyi klonlamak için)

## Bağımlılıkların Yüklenmesi
Projeyi Klonlayın:
```bash
git clone https://github.com/kullaniciadi/proje-adi.git
cd proje-adi


## Sanal Ortam Oluşturun ve Etkinleştirin

```bash
# Sanal ortam oluşturun
python -m venv venv

# Windows için
venv\Scripts\activate

# Mac/Linux için
source venv/bin/activate


Bağımlılıkları Yükleyin:

pip install -r requirements.txt

Tabloların Kurulması
Projede kullanacağınız veritabanı tablolarını hazırlayın:

flask db init       # İlk kez başlatmak için
flask db migrate    # Veritabanı şemalarını oluşturur
flask db upgrade    # Migrasyonları uygulayarak veritabanını günceller


Yapılandırma
config.py dosyasında veritabanı bağlantı bilgilerini ve JWT gibi diğer yapılandırma ayarlarını tanımlayın.

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gizli_anahtar')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt_gizli_anahtar'

## 🧑‍💻 Kullanım
Yönetici Paneli
Kullanıcı Yönetimi: Yeni kullanıcı ekleme, silme ve yetki değiştirme işlemlerini buradan yapabilirsiniz.
Dosya Yönetimi: Dosya yükleme, arama ve silme işlemlerini gerçekleştirebilirsiniz.
Şifre Değiştirme: İlk girişte kullanıcıya şifre belirleme imkanı verilir, ardından kullanıcılar şifrelerini değiştirebilir.

## 🛠️ Hata Ayıklama
Sanal Ortam: Sanal ortamın (venv) aktif olduğundan emin olun.

Bağımlılıkların Güncellenmesi: Yeni bir modül eklediyseniz pip freeze > requirements.txt komutuyla requirements.txt dosyanızı güncelleyin.

Veritabanı Problemleri: Veritabanı migrasyonlarını tekrar kontrol edin veya veritabanını sıfırlamak için:

flask db downgrade
flask db upgrade

Port Sorunları: Proje bir port üzerinde çalışıyorsa başka bir port ile çalıştırmayı deneyin:

flask run --port=5001

## 🤝 Katkıda Bulunma

Bu projeyi forklayın.
Yeni bir dal (branch) oluşturun: git checkout -b özellik-adi.
Değişikliklerinizi işleyin: git commit -m 'Özellik ekle'.
Dalınıza push edin: git push origin özellik-adi.
Bir Pull Request gönderin.

## 📜 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

