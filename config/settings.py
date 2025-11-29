# config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Projenin kök dizinini belirler
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Proje Ayarları
    PROJECT_NAME: str = "AI Security Assistant"
    API_V1_STR: str = "/api/v1"

    # Veri ve Veritabanı Ayarları
    SQLITE_DB_PATH: Path = BASE_DIR / "backend" / "db" / "sqlite.db"
    CHROMADB_CACHE_PATH: Path = BASE_DIR / "backend" / "db" / "chromedb_cache"

    # Ollama (Yerel LLM) Ayarları
    # Eğer Ollama farklı bir hostta çalışıyorsa burayı değiştirebiliriz.
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL_NAME: str = "mistral:latest" # Veya kullanmak istediğiniz başka bir model

    # Harici API Anahtarları (NVD, vb.)
    # Hassas bilgileri burada tutmamalıyız, bunları ortam değişkenlerinden (env) çekmeliyiz.
    NVD_API_KEY: str = "YOUR_NVD_API_KEY_HERE"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()