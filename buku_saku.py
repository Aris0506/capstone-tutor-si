import streamlit as st
from openai import OpenAI
import os
from docx import Document



# 1. KONFIGURASI HALAMAN 
st.set_page_config(page_title="Tutor Virtual SI - UT", page_icon="🎓")

# # # --- JUDUL ---
st.title("🎓 Tutor Virtual Mahasiswa UT")
st.caption("Asisten Belajar Mandiri Mahasiswa Program Studi Sistem Informasi")


# 3. FUNGSI LOAD DATA 
@st.cache_data  # open file, then save to temporary memories
def load_docx_text(file_path): # Open file Word & ekstrak teksnya
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if len(para.text.strip()) > 0: # If PARAGRAPH/BARIS empty, just lewati (skip)
                full_text.append(para.text)
        return full_text
    except Exception as e:
        return [] # SAFETY NET: Kalau file Word-nya error atau hilang, jangan crash, balikin kosong aja

def get_relevant_context(query, text_list, limit=40): # SEARCH KEY WORD dari pertanyaan mahasiswa
    query_words = query.lower().split() # Pecah kalimat pertanyaan mahasiswa jadi kata per kata (huruf kecil)
    relevant_paragraphs = []
    
    for paragraph in text_list:
        if any(word in paragraph.lower() for word in query_words if len(word) > 1): # Cek apakah ada kata kunci di paragraf ini
            relevant_paragraphs.append(paragraph)
            
    return "\n".join(relevant_paragraphs[:limit]) # Gabungkan paragrafnya, tapi BATASI maksimal 40 biar gak boros token API

# 4. MAPPING FILE (Katalog Lemari Arsip)
# Ini adalah tipe data Dictionary (Kamus).
# Sebelah kiri = Nama yang tampil di layar web.
# Sebelah kanan = file_path (alamat asli file Word-nya di dalam folder laptop/server).
FILES = {
    "Algoritma & Pemrograman": "data/Algoritma Dan Pemrograman_LENGKAP_CLEANED.docx",
    "Basis Data": "data/Basis Data_LENGKAP_CLEANED.docx",
    "Analisis Perancangan Sistem": "data/MSIM4302 - Analisis Dan Perancangan Sistem_LENGKAP_CLEANED.docx",
    "Sistem Informasi Manajemen": "data/Sistem Informasi Manajemen (Pengantar SI)_LENGKAP_CLEANED.docx"
}

################################################################################################
#  5. SIDEBAR 
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    # # Input API Key (masukin token/kartu bayar untuk manggil OpenAI)
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.markdown("[Dapatkan API Key di sini](https://platform.openai.com/account/api-keys)")
    
    st.divider() # Garis pembatas biar rapi
    st.header("📚 Pilih Materi Kuliah")
    
    # MEMORI SEMENTARA: Cek mahasiswa lagi buka matkul apa sekarang
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = list(FILES.keys())[0] # Default-nya matkul urutan pertama

    # # Menampilkan Dropdown pilihan matkul berdasarkan laci FILES
    selected_subject = st.selectbox("Mau belajar apa hari ini?", list(FILES.keys()))
    st.markdown("""*Catatan: Bot tidak akan menjawab pertanyaan di luar materi kuliah.*""")
    
    # LOGIKA RESET OTOMATIS: Kalau mahasiswa ganti matkul, bersihkan chat! (Biar AI gak bingung konteks)
    if selected_subject != st.session_state.current_subject:
        st.session_state.current_subject = selected_subject
        st.session_state.messages = [{"role": "assistant", "content": f"Mata kuliah diubah ke {selected_subject}. Silakan bertanya!"}]
        st.rerun() # Refresh halaman web seketika
    
    
    # EKSEKUSI PEMBACAAN FILE
    file_path = FILES[selected_subject] # 1. Cari alamat file berdasarkan pilihan mahasiswa
    if os.path.exists(file_path): # 2. Cek apakah file Word fisiknya beneran ada di laptop/server
        course_content = load_docx_text(file_path) # 3. Buka file-nya, ekstrak teksnya (Panggil function yg di atas)
        st.success(f"✅ Modul {selected_subject} dimuat!")
    else:
        # SAFETY NET: Kalau file hilang, kasih peringatan merah, teks kosongin biar gak crash
        st.error(f"❌ File tidak ditemukan: {file_path}") 
        course_content = []

    st.divider()
    # Tombol Hapus Riwayat ada di Sidebar agar tidak mengganggu chat
    if st.button("Hapus Riwayat Chat 🗑️"):
        st.session_state.messages = [] # Kosongkan list memori chat
        st.rerun() # refresh halaman

    st.divider()
    st.info("Dibuat oleh Kelompok [Nomor] - Capstone Project 2026")

