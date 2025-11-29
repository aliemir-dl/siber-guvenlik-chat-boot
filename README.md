

🛡️ AI Security Assistant (Yapay Zeka Destekli Güvenlik Asistanı)

TÜBİTAK 2209-A Araştırma Projesi Kapsamında Geliştirilmiştir.

Bu proje, yazılım geliştirme süreçlerinde ortaya çıkan güvenlik gereksinimlerini analiz eden, OWASP, NIST, ISO 27001 gibi standartlarla eşleştiren ve geliştiricilere uygulanabilir çözüm planları sunan yapay zeka destekli bir sistemdir.

🌟 Temel Özellikler

Çift Modlu Analiz:

🚀 Fast Mode: Kural tabanlı, anlık tepki veren hızlı analiz (<200ms).

🧠 AI Mode (Derin Analiz): Yerel LLM (Ollama) kullanarak bağlam odaklı, detaylı risk analizi.

RAG (Retrieval-Augmented Generation): NVD (National Vulnerability Database) verilerini ve CVSS puanlarını analiz sürecine dahil ederek halüsinasyonu önler.

Standart Uyumluluğu: Gereksinimleri otomatik olarak OWASP Top 10, MITRE ATT&CK ve IEC 62443 maddeleriyle eşleştirir.

İki Aşamalı Çözüm: Geliştiricilere "Kısa Vadeli Acil Önlemler" ve "Uzun Vadeli Stratejik Planlar" sunar.

🛠️ Mimari ve Teknolojiler

Backend: Python, FastAPI

Yapay Zeka: Ollama (Mistral/Llama3), LangChain Konseptleri

Veri Tabanı: ChromaDB (Vektör), SQLite (Meta Veri)

Frontend: Streamlit

Veri Kaynağı: NIST NVD API

🚀 Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin.

1. Ön Gereksinimler

Python 3.10 veya üzeri

Ollama (Kurulu ve çalışır durumda olmalı)

git

2. Projeyi Klonlama

git clone [https://github.com/kullaniciadi/AI-Security-Assistant.git](https://github.com/kullaniciadi/AI-Security-Assistant.git)
cd AI-Security-Assistant


3. Sanal Ortam ve Kütüphaneler

# Sanal ortam oluşturma
python -m venv venv

# Aktifleştirme (Windows)
venv\Scripts\activate

# Aktifleştirme (Mac/Linux)
source venv/bin/activate

# Kütüphaneleri yükleme
pip install -r requirements.txt


4. LLM Modelini Hazırlama

Ollama üzerinden kullanılacak modeli indirin (Varsayılan: Mistral):

ollama run mistral


⚙️ Yapılandırma

config/settings.py dosyası varsayılan ayarları içerir. Hassas veriler için .env dosyası oluşturabilirsiniz (Opsiyonel):

# .env dosyası örneği
NVD_API_KEY=your_nvd_api_key_here
OLLAMA_BASE_URL=http://localhost:11434


▶️ Çalıştırma

Sistemi ayağa kaldırmak için iki ayrı terminal penceresi kullanın.

Terminal 1: Backend (API)

uvicorn backend.main:app --reload --port 8000


İlk çalıştırmada NVD verilerinin çekilmesi ve vektörleştirilmesi birkaç dakika sürebilir.

Terminal 2: Frontend (Arayüz)

streamlit run frontend/app.py --server.port 8501


Tarayıcınızda http://localhost:8501 adresine gidin ve analize başlayın!

🧪 Örnek Test Senaryosu

Gereksinim:

"Müşteri verilerini tutan eski bir Java uygulamamız var ve Log4j kütüphanesi güncellenmemiş. Olası riskler nelerdir?"

Beklenen Çıktı:

Risk: KRİTİK (CVSS 10.0)

CVE: CVE-2021-44228 (Log4Shell)

Öneri: Acil olarak Log4j sürümünü 2.17.1+ yükseltin veya JNDI lookup özelliğini devre dışı bırakın.

🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır. Pull request'ler kabul edilir. Büyük değişiklikler için lütfen önce bir issue açın.

📄 Lisans

MIT License


Dosya Yapısı:

AI-Security-Assistant/
│
├── backend/
│   ├── main.py                 # FastAPI ana dosyası
│   ├── ollama_integration.py   # LLM ile etkileşim
│   ├── data_manager.py         # Veri toplama ve yönetim modülü (NVD, SQLite, CromeDB)
│   ├── db/
│   │   ├── sqlite.db           # SQLite veritabanı dosyası
│   │   └── chromedb_cache/     # CromeDB dosyaları
│   └── utils/
│       └── helpers.py          # Yardımcı fonksiyonlar (ör. JSON temizleme, loglama)
│
├── frontend/
│   ├── index.html              # Ana sayfa
│   ├── style.css               # Arayüz stili
│   ├── script.js               # API ile iletişim (fetch)
│
├── models/
│   └── prompts/                # LLM için hazır prompt şablonları
│       └── analyze_prompt.txt
│
├── docs/
│   └── GereksinimDokumani.docx # Gereksinim dosyası
│
├── config/
│   └── settings.py             # API anahtarları, bağlantı yolları
│
└── README.md                   # Proje açıklaması


# Yapay Zeka Destekli Siber Güvenlik Açığı Yönetim Sistemi

Bu proje Ollama tabanlı LLM modeli kullanır.
# Terminal 1: FastAPI (Backend)
uvicorn backend.main:app --reload --port 8000

# Terminal 2: Streamlit (Frontend)
streamlit run frontend/app.py --server.port 8501


"Müşteri tarafında kritik veri işleyen eski bir Java uygulamamız var. Uygulama, hala Apache Log4j'nin eski bir versiyonunu kullanıyor. Log4j zafiyetlerini (özellikle CVE-2021-44228) temel alarak, bu durumu KRİTİK yapan riskleri değerlendir ve bize kısa vadeli acil düzeltme planı sun."