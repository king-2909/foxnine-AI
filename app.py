import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Konfigurasi Halaman & Tema Matrix Terang
st.set_page_config(
    page_title="Foxnine AI - Coder & Assistant",
    page_icon="🦊",
    layout="centered"
)

# Kustomisasi CSS ala Matrix
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    html, body, [class*="css"] {
        font-family: 'Share Tech Mono', monospace;
    }
    .stApp {
        background-color: #0d1117;
        color: #00ff66;
    }
    .stTextInput input {
        color: #00ff66;
        background-color: #161b22;
        border: 1px solid #00ff66;
    }
    .stButton button {
        background-color: #00ff66;
        color: #0d1117;
        font-weight: bold;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🦊 FOXNINE AI : MATRIX TERMINAL 🦊")
st.caption("Spesialis Pemrograman (Double-Check) & Pelajaran Umum")

# Input API Key
api_key = st.text_input("🔑 Masukkan Google Gemini API Key Kamu (Gratis di Google AI Studio):", type="password")

if api_key:
    client = genai.Client(api_key=api_key.strip())

    # Fungsi cerdas memilih model yang benar-benar aktif & terbaru
    def get_valid_model():
        try:
            available_models = [m.name for m in client.models.list()]
            
            # Prioritas 1: Gunakan model rekomendasi Google saat ini
            for name in available_models:
                if "gemini-3.8-flash" in name:
                    return name
            
            # Prioritas 2: Cari model versi 3.x lainnya jika ada
            for name in available_models:
                if "gemini-3" in name and "flash" in name:
                    return name
                    
            # Fallback jika tidak terdeteksi
            return "gemini-3.8-flash"
        except Exception:
            return "gemini-3.8-flash"

    selected_model = get_valid_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Tanyakan sesuatu atau minta buatkan kode..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Step 1: Coder Agent
                with st.status("🦊 [1/2] Foxnine AI (Coder) sedang merancang solusi...", expanded=False) as status:
                    coder_prompt = f"Kamu adalah Foxnine AI Coder. Jawab permintaan user ini sebaik dan seakurat mungkin: {prompt}"
                    coder_response = client.models.generate_content(
                        model=selected_model,
                        contents=coder_prompt
                    )
                    draft_code = coder_response.text
                    status.update(label="🦊 [1/2] Draft awal selesai dirancang!", state="complete")

                # Step 2: Reviewer Agent
                with st.status("🦊 [2/2] Foxnine AI (Reviewer) sedang mengecek & mengoptimalkan...", expanded=True) as status:
                    reviewer_prompt = f"""
                    Kamu adalah Foxnine AI Reviewer. Periksa draft jawaban dari Coder berikut ini.
                    Pastikan tidak ada bug, logika kode benar, dan penjelasannya jelas serta mudah dipahami.
                    
                    Draft Coder:
                    {draft_code}
                    
                    Tolong berikan hasil akhir yang sudah diperbaiki/dioptimalkan dengan format yang rapi dan profesional!
                    """
                    final_response = client.models.generate_content(
                        model=selected_model,
                        contents=reviewer_prompt
                    )
                    status.update(label="🦊 [2/2] Analisis selesai!", state="complete")

                st.markdown(final_response.text)
                st.session_state.messages.append({"role": "assistant", "content": final_response.text})

            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi API: {e}")
else:
    st.info("Silakan masukkan API Key kamu di atas untuk mulai berinteraksi dengan Foxnine AI.")