################################################################################################
# 6. CHAT INTERFACE
# INISIALISASI MEMORI: Kalau user baru pertama kali buka web, buat list memori kosong
if "messages" not in st.session_state:
    # Kasih pesan sambutan pertama (role: assistant = bot)
    st.session_state["messages"] = [{"role": "assistant", "content": "Halo! Silakan pilih mata kuliah di sidebar kiri, lalu tanyakan materinya."}]

# LOOPING HISTORY: Baca semua memori chat dari awal sampai akhir
for msg in st.session_state.messages:
    # Tampilkan ke layar dengan avatar sesuai peran (user / assistant)
    st.chat_message(msg["role"]).write(msg["content"])

################################################################################################
# 7. PROSES INPUT CHAT
# TUNGGU INPUT: Program berhenti di sini sampai mahasiswa ngetik dan tekan Enter
if prompt := st.chat_input("Type Here...!"):
    if not openai_api_key:
        st.info("⚠️ Masukkan API Key dulu di sidebar ya!")
        st.stop() # Hentikan proses kodingan ke bawah

    # TAMPILKAN INPUT USER: Simpan ke memori chat, lalu tampilkan di layar dgn avatar 🧑‍🎓
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍🎓").write(prompt)

    # PENCARIAN KONTEKS (RAG): 
    # Manggil fungsi get_relevant_context yg ada di atas.
    # Ngirim 2 bahan: 'prompt' (pertanyaan user) dan 'course_content' (isi buku dari sidebar).
    # Hasil sortirannya disimpen di variabel 'context_text'.
    context_text = get_relevant_context(prompt, course_content)
    
    # SYSTEM PROMPT (Otak AI): Aturan ketat / SOP agar AI tidak halusinasi
    system_prompt = f"""
    Kamu adalah Tutor Virtual ahli Sistem Informasi untuk mata kuliah {selected_subject}.
    
    TUGAS UTAMA:
    Jawab pertanyaan mahasiswa dengan lengkap dan akademis.
    
    SUMBER DATA:
    Gunakan konteks berikut yang diambil dari modul kuliah:
    ----------------
    {context_text}
    ----------------
    
    ATURAN PENTING:
    1. PRIORITASKAN jawaban dari konteks modul di atas.
    2. JIKA informasi di modul kurang, GUNAKAN PENGETAHUAN UMUM-MU, TAPI SYARATNYA: Pertanyaan harus RELEVAN dengan mata kuliah {selected_subject}.
    3. JIKA pertanyaan MELENCENG JAUH (misal: tanya SQL saat mata kuliah Algoritma, atau tanya Resep Masakan), JANGAN DIJAWAB. Katakan: "Maaf, topik ini bukan bagian dari mata kuliah {selected_subject}."
    4. JANGAN PERNAH MENJAWAB "Maaf informasi tidak ditemukan" jika topiknya masih nyambung.
    5. Langsung jelaskan definisinya dengan percaya diri.
    """
    # Siapkan koneksi ke server OpenAI
    client = OpenAI(api_key=openai_api_key)
    
    try:
        # Gabungkan System Prompt (Aturan) + Seluruh Riwayat Chat (Biar AI ingat konteks obrolan)
        final_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        # EKSEKUSI API: Munculkan animasi loading saat AI sedang berpikir
        with st.spinner("Sedang membaca modul & menyusun jawaban..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Pastikan model ini tersedia di akun (atau gpt-3.5-turbo)
                messages=final_messages
            )
            # Ambil teks jawaban hasil mikir AI
            msg = response.choices[0].message.content
            
        # Tampilkan output asisten
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant", avatar="🤖").write(msg)
        
        # Tampilkan Sumber Referensi (Opsional di dalam expander)
        if context_text:
            with st.expander("🔍 Lihat Sumber Referensi Modul"):
                st.info(context_text) # Teks dibungkus di dalam kotak biru
        
    except Exception as e:
        # SAFETY NET: Kalau API key salah, atau limit habis, jangan crash, tampilkan pesan error
        st.error(f"Error: {e}")