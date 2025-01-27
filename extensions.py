from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy'nin varsayılan bağlantı havuzu ayarlarını özelleştirme
db = SQLAlchemy(
    engine_options={
        "pool_size": 10,  # Aynı anda açık tutulabilecek maksimum bağlantı sayısı
        "max_overflow": 5,  # Gerekirse açılabilecek ek bağlantı sayısı
        "pool_timeout": 30,  # Bağlantı havuzu doluyken bekleme süresi (saniye)
        "pool_recycle": 1800,  # Bağlantıların otomatik olarak yeniden oluşturulma süresi (saniye)
    }
)
