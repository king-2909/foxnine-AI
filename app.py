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

# Kustomisasi CSS ala Matrix (Gaya Terang, Kontras Tinggi, Neon Hijau)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* Tampilan Global */
    html, body, [class*="css"] {
        font-family: 'Share Tech Mono', monospace;
        background-color: #031508;
        color: #d1ffd6;
    }

    /* Judul Utama */
    .main-title {
        color: #00ff66;
        text-shadow: 0 0 10px #00ff66, 0 0 20px #005511;
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #8affaa;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 25px;
    }

    /* Kotak Input API Key & Chat */
    .stTextInput input, .stChatInput input {
        background-color: #052b0f !important;
        color: #ffffff !important;
        border: 2px solid #00ff66 !important;
        border-radius: 6px;
    }

    /* Styling Kotak Pesan AI & User */
    div.stChatMessage {
        background-color: #072e12;
        border: 1px solid #145a28;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.15);
    }
    
    /* Warna teks di dalam chat */
    div.stChatMessage p, div.stChatMessage span, div.stChatMessage li {
        color: #e2ffe6 !important;
        font-size: 1.05rem;
    }

    /* Kotak Blok Kode */
    pre {
        background-color: #010d04 !important;
        border: 2px solid #00ff66 !important;
        border-radius: 6px !important;
        box-shadow: inset 0 0 10px rgba(0, 255, 102, 0.2);
    }
    code {
        color: #5fff89 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Tampilan Matrix dengan Nama Foxnine AI
st.markdown('<p class="main-title">🦊 FOXNINE AI : MATRIX TERMINAL 🦊</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Spesialis Pemrograman (Double-Check) & Pelajaran Umum</p>', unsafe_allow_html=True)

# 2. Input API Key (Mengambil dari Environment atau Input Manual)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.text_input("🔑 Masukkan Google Gemini API Key Kamu (Gratis di Google AI Studio):", type="password")

if api_key:
    # Inisialisasi Google GenAI Client
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.0-flash"

    # Inisialisasi Riwayat Percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat sebelumnya
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kotak Input Chat Pengguna
    if prompt := st.chat_input("Tanyakan soal koding, matematika, atau pelajaran lainnya ke Foxnine AI..."):
        # Simpan dan tampilkan pesan pengguna
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Proses AI dengan Sistem 2-Langkah (Double-Check)
        with st.chat_message("assistant"):
            
            # --- TAHAP 1: Coder Agent ---
            with st.status("🦊 [1/2] Foxnine AI (Coder) sedang merancang solusi...", expanded=True) as status:
                try:
                    coder_response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=(
                                "Kamu adalah Foxnine AI, Senior Software Engineer dan tutor pelajaran umum (Matematika, Sains, dll.). "
                                "Jika diminta membuat kode, berikan solusi terbaik, bersih, dan terstruktur."
                            ),
                            temperature=0.2,
                        ),
                    )
                    draft_text = coder_response.text
                    st.write("✔ Draf awal berhasil dibuat.")
                    
                    # --- TAHAP 2: Reviewer Agent (Jika ada kode) ---
                    if "```" in draft_text:
                        status.update(label="🔍 [2/2] Foxnine AI (Reviewer) sedang melakukan double-check & audit bug...", state="running")
                        
                        reviewer_response = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=f"Tolong review, validasi, dan perbaiki draf kode berikut jika ada bug atau kurang efisien:\n\n{draft_text}",
                            config=types.GenerateContentConfig(
                                system_instruction=(
                                    "Kamu adalah Foxnine AI (Code Reviewer/Auditor yang sangat teliti). "
                                    "Periksa draf kode untuk mendeteksi bug, kesalahan logika, atau efisiensi. "
                                    "Berikan versi final kode yang sudah benar-benar aman dan optimal."
                                ),
                                temperature=0.1,
                            ),
                        )
                        final_response = reviewer_response.text
                        status.update(label="✅ Selesai! Foxnine AI telah memvalidasi kodenya.", state="complete", expanded=False)
                    else:
                        final_response = draft_text
                        status.update(label="✅ Selesai! Pertanyaan diproses oleh Foxnine AI.", state="complete", expanded=False)

                    # Tampilkan hasil akhir ke layar
                    st.markdown(final_response)
                    st.session_state.messages.append({"role": "assistant", "content": final_response})

                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi API: {e}")
else:
    st.warning("⚠️ Masukkan API Key terlebih dahulu untuk mengaktifkan terminal Foxnine AI.")
