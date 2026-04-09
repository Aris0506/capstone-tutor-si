# Gambaran Besar

RAG  3 komponen utama:
- Retrieval → ambil konteks dari dokumen
- Augmentation → masukin konteks ke prompt
- Generation → LLM jawab


. ❓ “Apa itu RAG?”

👉 Jawaban santai tapi cerdas:

RAG adalah metode yang menggabungkan proses pencarian informasi (retrieval) dari knowledge base dengan kemampuan generasi jawaban dari model bahasa. Jadi sistem tidak hanya mengandalkan model AI, tetapi juga menggunakan konteks dari dokumen agar jawaban lebih relevan.

# 2. ❓ “Kenapa pakai RAG?”

Karena model bahasa murni berpotensi menghasilkan jawaban yang tidak akurat atau di luar konteks. Dengan RAG, sistem mengambil referensi langsung dari materi kuliah, sehingga jawaban lebih terkontrol dan sesuai kebutuhan akademik.

# 3. ❓ “Retrieval kamu pakai apa?”

Saat ini masih menggunakan pendekatan berbasis kata kunci (keyword-based) dengan perhitungan skor sederhana. Namun ke depan bisa dikembangkan menggunakan vector embedding dan semantic search untuk meningkatkan akurasi.

💥 ini jawaban aman + keliatan ngerti roadmap

# 4. ❓ “Kenapa pakai Streamlit?”

Karena Streamlit memungkinkan pengembangan aplikasi web secara cepat dan langsung terintegrasi dengan Python, sehingga cocok untuk fokus pada pengembangan sistem AI tanpa perlu kompleksitas front-end.

# 5. ❓ “Kelemahan sistem kamu?”

Keterbatasan utama saat ini adalah metode retrieval yang masih sederhana dan ketergantungan pada kualitas dokumen. Selain itu, sistem masih stateless dan belum menyimpan riwayat percakapan secara permanen.

💥 ini penting banget—jangan bilang “tidak ada kelemahan” ❌