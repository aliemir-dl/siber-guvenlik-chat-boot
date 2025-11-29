import streamlit as st
import requests
from typing import Optional, Dict, List, Any

# --- AYARLAR ---
# FastAPI sunucusunun adresi (backend varsayılan portu 8000)
API_BASE_URL = "http://localhost:8000/api/v1" 

# --- Pydantic Modellerinin Streamlit Versiyonu (Basitleştirilmiş) ---
class FrontendAnalysisResponse:
    """Backend'den gelen JSON cevabını tutan ve iç içe yapıyı çözen sınıf."""
    def __init__(self, data: Dict[str, Any]):
        self.status = data.get("status", "error")
        self.mode_used = data.get("mode_used", "N/A")
        self.processing_time_ms = data.get("processing_time_ms", 0)
        
        # Yeni Prompt yapısından gelen alanlar
        self.risk_level = data.get("risk_level", "Bilinmiyor")
        self.summary = data.get("summary", "Detaylı özet alınamadı.")
        self.cve_id_matches = data.get("cve_id_matches", [])
        self.framework_matches = data.get("framework_matches", {})
        
        # İç içe geçmiş öneri yapısını düzleştirme
        suggestions_data = data.get("security_suggestions", {})
        self.suggestions = {
            "short_term": suggestions_data.get("short_term", []),
            "long_term": suggestions_data.get("long_term", [])
        }

# --- API İLE İLETİŞİM FONKSİYONU ---

def call_analysis_api(requirement: str, mode: str) -> Optional[FrontendAnalysisResponse]:
    """FastAPI backend API'ına analiz isteği gönderir."""
    url = f"{API_BASE_URL}/analyze"
    payload = {
        "requirement_text": requirement,
        "analysis_mode": mode,
        "standard_frameworks": ["OWASP", "MITRE", "NIST", "ISO", "IEC 62443"]
    }

    try:
        response = requests.post(url, json=payload, timeout=120) 
        response.raise_for_status() 
        
        # Cevabın başarılı olduğunu varsayarak FrontendAnalysisResponse nesnesi oluştur
        return FrontendAnalysisResponse(response.json())
    
    except requests.exceptions.ConnectionError:
        st.error(f"Bağlantı Hatası: Backend API ({url}) çalışmıyor. Lütfen FastAPI uygulamasını başlattığınızdan emin olun.")
        return None
    except requests.exceptions.HTTPError as e:
        error_detail = response.json().get('detail', 'Bilinmeyen Hata')
        st.error(f"API Hatası (HTTP {response.status_code}): Backend'de bir hata oluştu. Detay: {error_detail}")
        return None
    except Exception as e:
        st.error(f"Beklenmeyen Hata: {e}")
        return None


# --- STREAMLIT ARAYÜZ YAPISI ---

def get_risk_color(level: str) -> str:
    """Risk seviyesine göre renk kodu döner."""
    level = level.upper()
    if level == "KRİTİK": return "red"
    if level == "YÜKSEK": return "orange"
    if level == "ORTA": return "yellow"
    if level == "DÜŞÜK": return "green"
    return "gray"

