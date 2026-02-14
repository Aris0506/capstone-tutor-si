# import streamlit as st
# from openai import OpenAI
# import os
# from docx import Document

# # # --- KONFIGURASI HALAMAN ---
# # st.set_page_config(page_title="Tutor Virtual SI - UT", page_icon="🎓")

# # # --- JUDUL ---
# # st.title("🎓 Tutor Virtual Sistem Informasi")
# # st.caption("Asisten Belajar Mandiri Mahasiswa Universitas Terbuka")
# # --- KONFIGURASI HALAMAN ---
# st.set_page_config(
#     page_title="Tutor Virtual SI - UT",
#     page_icon="🎓",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # --- HEADER DENGAN LOGO ---
# col1, col2 = st.columns([1, 5])
# with col1:
#     # Pastikan file logo_ut.png ada di folder yang sama
#     try:
#         st.image("LOGO.png", width=80)
#     except:
#         st.write("🎓") # Fallback kalau gambar gak ada
# with col2:
#     st.title("Tutor Virtual SI")
#     st.markdown("*Sistem Informasi - Universitas Terbuka*")

# st.divider() # Garis pemisah biar rapi

# # --- 1. FUNGSI MEMBACA WORD (DOCX) ---
# # Fungsi ini membaca teks dari file word dan memecahnya jadi paragraf
# @st.cache_data # Biar ngebut, data dicache (disimpan sementara di memori)
# def load_docx_text(file_path):
#     doc = Document(file_path)
#     full_text = []
#     for para in doc.paragraphs:
#         if len(para.text.strip()) > 0: # Hanya ambil paragraf yang ada isinya
#             full_text.append(para.text)
#     return full_text

# # --- 2. FUNGSI PENCARI KONTEKS SEDERHANA ---
# # Karena buku tebal, kita cuma ambil paragraf yang mengandung kata kunci dari pertanyaan user
# def get_relevant_context(query, text_list, limit=5):
#     query_words = query.lower().split()
#     relevant_paragraphs = []
    
#     for paragraph in text_list:
#         # Jika ada kata dari pertanyaan yang muncul di paragraf modul, ambil paragraf itu
#         if any(word in paragraph.lower() for word in query_words if len(word) > 3): 
#             relevant_paragraphs.append(paragraph)
            
#     # Ambil 5 paragraf teratas saja biar gak kepanjangan
#     return "\n".join(relevant_paragraphs[:limit])

# # --- MAPPING FILE DATA ---
# # Pastikan nama file di sini SAMA PERSIS dengan nama file di folder 'data'
# FILES = {
#     "Algoritma & Pemrograman": "data/Algoritma Dan Pemrograman_LENGKAP_CLEANED.docx",
#     "Basis Data": "data/Basis Data_LENGKAP_CLEANED.docx",
#     "Analisis Perancangan Sistem": "data/MSIM4302 - Analisis Dan Perancangan Sistem_LENGKAP_CLEANED.docx",
#     "Sistem Informasi Manajemen": "Sistem Informasi Manajemen (Pengantar SI)_LENGKAP_CLEANED.docx"
# }

# # --- SIDEBAR ---
# with st.sidebar:
#     st.header("⚙️ Konfigurasi")
#     openai_api_key = st.text_input("OpenAI API Key", type="password")
    
#     st.divider()
#     st.header("📚 Pilih Materi Kuliah")
#     # Dropdown untuk memilih file mana yang mau dibaca
#     selected_subject = st.selectbox("Mau belajar apa hari ini?", list(FILES.keys()))
    
#     # Load data otomatis saat user memilih mata kuliah
#     file_path = FILES[selected_subject]
#     try:
#         if os.path.exists(file_path):
#             course_content = load_docx_text(file_path)
#             st.success(f"✅ Modul {selected_subject} dimuat!")
#         else:
#             st.error(f"❌ File tidak ditemukan: {file_path}")
#             course_content = []
#     except Exception as e:
#         st.error(f"Gagal membaca file: {e}")
#         course_content = []

# # --- CHAT INTERFACE ---
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "Halo! Silakan pilih mata kuliah di sebelah kiri, lalu tanyakan materi yang belum kamu paham."}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("⚠️ Masukkan API Key dulu di sidebar ya!")
#         st.stop()

#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     st.divider()
#     if st.button("Hapus Riwayat Chat 🗑️"):
#         st.session_state.messages = [] # Kosongkan memori
#         st.rerun() # Refresh halaman otomatis

#     # --- LOGIKA INTEGRASI DATA ---
#     # 1. Cari contekan dari modul
#     context_text = get_relevant_context(prompt, course_content)
    
#     # 2. Susun instruksi untuk AI (Prompt Engineering)
#     system_prompt = f"""
#     Kamu adalah Tutor Virtual untuk mata kuliah {selected_subject}.
#     Jawablah pertanyaan mahasiswa BERDASARKAN konteks berikut ini yang diambil dari modul kuliah.
    
#     KONTEKS MODUL:
#     {context_text}
    
