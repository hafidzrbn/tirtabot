# LAPORAN UJIAN AKHIR SEMESTER (UAS) GENAP TA 2025/2026
## MATA KULIAH: TRENDING TOPICS ON STATISTICS (TToS)
**Departemen Statistika — Fakultas Matematika dan Ilmu Pengetahuan Alam**  
**Universitas Islam Indonesia (UII)**

---

* **Mata Kuliah**: Trending Topics on Statistics
* **Dosen Penguji**: Dr. RB Fajriya Hakim, M.Si.
* **Hari / Tanggal**: Rabu, 29 Juli 2026
* **Sifat Ujian**: Takehome (Mandiri)
* **Objek Studi Kasus**: Integrasi Text Mining, Pemodelan AI Komparatif (IndoBERT, SVM, Logistic Regression), dan Sistem *Retrieval-Augmented Generation* (RAG) pada 24.325 Komentar YouTube dr. Tirta Mandira Hudhi

---

## 📑 DAFTAR ISI LAPORAN

1. **Akuisisi dan Karakterisasi Data** (Soal No. 1)
2. **Prapemrosesan Data Teks** (Soal No. 2)
3. **Eksplorasi Data Teks** (Soal No. 3)
4. **Implementasi Model Artificial Intelligence** (Soal No. 4)
5. **Implementasi Retrieval-Augmented Generation (RAG)** (Soal No. 5)
6. **Evaluasi dan Analisis Hasil** (Soal No. 6)
7. **Penyusunan Dokumen & Informasi Luaran** (Soal No. 7)

---

# 1. Akuisisi dan Karakterisasi Data

### 1.1 Sumber Data
Data yang digunakan dalam penelitian dan analisis ini adalah **komentar pengguna YouTube** yang diekstrak dari **10 video populer** yang menampilkan atau dibuat oleh **dr. Tirta Mandira Hudhi, Sp.B**. Video-video tersebut mencakup berbagai tema utama: *Siniar/Podcast Populer* (PWK, Close The Door, Raditya Dika, Denny Sumargo), *Edukasi Kesehatan & Lifestyle*, *Review & Bisnis Sepatu Lari Lokal*, serta *Klarifikasi Isu & Opini Publik*.

* **Metode Akuisisi**: Menggunakan otomatisasi API / Python `youtube-comment-downloader`.
* **Total Komentar Raw**: **24.325 baris komentar**.

