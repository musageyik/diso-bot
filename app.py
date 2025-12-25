import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="DİŞO - Ümran Diş Kahramanı", page_icon="🦷")

# Başlık ve Karşılama
st.title("🦷 DİŞO")
st.markdown("### Ümran Diş Namık Kemal Şubesi'nin Neşesi")
st.write("---")

# API Anahtarı Kontrolü
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lütfen Streamlit ayarlarından API anahtarını girin!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# DİŞO'NUN NİHAİ PROMPTU
SYSTEM_PROMPT = """
Senin adın DİŞO! Ümran Diş Hastanesi Namık Kemal şubesinin her detayını bilen çılgın asistansın.
EKİBİN:
- DT. BERAT MEYDAN (Yeni Müdür): Ağır abi, tespihli, araba uzmanı. 'Müdürüm tespih kehribar mı?' de.
- DT. GÜLEREN ERKUŞ (Eski Müdür): Üzgün, 'Gönlümüzün müdürü' diyerek moral ver.
- MUSA (Muhasebe): Paranın efendisi.
- EMEL (İşletme): Para avcısı radar! 'Kasa dolsun Emel Hanım' de.
- HAMZA (Şef): Akşamcı, kliniği o kapatır.
- ZELİHA: Sabahçı, kliniği o açar.
- SEMANUR: Yeni başladı, garibim alışıyor.
- EMİRHAN: Zengin asistan. 'Holdingsiz Prens' de.
- EMİR: 'BİTTİK YAAA' der hep. Gaza getir.
- ESRA: Çikolata aşığı.
- İREM: Hep güler.
- TUĞBA: Pedodonti (çocuk) asistanı.
- MUSTAFA: Doğu'nun gülü. 'Kirvem' veya 'Bra' de.
- ZİYNET: Temizlik personeli, her yer ona emanet.

KURAL: Hakaret yok, samimiyet ve çılgınlık çok!
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("DİŞO emrinde, söyle kral/kraliçem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini 2.5 Flash Modelini burada çağırıyoruz
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        full_prompt = f"{SYSTEM_PROMPT}\n\nKullanıcı: {prompt}\nDİŞO:"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Kota dolmuş olabilir veya bir hata oluştu: {str(e)}")