#     ATURAN:
#     1. Jika jawaban ada di konteks, jelaskan dengan bahasa yang mudah dimengerti.
#     2. Jika konteks kosong atau tidak relevan, gunakan pengetahuan umummu tapi tetap ingatkan ini jawaban umum.
#     3. Jangan sebutkan "Berdasarkan konteks di atas", langsung saja jelaskan materinya.
#     """

#     client = OpenAI(api_key=openai_api_key)
#     try:
#         # Kirim prompt + history chat
#         final_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
#         with st.spinner("Membaca modul..."):
#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=final_messages
#             )
#             msg = response.choices[0].message.content
            
#         st.session_state.messages.append({"role": "assistant", "content": msg})
#         st.chat_message("assistant").write(msg)
#         # Tampilkan jawaban AI
#         st.session_state.messages.append({"role": "assistant", "content": msg})
#         st.chat_message("assistant").write(msg)
        
#         # FITUR BARU: Tampilkan sumber contekan (biar kelihatan canggih)
#         with st.expander("🔍 Lihat Sumber Referensi Modul"):
#             st.info(context_text) # Menampilkan potongan teks asli dari Word
        
#     except Exception as e:
#         st.error(f"Error: {e}")


import streamlit as st
from openai import OpenAI
import os
from docx import Document

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tutor Virtual SI - UT", page_icon="🎓")

# # # --- JUDUL ---
st.title("🎓 Tutor Virtual Mahasiswa UT")
st.caption("Asisten Belajar Mandiri Mahasiswa Program Studi Sistem Informasi")


# --- 3. FUNGSI LOAD DATA ---
@st.cache_data
def load_docx_text(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if len(para.text.strip()) > 0:
                full_text.append(para.text)
        return full_text
    except Exception as e:
        return []

def get_relevant_context(query, text_list, limit=5):
    query_words = query.lower().split()
    relevant_paragraphs = []
    
    for paragraph in text_list:
        if any(word in paragraph.lower() for word in query_words if len(word) > 1): 
            relevant_paragraphs.append(paragraph)
            
    return "\n".join(relevant_paragraphs[:limit])

# --- 4. MAPPING FILE (Tanpa folder 'data/' jika file sejajar dengan app.py) ---
FILES = {
    "Algoritma & Pemrograman": "data/Algoritma Dan Pemrograman_LENGKAP_CLEANED.docx",
    "Basis Data": "data/Basis Data_LENGKAP_CLEANED.docx",
    "Analisis Perancangan Sistem": "data/MSIM4302 - Analisis Dan Perancangan Sistem_LENGKAP_CLEANED.docx",
    "Sistem Informasi Manajemen": "data/Sistem Informasi Manajemen (Pengantar SI)_LENGKAP_CLEANED.docx"
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.header("📚 Pilih Materi Kuliah")
    selected_subject = st.selectbox("Mau belajar apa hari ini?", list(FILES.keys()))
    
    # Load File
    file_path = FILES[selected_subject]
    if os.path.exists(file_path):
        course_content = load_docx_text(file_path)
        st.success(f"✅ Modul {selected_subject} dimuat!")
    else:
        st.error(f"❌ File tidak ditemukan: {file_path}")
        course_content = []

    st.divider()
    # Tombol Hapus Riwayat ada di Sidebar agar tidak mengganggu chat
    if st.button("Hapus Riwayat Chat 🗑️"):
        st.session_state.messages = []
        st.rerun()

# --- 6. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Halo! Silakan pilih mata kuliah di sidebar kiri, lalu tanyakan materinya."}]

# Tampilkan history chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- 7. PROSES INPUT CHAT ---
if prompt := st.chat_input("Type Here...!"):
    if not openai_api_key:
        st.info("⚠️ Masukkan API Key dulu di sidebar ya!")
        st.stop()

    # Tampilkan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Logika Integrasi Data
    context_text = get_relevant_context(prompt, course_content)
    
    system_prompt = f"""
    Kamu adalah Tutor Virtual untuk mata kuliah {selected_subject}.
    Jawablah pertanyaan mahasiswa BERDASARKAN konteks berikut ini yang diambil dari modul kuliah.
    
    KONTEKS MODUL:
    {context_text}
    
    ATURAN:
    1. Jawab dengan ramah dan akademis.
    2. Jika konteks kosong, gunakan pengetahuan umummu tapi beri disclaimer.
    3. Gunakan format Markdown (Bold, List, Code Block) agar rapi.
    """

    client = OpenAI(api_key=openai_api_key)
    
    try:
        final_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        with st.spinner("Sedang membaca modul & menyusun jawaban..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Pastikan model ini tersedia di akunmu (atau gpt-3.5-turbo)
                messages=final_messages
            )
            msg = response.choices[0].message.content
            
        # Tampilkan output asisten
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
        # Tampilkan Sumber Referensi (Opsional di dalam expander)
        if context_text:
            with st.expander("🔍 Lihat Sumber Referensi Modul"):
                st.info(context_text)
        
    except Exception as e:
        st.error(f"Error: {e}")