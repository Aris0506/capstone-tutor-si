import streamlit as st
from openai import OpenAI

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Tutor Virtual SI - UT",
    page_icon="🎓",
    layout="centered"
)

# --- JUDUL & INTRO ---
st.title("🎓 Tutor Virtual Sistem Informasi")
st.caption("Asisten Belajar Mandiri Mahasiswa Universitas Terbuka")

# --- SIDEBAR (UNTUK API KEY & INFO) ---
with st.sidebar:
    st.header("Konfigurasi")
    # Input API Key (Supaya aman, user input sendiri)
    openai_api_key = st.text_input("Masukkan OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Dapatkan API Key di sini](https://platform.openai.com/account/api-keys)")
    
    st.divider()
    st.header("Panduan")
    st.markdown("""
    Bot ini dapat membantu menjelaskan:
    - 📚 Konsep Sistem Informasi
    - 🐍 Coding (Python, SQL, Web)
    - 📊 Basis Data & Algoritma
    
    *Catatan: Bot tidak akan menjawab pertanyaan di luar materi kuliah.*
    """)
    st.info("Dibuat oleh Kelompok [Nomor] - Capstone Project 2026")

# --- SYSTEM PROMPT (OTAKNYA) ---
# Ini bagian krusial sesuai proposal Bab III (Validasi/Guardrails)
system_prompt = """
Kamu adalah Asisten Dosen (Tutor Virtual) untuk mahasiswa Sistem Informasi Universitas Terbuka.
Tugasmu adalah membantu mahasiswa memahami materi kuliah seperti Algoritma, Basis Data, Python, Manajemen Proyek SI, dll.

Aturan Penting:
1. Jawablah dengan ramah, akademis, tapi mudah dimengerti.
2. Gunakan format Markdown yang rapi (bold untuk istilah penting, code block untuk kodingan).
3. JIKA mahasiswa bertanya di luar topik akademik (misal: resep masakan, gosip artis, politik), tolak dengan sopan.
   Contoh penolakan: "Maaf, saya hanya bertugas membantu materi kuliah Sistem Informasi. Ada yang bisa saya bantu terkait materi?"
4. Jika ditanya tentang kodingan, berikan contoh code dan penjelasannya.
"""

# --- INISIALISASI SESSION STATE (RIWAYAT CHAT) ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", 
         "content": "Halo! Saya Tutor Virtualmu. Mau belajar materi apa hari ini? (Misal: SQL, ERD, atau Python)"
         }
    ]

# --- TAMPILKAN RIWAYAT CHAT DI LAYAR ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- PROSES INPUT CHAT ---
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("⚠️ Tolong masukkan OpenAI API Key di sidebar sebelah kiri dulu ya!")
        st.stop()

    # 1. Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Proses ke OpenAI
    client = OpenAI(api_key=openai_api_key)
    
    try:
        # Siapkan history lengkap untuk dikirim (supaya nyambung konteksnya)
        # Kita selipkan system prompt di awal
        full_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        with st.spinner("Sedang mencari jawaban di modul..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Atau gpt-3.5-turbo (lebih murah)
                messages=full_messages
            )
            msg = response.choices[0].message.content
            
        # 3. Tampilkan balasan AI
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")