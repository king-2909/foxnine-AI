import streamlit as st
from groq import Groq

# API Key Groq Permanen
API_KEY_DIRECT = "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"
client = Groq(api_key=API_KEY_DIRECT.strip())

# Konfigurasi Halaman & Tema Matrix
st.set_page_config(
    page_title="Foxnine AI - Ultimate Terminal",
    page_icon="🦊",
    layout="centered"
)

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

st.title("🦊 FOXNINE AI : ULTIMATE MATRIX 🦊")
st.caption("Asisten Gaul, Pakar Sains & Koding, Bebas Hambatan")

# Sidebar Mode Operasi
with st.sidebar:
    st.header("Pilih Mode Asisten")
    mode = st.radio(
        "Mode Aktif:",
        (" mode Bebas (Teman Ngobrol)", " Mode Expert Belajar (Math, Fisika, Kimia, Bahasa)", " Mode Coder & Sistem")
    )
    st.markdown("---")
    st.caption("• **chill**: Santai, bahasa bebas/gaul, paham info luar.\n• **Mode Belajar**: Penjelasan step-by-step paling gampang dimengerti.\n• **Mode Coder**: Analisis kode ganda.")

MODEL_NAME = "openai/gpt-oss-120b"
FALLBACK_MODEL = "llama-3.1-8b-instant"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tulis pesan, soal Fisika/Matematika, atau ajak ngobrol..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if mode == " Mode chill & Bebas (Teman Ngobrol)":
                system_prompt = """
                Kamu adalah Foxnine AI, asisten pribadi yang gaul, santai, asyik diajak ngobrol, dan menggunakan bahasa sehari-hari/gaul yang natural tanpa kaku.
                Aturan & Batasan:
                1. Bahasa sangat luwes, santai, dan fleksibel (minim batasan bahasa, asalkan tetap asyik).
                2. Bahasan bahaya/kriminalitas berat (seperti rencana kejahatan sungguhan atau terorisme/pembuatan bom) dilarang keras. Namun, jika pengguna bertanya soal mekanika atau cara kerja senjata api (senpi) dari sudut pandang ilmu pengetahuan, sejarah, atau mekanika teknik, boleh dijelaskan secara objektif demi edukasi dan wawasan sains.
                3. Berikan informasi yang up-to-date dan terbuka dengan dunia luar.
                """
            elif mode == "📚 Mode Expert Belajar (Math, Fisika, Kimia, Bahasa)":
                system_prompt = """
                Kamu adalah Foxnine AI versi Tutor Expert (Matematika, Fisika, Kimia, dan Bahasa).
                Gaya bahasa tetap santai dan gaul biar tidak bosan, TAPI ketika menjelaskan materi pelajaran atau soal:
                1. JANGAN HANYA MEMBERIKAN JAWABAN AKHIR.
                2. Berikan penjabaran langkah-langkah (step-by-step) dengan cara yang PALING MUDAH DIMENGERTI, analogi sederhana, atau logika dasar yang gampang nempel di kepala.
                """
            else:
                system_prompt = """
                Kamu adalah Foxnine AI Coder Expert. Bantu selesaikan dan optimalkan masalah pemrograman secara mendalam dan akurat.
                """

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

        except Exception as e:
            try:
                fallback_resp = client.chat.completions.create(
                    model=FALLBACK_MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                final_text = fallback_resp.choices[0].message.content
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            except Exception as ex:
                st.error(f"Error: {e}")
