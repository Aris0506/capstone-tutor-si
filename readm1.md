# 🎯 1. “Jelaskan sistem kamu” (BLUF style)

“Sistem yang saya buat adalah chatbot berbasis RAG menggunakan Streamlit untuk membantu pengguna mendapatkan jawaban dari dokumen pembelajaran secara relevan.”

Secara alur, user memasukkan pertanyaan melalui web, kemudian sistem melakukan pencarian informasi dari dokumen menggunakan keyword-based retrieval.

Hasil pencarian tersebut dimasukkan ke dalam prompt dan diproses oleh model bahasa untuk menghasilkan jawaban, yang kemudian ditampilkan kembali ke pengguna.

sehingga Pendekatan ini memastikan jawaban tidak hanya dihasilkan oleh model, tetapi juga berdasarkan referensi dari dokumen.

💥 Keren, singkat, langsung kena.

# 🎯 2. “Kenapa pakai RAG?” (BLUF style)

“Saya menggunakan RAG untuk meningkatkan akurasi jawaban dengan memanfaatkan konteks dari dokumen.”

Tanpa RAG, model bahasa berpotensi memberikan jawaban yang tidak sesuai atau di luar konteks.

Dengan RAG, sistem mengambil referensi langsung dari sumber yang relevan sehingga jawaban lebih terkontrol dan sesuai kebutuhan pembelajaran.

# “Kelemahan sistem kamu?”

“Kelemahan utama sistem ini ada pada metode retrieval yang masih sederhana.”

Saat ini masih menggunakan keyword-based, sehingga belum sepenuhnya memahami konteks semantik.

Ke depan bisa dikembangkan menggunakan vector embedding dan semantic search.

# “Kenapa Anda masih menggunakan keyword-based retrieval, bukan semantic search?”
“Saya menggunakan keyword-based retrieval karena fokus pengembangan sistem ini masih pada tahap minimum viable product atau prototype.”

Dengan keterbatasan waktu pengembangan sekitar tiga bulan, pendekatan ini dipilih karena lebih sederhana dan cepat untuk diimplementasikan.

Meskipun demikian, keterbatasan metode ini sudah kami identifikasi dan menjadi bagian dari rencana pengembangan selanjutnya, khususnya dengan penerapan semantic search berbasis vector embedding.

Karena semantic search mampu memahami konteks makna, bukan hanya kecocokan kata, sehingga hasil retrieval lebih relevan.

# Bagaimana sistem Anda memastikan bahwa jawaban yang dihasilkan itu relevan dan tidak menyimpang?
“Sistem memastikan relevansi jawaban melalui kombinasi proses retrieval dan pengaturan system prompt.”

Pertama, sistem mengambil konteks yang relevan dari dokumen menggunakan metode retrieval, sehingga model memiliki referensi yang sesuai.

Kedua, system prompt digunakan untuk memberikan batasan agar model hanya menjawab berdasarkan konteks tersebut dan tidak keluar dari topik.

Dengan pendekatan ini, jawaban yang dihasilkan menjadi lebih terarah dan tidak menyimpang.

Kemungkinan kesalahan tetap ada, terutama jika konteks yang diambil kurang relevan. Oleh karena itu, peningkatan kualitas retrieval menjadi fokus pengembangan selanjutnya.

# “Apa kelebihan utama sistem Anda dibanding chatbot biasa?”
Kelebihan utama sistem ini adalah kemampuannya menghasilkan jawaban yang lebih terkontrol dan berbasis konteks.”

Berbeda dengan chatbot biasa yang hanya mengandalkan model bahasa, sistem ini menggunakan pendekatan RAG sehingga jawaban didasarkan pada dokumen yang relevan.

Dengan membatasi referensi pada konteks tertentu, sistem dapat mengurangi risiko halusinasi dan meningkatkan relevansi jawaban.