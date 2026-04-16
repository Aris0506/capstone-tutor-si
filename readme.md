# Gambaran Besar

RAG  3 komponen utama:
- Retrieval → ambil konteks dari dokumen
- Augmentation → masukin konteks ke prompt
- Generation → LLM jawab


# 🛡️ BUKU SAKU SIDANG CAPSTONE: ARIS (LEAD PROGRAMMER)

---

## PILAR 1: KONSEP DASAR & VALUE SISTEM (Serangan Konseptual)
Gunakan ini kalau dosen nanya soal "Apa ini?" dan "Kenapa bikin ini?"

### Q: Coba jelaskan secara singkat sistem yang Anda buat!

**Jawaban (BLUF):**  
"Sistem ini adalah Tutor Virtual berbasis RAG (Retrieval-Augmented Generation) yang menjawab pertanyaan murni berdasarkan dokumen materi kampus, bukan berdasarkan halusinasi AI."

**Penjelasan:**  
"Alurnya ada 3: Pertama sistem mencari teks relevan dari modul (Retrieval), lalu menyuntikkan teks itu ke dalam instruksi AI (Augmentation), dan terakhir AI menyusun jawabannya (Generation)."

---

### Q: Apa kelebihan utama chatbot ini dibanding ChatGPT biasa?

**Jawaban (BLUF):**  
"Kelebihan utamanya adalah jawaban yang terkontrol dan berbasis konteks terverifikasi."

**Penjelasan:**  
"Chatbot biasa berpotensi memberikan jawaban yang tidak sesuai kurikulum. Dengan metode RAG, sistem kami mengunci pengetahuan AI agar hanya berpatokan pada modul yang diunggah, sehingga risiko halusinasi sangat minim."

---

## PILAR 2: ARSITEKTUR & KEPUTUSAN TEKNIS (Serangan Logika Pemrograman)
Gunakan ini kalau dosen nanya soal kode, Streamlit, atau cara sistem bekerja di belakang layar.

### Q: Bagaimana sistem memastikan jawabannya tidak menyimpang dari topik?

**Jawaban (BLUF):**  
"Sistem kami menggunakan pengamanan ganda melalui kombinasi Retrieval dan System Prompt."

**Penjelasan:**  
"Pertama, sistem mengambil konteks yang spesifik dari modul. Kedua, saya menanamkan System Prompt yang secara tegas membatasi model agar hanya menjawab berdasarkan konteks tersebut dan menolak topik di luar materi."

---

### Q: Kenapa Anda memilih Streamlit?

**Jawaban (BLUF):**  
"Karena fokus riset MVP ini adalah pada kecerdasan buatannya, bukan kerumitan front-end."

**Penjelasan:**  
"Streamlit menggunakan Python yang ekosistem AI-nya paling matang. Ini memungkinkan kami membangun purwarupa antarmuka web dengan sangat cepat agar bisa segera menguji efektivitas logika Retreival dan API-nya."

---

## PILAR 3: EVALUASI & ROADMAP (Serangan Kelemahan Sistem)
Gunakan ini saat dosen mulai mencari-cari celah atau kekurangan aplikasi lu.

### Q: Coba jujur, apa kelemahan utama sistem Anda saat ini?

**Jawaban (BLUF):**  
"Kelemahan utama MVP ini ada pada metode pencariannya (Retrieval) yang masih sederhana dan aplikasi yang bersifat stateless."

**Penjelasan:**  
"Sistem ini belum menyimpan riwayat obrolan secara permanen. Selain itu, karena masih menggunakan pencarian kata kunci (Keyword-based), sistem bisa gagal menemukan materi jika kata yang diketik mahasiswa berbeda ejaannya dengan yang ada di modul."

---

### Q: Kalau tahu metode Keyword-based itu lemah, kenapa tidak langsung pakai Semantic Search?

**Jawaban (BLUF):**  
"Karena pendekatan Keyword-based adalah solusi yang paling efisien untuk membangun Minimum Viable Product dalam waktu kurang dari 3 bulan."

**Penjelasan:**  
"Untuk tahap awal, ini sudah cukup membuktikan bahwa arsitektur RAG kami berfungsi. Namun, ini sudah masuk dalam prioritas rekomendasi pengembangan kami ke depan. Kami akan mengimplementasikan Vector Embedding agar pencarian didasarkan pada makna (Semantic), bukan sekadar kecocokan huruf."

---
#
- Keyword-based (Yang kami pakai sekarang): Sistem mencari huruf yang persis sama. Kelemahannya, kalau mahasiswa ngetik 'Apa itu kunci utama?', tapi di modul tertulisnya 'Primary Key', sistem bisa gagal menemukan jawabannya.

- Vector Embedding & Semantic Search (Target kami ke depan): Teks diubah menjadi angka matematika yang membaca makna. Jadi AI akan tahu bahwa 'Kunci Utama' dan 'Primary Key' itu maknanya sama persis, sehingga hasil pencarian tetap akurat meskipun kata-katanya berbeda."