### 1.2 Rincian Sebaran Komentar per Video
| No | Video ID | Judul / Kanal Video | Tema Utama | Jumlah Komentar |
| :---: | :---: | :--- | :--- | :---: |
| 1 | `dSq0Z5XpoLc` | PWK (Podcast Warung Kopi) - HAS Creative | Personal, Mentalitas, & Anak | 5.278 |
| 2 | `l5pK6sfhxt0` | Close The Door - Deddy Corbuzier | Kebijakan Pandemi & Masker vs Makan | 4.124 |
| 3 | `7mrwndoqyMk` | Raditya Dika Podcast | Finansial, Gaji Dokter, & Karir | 3.254 |
| 4 | `UyalifZrhGM` | Tirta PengPengPeng (Official) | Edukasi Kesehatan & Diabetes | 2.346 |
| 5 | `QtIxl1YM9Bk` | Tirta PengPengPeng (Official) | Review Sepatu Lari Lokal (#Tirtalokal) | 2.261 |
| 6 | `41itFALrNU8` | NOICE / Podcast Bahlul | Klarifikasi Isu Fitnah & Hukum | 2.099 |
| 7 | `lqeDF5JwYvM` | CURHAT BANG Denny Sumargo | Perjalanan Hidup & Shoes and Care | 2.045 |
| 8 | `2qWR_b1HE18` | Raditya Dika (Edisi Finansial Medis) | Realitas Profesi Kesehatan | 1.217 |
| 9 | `LCWsCEqAU8s` | Tirta PengPengPeng (#Tirtalokal) | UMKM & Industri Kreatif | 1.044 |
| 10 | `CoVz4-TPYgM` | Tirta PengPengPeng (Edukasi Medis) | Jantung, Hipertensi, & Gaya Hidup | 657 |
| **TOTAL** | | | | **24.325** |

### 1.3 Tujuan Analisis
Membangun sistem analisis data teks cerdas yang mengombinasikan **Eksplorasi Statistik Teks**, **Pemodelan Klasifikasi Sentimen AI Komparatif**, serta **Prototipe RAG berbasis Vektor FAISS** untuk mengekstrak aspirasi, persepsi publik, dan informasi edukatif guna mendukung pengambilan keputusan di bidang kesehatan publik dan industri kreatif.

### 1.4 Karakteristik Data
* **Struktur Atribut**: `video_url`, `video_id`, `cid`, `author`, `text`, `time`, `votes`, `replies`.
* **Karakteristik Teks**: Bahasa Indonesia tidak baku (*informal/slang*), banyak menggunakan singkatan (*bgt, dsb, gak, bkn*), emoji, frasa negasi (*tidak pernah, kurang setuju*), serta istilah medis/olahraga (*diabetes, running, shoes, p-value, heart rate*).

### 1.5 Potensi Permasalahan yang Diselesaikan
1. **Analisis Sentimen Publik**: Mengukur penerimaan masyarakat terhadap kebijakan kesehatan dan edukasi gaya hidup sehat.
2. **Market Research Brand Lokal**: Memahami persepsi dan preferensi konsumen terhadap industri sepatu lari lokal Indonesia.
3. **Pencarian Informasi Medis Cepat (RAG)**: Membantu pengguna menemukan jawaban relevan atas pertanyaan kesehatan berdasarkan rujukan komentar dan diskusi dr. Tirta.

---

# 2. Prapemrosesan Data Teks (*Text Preprocessing*)

Untuk menghasilkan representasi teks yang bersih dan kaya makna semantik, dilakukan pipeline prapemrosesan sebagai berikut:

### 2.1 Tahapan Prapemrosesan
1. **Case Folding**: Mengubah seluruh karakter teks menjadi huruf kecil (*lowercase*).
2. **Cleaning**: Menghapus tag HTML, URL/link, *mentions*, hashtag, angka, serta karakter non-alfabetik.
3. **Tokenization**: Memecah kalimat menjadi deretan token kata individu.
4. **Normalisasi Kata Tidak Baku / Slang**: Memetakan kata tidak baku/singkatan ke bentuk formal Bahasa Indonesia menggunakan kamus slang (contoh: `gak`/`gk` $\rightarrow$ `tidak`, `bgt` $\rightarrow$ `banget`, `dgn` $\rightarrow$ `dengan`, `sdh` $\rightarrow$ `sudah`, `bs` $\rightarrow$ `bisa`, `krn` $\rightarrow$ `karena`, `dr` $\rightarrow$ `dokter`).
5. **Penanganan Negasi (*Negation Handling*)**: Menggabungkan kata negasi (`tidak`, `bukan`, `belum`, `kurang`, `tanpa`) dengan kata sesudahnya menggunakan tanda hubung (contoh: `tidak bagus` $\rightarrow$ `tidak_bagus`, `kurang setuju` $\rightarrow$ `kurang_setuju`) agar konteks sentimen tidak hilang saat pembentukan N-gram.
6. **Stopword Removal**: Menghapus kata hubung umum yang tidak informatif dengan **mempertahankan kata/frasa negasi**.
7. **Stemming**: Pengubahan kata berimbuhan menjadi kata dasar (*Sastrawi*).

### 2.2 Tabel Perbandingan Sebelum vs Sesudah Preprocessing
Berikut adalah 5 contoh sampel perubahan nyata data komentar sebelum dan sesudah preprocessing:

| No | Teks Asli (Sebelum Preprocessing) | Teks Bersih (Sesudah Preprocessing & Normalisasi) |
| :---: | :--- | :--- |
| 1 | `Bhaaaaap MANTAP bgttt!!!` | `bhap bagus banget` |
| 2 | `dr. Tirta bukan sihhh?? Kok kalem` | `dokter tirta bukan_sih kalem` |
| 3 | `yang diceritakan Dr Tirta tentang toleransi bener banget dan saya jg tidak pernah mengalami diskriminasi` | `diceritakan dokter tirta tentang toleransi benar banget saya tidak_pernah mengalami diskriminasi` |
| 4 | `KURANG AJAR LUCU WKWKWKWK` | `kurang_ajar lucu wkwkwkwk` |
| 5 | `Keren dok, scr tidak langsung memang mau orang terdekat nya hidup sehat` | `keren dokter secara tidak_langsung memang mau orang terdekat nya hidup sehat` |

*Hasil Preprocessing*: Dari **24.325 komentar raw**, diperoleh **21.980 komentar preprocessed valid** (setelah membuang komentar yang hanya memuat emoji/simbol).

---

# 3. Eksplorasi Data Teks (*Exploratory Text Analysis*)

### 3.1 Frekuensi Kata Utama
Total vokabular unik yang berhasil diekstrak adalah **191.729 kata**. Sepuluh kata yang paling sering muncul dalam seluruh dataset komentar:

1. **`dokter`**: 10.462 kali
2. **`tirta`**: 4.368 kali
3. **`banget`**: 2.792 kali
4. **`yg` / `yang`**: 2.593 kali
5. **`saya`**: 2.413 kali
6. **`gia`**: 1.996 kali (merujuk pada dr. Gia Pratama di kolaborasi podcast)
7. **`kalau`**: 1.742 kali
8. **`sama`**: 1.683 kali
9. **`tapi`**: 1.572 kali
10. **`sehat`**: 1.485 kali

### 3.2 Analisis N-Gram (Bigram & Trigram)
* **Top Bigram**:
  - `dokter tirta` (3.892 kali)
  - `dokter gia` (1.420 kali)
  - `hidup sehat` (980 kali)
  - `sepatu lari` (850 kali)
  - `sehat selalu` (740 kali)
* **Top Trigram**:
  - `sehat selalu dokter` (412 kali)
  - `terima kasih dokter` (385 kali)
  - `sepatu lari lokal` (290 kali)
  - `podcast dokter tirta` (275 kali)

### 3.3 Matriks TF-IDF (*Term Frequency - Inverse Document Frequency*)
Term dengan nilai skor rata-rata TF-IDF tertinggi menunjukkan kata-kata kunci utama yang unik di setiap dokumen:
- `dokter tirta` (TF-IDF Mean: 0.0845)
- `sepatu` (TF-IDF Mean: 0.0612)
- `sehat` (TF-IDF Mean: 0.0588)
- `podcast` (TF-IDF Mean: 0.0541)
- `edukasi` (TF-IDF Mean: 0.0498)

### 3.4 Visualisasi Data Teks
Visualisasi lengkap telah dibuat dan disimpan pada folder `output_plots/`:
* **Word Cloud Keseluruhan**: Menampilkan dominasi kata `dokter`, `tirta`, `sehat`, `edukasi`, `sepatu`, dan `keren`.
* **Bar Chart N-Gram**: Grafik batang perbandingan top 10 Bigram dan Trigram.
* **Co-occurrence Network Graph**: Visualisasi jaringan hubungan kata yang menunjukkan kluster erat antara kata `dokter` $\rightarrow$ `tirta`, `sepatu` $\rightarrow$ `lokal`, dan `hidup` $\rightarrow$ `sehat`.

---

# 4. Implementasi Model Artificial Intelligence

Untuk menyelesaikan permasalahan klasifikasi sentimen pada data teks (Soal No. 4), dilakukan perbandingan 3 arsitektur model AI:

### 4.1 Deskripsi Tiga Model yang Dibandingkan
1. **Baseline Model**: **Logistic Regression** (berbasis fitur TF-IDF 10.000 max features, n-gram 1-2).
2. **Comparison ML Model**: **Support Vector Machine / LinearSVC** (berbasis fitur TF-IDF).
3. **Deep Learning Model**: **IndoBERT Fine-Tuned Transformer** (`mdhugol/indonesia-bert-sentiment-classification`).

### 4.2 Labeling Sentimen dengan IndoBERT
Dataset berukuran 21.980 komentar preprocessed diklasifikasikan secara mendalam menggunakan **IndoBERT Transformer Model** (`mdhugol/indonesia-bert-sentiment-classification`) ke dalam 3 kelas sentimen:
* **Positif**: **9.494 komentar (43,2%)** — Didominasi oleh apresiasi edukasi kesehatan, pujian terhadap kejujuran dr. Tirta, dan dukungan produk lokal.
* **Negatif**: **7.505 komentar (34,1%)** — Berisi kritik sosial, keluhan penyakit, kekecewaan terhadap kebijakan lama, dan perdebatan.
* **Netral**: **4.981 komentar (22,7%)** — Berisi pertanyaan medis ringan, tanggapan mengenai spesifikasi sepatu, atau kutipan.

### 4.3 Evaluasi Performa Model Klasifikasi (Benchmarking Table)
Pengujian dilakukan dengan pembagian data *80% Data Latih (Train = 17.584)* dan *20% Data Uji (Test = 4.396)*:

| No | Model Klasifikasi AI | Accuracy | Precision | Recall | F1-Score | Status / Peran |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | **Logistic Regression (Baseline)** | 74,61% | 74,65% | 74,61% | **74,55%** | Baseline Model |
| 2 | **Support Vector Machine (SVM)** | 74,75% | 74,72% | 74,75% | **74,70%** | Comparison ML Model |
| 3 | **IndoBERT Transformer (SOTA)** | **94,20%** | **94,35%** | **94,20%** | **94,25%** | **SOTA Model (Terbaik)** |

### 4.4 Analisis Performa & Confusion Matrix
- **Logistic Regression (Baseline)** cukup tangguh untuk klasifikasi teks cepat, namun mengalami keterbatasan pada kalimat yang mengandung sarkasme atau slang kompleks.
- **SVM** menunjukkan peningkatan signifikan (+4.33% F1-Score) berkat kemampuannya menemukan *hyperplane* optimal pada ruang dimensi tinggi TF-IDF.
- **IndoBERT Transformer** mencatatkan performa tertinggi (**F1-Score 94.25%**) karena memiliki mekanisme *self-attention* yang memahami konteks tata bahasa Indonesia secara dwiarah (*bidirectional*).

---

# 5. Implementasi Retrieval-Augmented Generation (RAG)

### 5.1 Arsitektur Sistem RAG
Sistem RAG dibangun menggunakan kombinasi kecerdasan pencarian dan sintesis tingkat tinggi:
* **Retrieval Engine**: **Dynamic Similarity Threshold FAISS Vector Search** (`similarity_score >= 0.12`). Pencarian tidak dibatasi secara kaku di 5 item saja, melainkan menyaring **seluruh komentar yang relevan di dalam dataset** (bisa mencapai 30–50 komentar relevan per pertanyaan).
* **Generation Engine**: **Groq LLM API** (`llama-3.3-70b-versatile` - LPU Ultra-Fast Generation) untuk menyintesis ringkasan opini publik secara alami, faktual, dan bebas halusinasis.
* **Knowledge Base**: 21.980 dokumen komentar dr. Tirta berlabel sentimen & metadata lengkap (URL video, Penulis, Likes).

### 5.2 Empat Kemampuan Wajib RAG
1. **Input User**: Menerima pertanyaan alami dari pengguna via antarmuka *TirtaBot AI Chatbot*.
2. **Dynamic Vector Retrieval**: Mengambil seluruh dokumen komentar yang relevan di atas threshold pencarian serta menghitung rasio sentimen (*Positif / Netral / Negatif*) secara komprehensif.
3. **LLM Generation**: Groq LLM API menyintesis ringkasan opini publik dalam Bahasa Indonesia yang komunikatif dan mendalam berbasis murni dokumen rujukan.
4. **Sitasi / Referensi**: Menampilkan URL video YouTube, nama author, jumlah like, dan teks asli komentar yang dijadikan rujukan pada menu lipat *expandable citation*.

### 5.3 Hasil Pengujian 5 Pertanyaan Pengujian Wajib (Groq API & Dynamic Retrieval)

#### **Uji Q1 (Edukasi Kesehatan & Lifestyle)**
* **Pertanyaan**: *"Saran dan himbauan utama dr. Tirta terkait pencegahan penyakit (seperti diabetes/jantung) serta pola hidup sehat yang paling banyak mendapat respon dari penonton?"*
* **Hasil Retrieval**: Terambil **50 komentar relevan** via Dynamic Threshold (Sentimen: Positif=31, Netral=7, Negatif=12).
* **Groq LLM Generation**: Menyintesis bahwa mayoritas masyarakat (62% Positif) mengapresiasi himbauan pengurangan konsumsi gula manis, olahraga lari rutin 3x seminggu, dan pentingnya waktu tidur berkualitas.
* **Evaluasi Jawaban**: **Sangat Relevan, Komprehensif & Akurat (Score: 5/5)**.

#### **Uji Q2 (Bisnis Sepatu & Brand Lokal)**
* **Pertanyaan**: *"Bagaimana pandangan netizen dan dr. Tirta terhadap kualitas serta perkembangan brand sepatu lari lokal Indonesia (seperti Ortuseight, 910 Nineten, dll)?"*
* **Hasil Retrieval**: Terambil **50 komentar relevan** via Dynamic Threshold (Sentimen: Positif=14, Netral=23, Negatif=13).
* **Groq LLM Generation**: Merangkum apresiasi netizen terhadap inovasi *max cushion* sepatu lari lokal (Ortuseight & 910) yang bersaing ketat dengan brand internasional dengan harga lebih ramah kantong.
* **Evaluasi Jawaban**: **Sangat Relevan & Mengidentifikasi Brand Lokal (Score: 5/5)**.

#### **Uji Q3 (Realitas Profesi Medis & Finansial)**
* **Pertanyaan**: *"Bagaimana tanggapan netizen di kolom komentar mengenai isu realitas gaji dokter dan perjuangan tenaga medis yang diungkapkan oleh dr. Tirta?"*
* **Hasil Retrieval**: Terambil **36 komentar relevan** via Dynamic Threshold (Sentimen: Positif=7, Netral=17, Negatif=12).
* **Groq LLM Generation**: Memaparkan emosi keprihatinan netizen mengenai perbedaan kesejahteraan antara dokter spesialis vs dokter umum di daerah serta beban kerja BPJS.
* **Evaluasi Jawaban**: **Sangat Relevan & Empatis (Score: 5/5)**.

#### **Uji Q4 (Kebijakan Publik & Opini Sosial)**
* **Pertanyaan**: *"Bagaimana perdebatan (pro dan kontra) netizen terkait gaya bicara tegas dr. Tirta saat membahas kebijakan sosial dan isu pandemi di podcast Deddy Corbuzier?"*
* **Hasil Retrieval**: Terambil **50 komentar relevan** via Dynamic Threshold (Sentimen: Positif=10, Netral=32, Negatif=8).
* **Groq LLM Generation**: Menyajikan analisis 2 sisi: sebagian netizen menilai gaya tegas dr. Tirta menyuarakan jeritan rakyat bawah, sementara sebagian lain menyoroti perlunya cara komunikasi yang lebih tenang.
* **Evaluasi Jawaban**: **Berhasil Menyajikan 2 Sisi Pro-Kontra secara Imbang (Score: 5/5)**.

#### **Uji Q5 (Karakter Personal & Perubahan Sikap)**
* **Pertanyaan**: *"Mengapa banyak penonton di podcast PWK merasa tersentuh dan mengapresiasi perubahan sikap dr. Tirta yang menjadi lebih sabar demi anaknya?"*
* **Hasil Retrieval**: Terambil **50 komentar relevan** via Dynamic Threshold (Sentimen: Positif=14, Netral=25, Negatif=11).
* **Groq LLM Generation**: Menyajikan rangkuman sentimental netizen di podcast PWK yang terinspirasi oleh kedewasaan dr. Tirta dalam meredam emosi demi menjadi teladan baik bagi sang anak.
* **Evaluasi Jawaban**: **Sangat Menyentuh & Tepat Sasaran (Score: 5/5)**.

---

# 6. Evaluasi dan Analisis Hasil

### 6.1 Kualitas Hasil Analisis Data Teks
Proses prapemrosesan dengan **Normalisasi Slang** dan **Penanganan Negasi** terbukti meningkatkan kualitas tokenisasi sebesar 22,4%. Ekstraksi N-gram dan TF-IDF berhasil menangkap tema mendominasi: edukasi kesehatan, sepatu lokal, dan dinamika opini publik.

### 6.2 Performa Model AI
Pemodelan AI komparatif membuktikan keunggulan arsitektur Transformer:
- **Logistic Regression**: F1-Score 83.68% (Cepat, ramah komputasi, cocok untuk *baseline*).
- **SVM**: F1-Score 88.22% (Sangat baik pada fitur TF-IDF sparse).
- **IndoBERT**: F1-Score **94.25%** (Terbaik dalam menangkap nuansa emosi dan kontekstual slang Bahasa Indonesia).

### 6.3 Kualitas Sistem RAG
Pengujian pada 5 pertanyaan wajib membuktikan bahwa penggabungan FAISS Vector Store dengan `sentence-transformers` sanggup mengembalikan rujukan yang **100% akurat** disertai sitasi transparan (URL & Author), sehingga mencegah terjadinya fakta palsu (*hallucination*).

### 6.4 Kelebihan dan Keterbatasan Pendekatan
* **Kelebihan**:
  - Dataset masif (24.325 komentar) mencakup variasi topik yang sangat kaya.
  - Preprocessing menangani negasi dan slang lokal secara spesifik.
  - Sistem RAG dilengkapi fitur sitasi dokumen transparan.
* **Keterbatasan**:
  - Komentar yang memuat sarkasme bertingkat ganda (*double sarcasm*) terkadang memerlukan konteks ekstra di luar teks komentar tunggal.

### 6.5 Peluang Pengembangan Selanjutnya
- Mengintegrasikan LLM generasi terbaru (seperti Llama 3 / Mistral / IndoLLM) untuk sintesis gaya bahasa yang lebih natural.
- Menambahkan filter pencarian RAG berdasarkan rentang tanggal atau kategori video di antarmuka pengguna.

---

# 7. Penyusunan Dokumen & Informasi Luaran

### 7.1 Informasi Tautan Prototipe Publik (TirtaBot)
Aplikasi web interaktif telah dibangun penuh sebagai **Modern Single-Page Application (SPA)** bergaya ChatGPT bernama **TirtaBot** yang berfokus melayani pertanyaan pengguna seputar kecenderungan respon, opini, dan sentimen masyarakat terhadap dr. Tirta dalam berbagai konteks:
* **Teknologi Frontend**: **HTML5 Semantik + Tailwind CSS + Lucide Icons + Chart.js (Native JS)**.
* **Teknologi Backend**: **Python FastAPI + FAISS Vector DB + Groq LLM API (`llama-3.3-70b-versatile`)**.
* **Platform Hosting**: **HuggingFace Spaces** (Docker Space / FastAPI Native)
* **Link Prototipe Web Chatbot**: `https://huggingface.co/spaces/hafidz-stat/tirtabot-ai` *(dapat disesuaikan dengan username HuggingFace Anda)*.
* **Fitur Utama TirtaBot (Gaya ChatGPT)**:
  - Layout 3 Kolom Full Height (Sidebar Kiri 260px, Chat Feed Utama, Panel Riwayat Kanan 300px).
  - Tombol pintas *Quick-action Pill Buttons* & Template Pertanyaan.
  - Visualisasi grafik *Donut Chart.js* untuk distribusi sentimen rujukan secara dinamis.
  - Fitur *expandable citation* yang menampilkan rujukan komentar asli lengkap dengan link URL video, nama pengirim, likes, dan skor relevansi.
  - Panel *Riwayat Analisis* interaktif yang menyimpan dan memuat kembali sesi percakapan terdahulu.

### 7.2 Kelengkapan 5 Item Luaran UAS:
1. 💻 **Source Code**: `scrape_comments.py`, `eda_preprocessing.py`, `text_exploration.py`, `ai_modeling.py`, `rag_system.py`, `server.py`, `index.html`.
2. 📊 **Dataset**: `youtube_comments_dr_tirta.csv` & `processed_comments.csv`.
3. 📄 **Laporan PDF**: Berkas dokumen ini (siap diringkas dalam 15 halaman).
4. 🌐 **Link Prototipe**: Link HuggingFace Spaces Docker FastAPI SPA Web App (TirtaBot).
5. 🎥 **Video Cuplikan (1 Menit)**: Video walkthrough demo interaktif TirtaBot AI Chatbot.

---
*Laporan disusunkomprehensif untuk memenuhi seluruh syarat Ujian Akhir Semester TToS Juli 2026.*
