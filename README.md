# 📁 Flask ile Geliştirilen Dosya Yönetim Sistemi

Bu proje, kullanıcıların dosya yüklemesi, yönetmesi ve detaylı loglama yapabilmesi için Flask ile geliştirilmiş bir dosya yönetim sistemi sağlar.



## 🚀 Özellikler
- **Kullanıcı Yönetimi**: Kayıt, giriş, şifre belirleme ve değiştirme.
- **Yetkilendirme**: Rol bazlı erişim kontrolü (Çalışan, Müdür Yardımcısı, Müdür, Patron, Admin).
- **Dosya Yükleme ve Yönetimi**: Dosya yükleme, arama ve loglama.
- **Detaylı Loglama**: Kullanıcı aktivitelerinin kaydını tutarak yöneticiye raporlama imkanı sağlar.
- **Yönetici Paneli**: Yönetici rolündeki kullanıcılar için kullanıcı ve log kayıtlarını yönetme arayüzü.

---


## Gereksinimler
- **Docker (20.10+ önerilir)**
- **Docker Compose** (Python paket yöneticisi)
- **Docker Swarm** modunun etkin olduğu bir sunucu ortamı (tek veya birden fazla node).

---

## 📦 Proje Yapısı
Beyanname/  
├── app/                 # Flask uygulaması  
├── migrations/          # Veritabanı migrasyonları  
├── static/              # Statik dosyalar (CSS, JS, img)  
├── templates/           # HTML şablon dosyaları  
├── Dockerfile           # Flask uygulaması için Docker yapılandırması  
├── docker-compose.yml   # Servisleri tanımlayan Compose dosyası  
└── README.md            # Proje açıklamaları  

---

## 🐳 Docker Swarm ile Dağıtım Adımları
### 1. Docker Swarm Modunu Başlat ###
Docker Swarm kullanabilmek için aşağıdaki komutla Swarm modunu başlatın:
```
docker swarm init

```
Eğer birden fazla sunucu kullanıyorsanız, diğer sunucuları Swarm’a eklemek için aşağıdaki komutu kullanabilirsiniz:
```
docker swarm join-token manager

```
### 2. Overlay Network Oluştur ###
```
docker network create --driver overlay new_shared_network

```

### 3. Docker Compose Dosyası ###

docker-stack.yml dosyasını kullanarak servislerinizi tanımlayın.


### 4. Stack’i Dağıt ###
Swarm modunda stack’i çalıştırmak için aşağıdaki komutu kullanın:
```
docker stack deploy -c docker-compose.yml beyanname

```
Bu komut, Docker Compose dosyasındaki tüm servisleri Swarm üzerinde başlatır.
### 5. Servisleri Kontrol Et ###
Başlatılan servislerin durumunu kontrol etmek için şu komutu kullanabilirsiniz:
```
docker service ls

```
Her servisin REPLICAS değerini kontrol ederek doğru şekilde çalıştığını doğrulayabilirsiniz.
### 6. Uygulamaya Erişim ###
Uygulama başarılı bir şekilde çalışıyorsa, varsayılan olarak şu adresten erişebilirsiniz:

http://localhost:5000

Eğer birden fazla node kullanıyorsanız, manager node’un IP adresini kullanabilirsiniz:
```
http://<manager-node-ip>:5000

```
---
## 🛠️ Hata Ayıklama  ##
### Data too long for column Hatası ve Çözümü ###
Tablodaki atr_belgesi sütunu BLOB türünde olduğundan, büyük dosyalar için yetersiz kapasite (65 KB) hatası oluştu.
### Çözüm: LONGBLOB ile Güncelleme ###
Container'a bağlanın:
```
docker exec -it <db_container_id> mysql -u root -p
```
Veritabanı şifresini girerek container'a bağlanın.

Sütun Tipini Güncelleyin:
```
ALTER TABLE beyanname_kayitlari MODIFY COLUMN atr_belgesi LONGBLOB;

```
Kontrol Edin:
```
DESCRIBE beyanname_kayitlari;
```
LONGBLOB, 4 GB'a kadar veri saklayabilir ve büyük dosyalar için uygundur. 🚀
### Overlay Network Sorunları ###
Ağ ile ilgili sorun yaşarsanız, mevcut ağı silip yeniden oluşturabilirsiniz:

```
docker network rm new_shared_network
docker network create --driver overlay new_shared_network
```
## Port Çakışması ##
Eğer bir port başka bir uygulama tarafından kullanılıyorsa, docker-compose.yml dosyasındaki ports kısmını değiştirin:
```
ports:
  - "8080:5000"

```
Sonrasında şu adresten erişim sağlayabilirsiniz:

http://localhost:8080

---
## 🤝 Katkıda Bulunma ##

- Bu projeyi forklayın.
- Yeni bir dal (branch) oluşturun: git checkout -b ozellik-adi.  
- Değişikliklerinizi işleyin: git commit -m "Yeni özellik eklendi".  
- Dalınıza push edin: git push origin ozellik-adi.  
- Bir Pull Request gönderin.
