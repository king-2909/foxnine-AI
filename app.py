import streamlit as st
from groq import Groq

# 1. Konfigurasi Halaman & Tema Matrix
st.set_page_config(
    page_title="Foxnine AI - Assistant & Coder",
    page_icon="🦊",
    layout="centered"
)

# Kustomisasi CSS Matrix
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
st.caption("Asisten AI Pintar, Paham Empati, & Spesialis Pemrograman")

# Sidebar untuk Pengaturan Mode
with st.sidebar:
    st.header("⚙️ Pengaturan Mode")
    mode = st.radio(
        "Pilih Mode Operasi:",
        ("💬 Mode Ngobrol & Diskusi Santai", "💻 Mode Coder & Reviewer (Double-Check)")
    )
    st.markdown("---")
    st.caption("• **Mode Ngobrol**: Respons ramah, bersahabat, paham emosi & kesehatan ringan.\n• **Mode Coder**: Analisis ganda khusus koding & logika berat.")

# Input API Key
api_key = st.text_input("🔑 Masukkan Groq API Key Kamu (gsk_...):", type="password")

if api_key:
    client = Groq(api_key=api_key.strip())
    MODEL_NAME = "openai/gpt-oss-120b"
    FALLBACK_MODEL = "llama-3.1-8b-instant"

    # Inisialisasi Riwayat Percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan percakapan sebelumnya
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ngobrol apa saja, tanya keluhan, atau minta buatkan kode..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                if mode == "💬 Mode Ngobrol & Diskusi Santai":
                    # System Prompt agar AI Natural & Paham Empati
                    system_prompt = """
                    Kamu adalah Foxnine AI, asisten AI yang ramah, hangat, empati, cerdas, dan menyenangkan diajak ngobrol.
                    Gaya bahasamu kasual tapi sopan (bisa paham bahasa sehari-hari, santai, dan tidak kaku).
                    
                    Panduan Sikap:
                    1. Jika pengguna curhat, merasa sedih, atau lelah: Berikan perhatian, dukungan moral, dan kalimat yang menenangkan.
                    2. Jika pengguna menanyakan keluhan kesehatan ringan (pusing, capek, flu, dll): Jawab dengan empati, berikan saran perawatan mandiri/pertolongan pertama yang umum dan aman, serta ingatkan secara ramah untuk konsultasi ke dokter jika gejala memberat.
                    3. Jika diajak bercanda/sapaan biasa: Jawab dengan ramah dan alami layaknya teman ngobrol.
                    4. Jawablah langsung, hangat, dan mengalir natural tanpa format yang terlalu kaku.
                    """
                    
                    # Menyusun konteks percakapan
                    messages_payload = [{"role": "system", "content": system_prompt}]
                    for msg in st.session_state.messages:
                        messages_payload.append({"role": msg["role"], "content": msg["content"]})

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages_payload
                    )
                    final_text = response.choices[0].message.content
                    st.markdown(final_text)
                    st.session_state.messages.append({"role": "assistant", "content": final_text})

                else:
                    # Mode Coder (Double-Check)
                    with st.status("🦊 [1/2] Foxnine AI (Coder) merancang solusi...", expanded=False) as status:
                        coder_prompt = f"Kamu adalah Foxnine AI Coder. Jawab permintaan teknis/koding ini secara akurat: {prompt}"
                        coder_resp = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=[{"role": "user", "content": coder_prompt}]
                        )
                        draft_code = coder_resp.choices[0].message.content
                        status.update(label="🦊 [1/2] Draft selesai!", state="complete")

                    with st.status("🦊 [2/2] Foxnine AI (Reviewer) mengoptimalkan...", expanded=True) as status:
                        reviewer_prompt = f"Periksa & optimalkan draft kodingan berikut agar tidak ada bug:\n\n{draft_code}"
                        reviewer_resp = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=[{"role": "user", "content": reviewer_prompt}]
                        )
                        final_text = reviewer_resp.choices[0].message.content
                        status.update(label="🦊 [2/2] Analisis selesai!", state="complete")

                    st.markdown(final_text)
                    st.session_state.messages.append({"role": "assistant", "content": final_text})

            except Exception as e:
                # Fallback jika model utama bermasalah
                try:
                    fallback_resp = client.chat.completions.create(
                        model=FALLBACK_MODEL,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    final_text = fallback_resp.choices[0].message.content
                    st.markdown(final_text)
                    st.session_state.messages.append({"role": "assistant", "content": final_text})
                except Exception as ex:
                    st.error(f"Terjadi kesalahan koneksi API: {e}")
else:
    st.info("Silakan masukkan Groq API Key kamu di atas untuk mulai berinteraksi dengan Foxnine AI.")
