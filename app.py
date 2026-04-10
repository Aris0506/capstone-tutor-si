import streamlit as st
from openai import OpenAI
import os
from docx import Document
import re



# 1. KONFIGURASI HALAMAN 
st.set_page_config(page_title="Tutor Virtual SI - UT", page_icon="🎓")

# # # --- JUDUL ---
st.title("🎓 Tutor Virtual Mahasiswa UT")
st.caption("Asisten Belajar Mandiri Mahasiswa Program Studi Sistem Informasi")


# 2. FUNGSI LOAD DATA 
@st.cache_data
def load_docx_text(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                full_text.append(text)
                
        return full_text
    
    except Exception as e:
        # Menampilkan error di layar web pakai Streamlit
        st.error(f"Gagal memuat modul: {e}") 
        return []

# 3. RAG - Retrieval (ambil konteks dari dokumen)
def get_relevant_context(query, text_list, limit=5):
    # a.PREPROCESSING QUERY (Filter kata receh)
    query_words = [word for word in query.lower().split() if len(word) > 2]
    
    # b. Safety Net: Kalau user cuma ngetik kata pendek kayak "IT"
    if not query_words:
        query_words = query.lower().split()

    scored = []
    
    # SCORING (TF & Exact Match)
    for paragraph in text_list:
        # Bersihkan paragraf dari tanda baca sebelum dihitung
        clean_paragraph = re.sub(r'[^\w\s]', '', paragraph.lower())
        
        # c. scoring (Hitung frekuensi kemunculan kata secara eksak (Term Frequency))
        score = sum(clean_paragraph.split().count(word) for word in query_words)
        # d. Simpan yang relevan
        if score > 0:
            # Yang disimpan tetap paragraf asli (paragraph) yang ada tanda bacanya, 
            # biar AI gampang bacanya, bukan clean_paragraph
            scored.append((score, paragraph)) 

    # SAFETY NET KALO GAK KETEMU APA-APA
    if not scored:
        return "Materi tidak ditemukan dalam modul."

    # RANKING
    scored.sort(reverse=True) # e. Ranking
    return "\n".join([p for _, p in scored[:limit]]) # f. Ambil top context

# 4. MAPPING FILE (Tanpa folder 'data/' jika file sejajar dengan app.py) ---
FILES = {
    "Algoritma & Pemrograman": "data/Algoritma Dan Pemrograman_LENGKAP_CLEANED.docx",
    "Basis Data": "data/Basis Data_LENGKAP_CLEANED.docx",
    "Analisis Perancangan Sistem": "data/MSIM4302 - Analisis Dan Perancangan Sistem_LENGKAP_CLEANED.docx",
    "Sistem Informasi Manajemen": "data/Sistem Informasi Manajemen (Pengantar SI)_LENGKAP_CLEANED.docx"
}

#  5. SIDEBAR 
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.markdown("[Dapatkan API Key di sini](https://platform.openai.com/account/api-keys)")
    
    st.divider()
    st.header("📚 Pilih Materi Kuliah")
    
    # Simpan state subject sebelumnya untuk ngecek apakah user ganti matkul
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = list(FILES.keys())[0]

    selected_subject = st.selectbox("Mau belajar apa hari ini?", list(FILES.keys()))
    st.markdown("""*Catatan: Bot tidak akan menjawab pertanyaan di luar materi kuliah.*""")
    
    # LOGIKA RESET OTOMATIS: if ganti matkul, bersihkan chat!
    if selected_subject != st.session_state.current_subject:
        st.session_state.current_subject = selected_subject
        st.session_state.messages = [{"role": "assistant", "content": f"Mata kuliah diubah ke {selected_subject}. Silakan bertanya!"}]
        st.rerun()
    
    
    # Load File
    file_path = FILES[selected_subject]
    if os.path.exists(file_path):
        course_content = load_docx_text(file_path)
        st.success(f"Modul {selected_subject} dimuat!")
    else:
        st.error(f"File tidak ditemukan: {file_path}")
        course_content = []

    st.divider()
    # Tombol Hapus Riwayat ada di Sidebar agar tidak mengganggu chat
    if st.button("Hapus Riwayat Chat 🗑️"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.info("Dibuat oleh Kelompok [Nomor] - Capstone Project 2026")

# 6. CHAT INTERFACE
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Halo! Silakan pilih mata kuliah di sidebar kiri, lalu tanyakan materinya."}]

# Tampilkan history chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 7. PROSES INPUT CHAT
if prompt := st.chat_input("Type Here...!"):
    if not openai_api_key:
        st.info("⚠️ Masukkan API Key dulu di sidebar ya!")
        st.stop()

    # Tampilkan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍🎓").write(prompt)

    #8. AUGMENTATION (masukin konteks ke prompt) Logika Integrasi Data
    context_text = get_relevant_context(prompt, course_content)
    
    # SYSTEM PROMPT
    system_prompt = f"""
    Kamu adalah Tutor Virtual ahli Sistem Informasi untuk mata kuliah {selected_subject}.

    TUGAS UTAMA:
    Berikan jawaban yang jelas, terstruktur, dan bersifat akademis untuk membantu mahasiswa memahami materi.

    SUMBER DATA:
    Gunakan konteks berikut yang diambil dari modul kuliah:
    ----------------
    {context_text}
    ----------------
    
    ATURAN:
    1. PRIORITASKAN jawaban berdasarkan konteks modul di atas.
    2. Jika konteks tidak cukup, boleh menggunakan pengetahuan umum SELAMA masih relevan dengan mata kuliah {selected_subject}.
    3. Jika pertanyaan tidak relevan dengan mata kuliah, tolak dengan sopan:
    "Maaf, topik ini bukan bagian dari mata kuliah {selected_subject}."
    4. Jika konteks terbatas, tetap jawab dengan penjelasan terbaik dan jelaskan bahwa informasi dari modul terbatas.
    5. Gunakan bahasa yang jelas, runtut, dan mudah dipahami mahasiswa.
    6. Hindari jawaban yang terlalu singkat tanpa penjelasan.
    """

    client = OpenAI(api_key=openai_api_key)
    
    try:
        final_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        with st.spinner("Sedang membaca modul & menyusun jawaban..."):
            #9. GENERATION LLM Jawab
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Pastikan model ini tersedia di akun (atau gpt-3.5-turbo)
                messages=final_messages
            )
            msg = response.choices[0].message.content
            
        # Tampilkan output asisten
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant", avatar="🤖").write(msg)
        
        # Tampilkan Sumber Referensi (Opsional di dalam expander)
        if context_text:
            with st.expander("🔍 Lihat Sumber Referensi Modul"):
                st.info(context_text)
        
    except Exception as e:
        st.error(f"Error: {e}")