def main_dashboard():
    st.set_page_config(layout="wide", page_title="AI Security Assistant")

    st.title("🛡️ Yapay Zeka Destekli Güvenlik Haritalama Sistemi")
    st.markdown("İş veya teknik gereksinimlerinizi analiz ederek, ilgili güvenlik çerçeveleriyle eşleştirin ve çözüm önerileri alın.")
    st.markdown("---")
    
    # --- YAN PANEL: Ayarlar ve Çerçeveler ---
    with st.sidebar:
        st.header("⚙️ Analiz Ayarları")
        
        analysis_mode = st.radio(
            "Analiz Modunu Seçin:",
            ("auto", "fast", "ai"),
            format_func=lambda x: {"auto": "Otomatik Seçim", "fast": "Hızlı Mod", "ai": "Yapay Zeka (Derin)"}[x],
            index=2, # Başlangıçta AI modu seçili olsun
            help="Auto: Kural tabanlı Fast Mode'u dener, eşleşmezse veya zorunluysa AI Mode'a geçer."
        )
        
        ai_status_icon = "🟢" if analysis_mode != "fast" else "🟡"
        st.markdown(f"**Yapay Zeka Durumu:** {ai_status_icon} **Mevcut**")

        st.markdown("---")
        st.subheader("Desteklenen Çerçeveler")
        st.success("OWASP İlk 10")
        st.success("MITRE ATT&CK")
        st.success("NIST Siber Güvenlik Çerçevesi")
        st.success("ISO 27001/27002")
        st.success("IEC 62443") 

    # --- ANA İÇERİK: Gereksinim Girişi ---
    st.header("Sistem Genel Bakışı")
    
    requirement_input = st.text_area(
        "İşletmenizin veya teknik gereksinimlerinizin listesini girin:",
        key="requirement_text",
        height=200,
        placeholder="Örnek: Yeni e-ticaret platformumuzda kullanıcı şifrelerini güvenli bir şekilde saklamalıyız ve müşteri kişisel verilerine yetkisiz erişimi engellemeliyiz."
    )
    
    if st.button("🔎 Gereksinimi Analiz Et", type="primary"):
        if requirement_input:
            with st.spinner(f"**{analysis_mode.upper()}** Modu ile analiz ediliyor..."):
                result = call_analysis_api(requirement_input, analysis_mode)

            if result and result.status == "success":
                display_results(result)
            elif result:
                st.warning("Analiz başarılı ancak sonuçlar beklendiği gibi işlenemedi.")
        else:
            st.warning("Lütfen analiz edilecek bir gereksinim metni girin.")


def display_results(result: FrontendAnalysisResponse):
    """API'dan gelen zenginleştirilmiş sonuçları gösterir."""
    st.markdown("---")
    
    # Risk Seviyesi Metriği
    risk_color = get_risk_color(result.risk_level)
    st.markdown(f"""
    <div style='background-color: {risk_color}; padding: 10px; border-radius: 5px; color: white; text-align: center; margin-bottom: 20px;'>
        <h3 style='margin: 0; color: white;'>RISK SEVİYESİ: {result.risk_level.upper()}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"Kullanılan Mod: **{result.mode_used}** | Tepki Süresi: **{result.processing_time_ms} ms**")
    
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Özet ve CVE Eşleşmeleri
        st.subheader("📋 Genel Özet ve Etki Analizi")
        st.info(result.summary)
        
        if result.cve_id_matches:
            st.markdown("**İlgili CVE ID'leri:**")
            st.code(", ".join(result.cve_id_matches))
        
        # Eşleşen Çerçeveler
        st.subheader("🔗 Eşleşen Çerçeveler (Nedenleri)")
        if result.framework_matches:
            for framework, match in result.framework_matches.items():
                # Neden kısmını ayrı göster
                parts = match.split("(Neden:", 1)
                st.markdown(f"**{framework}**: `{parts[0].strip()}`")
                if len(parts) > 1:
                    st.caption(f"Açıklama: {parts[1].replace(')', '').strip()}")
        else:
            st.info("Hiçbir güvenlik çerçevesi eşleştirilemedi.")

    with col2:
        # Çözüm Planı (Kısa ve Uzun Vadeli)
        st.subheader("💡 İki Aşamalı Çözüm Planı")
        
        # Kısa Vadeli Önlemler
        st.markdown("**1. Kısa Vadeli Acil Önlemler**")
        if result.suggestions.get('short_term'):
            for suggestion in result.suggestions['short_term']:
                st.success(f"✔️ {suggestion}")
        else:
            st.warning("Kısa vadeli acil öneri bulunamadı.")
            
        # Uzun Vadeli Önlemler
        st.markdown("**2. Uzun Vadeli Stratejik Önlemler**")
        if result.suggestions.get('long_term'):
            for suggestion in result.suggestions['long_term']:
                st.info(f"➕ {suggestion}")
        else:
            st.warning("Uzun vadeli stratejik öneri bulunamadı.")


if __name__ == "__main__":
    main_dashboard()