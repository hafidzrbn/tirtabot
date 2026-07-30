# 🩺 TirtaBot AI — Asisten Intelligent RAG & Analisis Sentimen Publik dr. Tirta

> **Laporan & Prototipe Ujian Akhir Semester (UAS) Genap TA 2025/2026**  
> **Mata Kuliah**: Trending Topics on Statistics (TToS)  
> **Dosen Penguji**: Dr. RB Fajriya Hakim, M.Si.  
> **Penyusun**: Muhammad Hafidz Rabbaanii Sulthon (**NIM: 23611091**)  
> **Institusi**: Jurusan Statistika, Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Islam Indonesia (UII), Yogyakarta  

---

## 🌐 Akses Prototipe Publik & Repositori

* **Link Web Application (Streamlit Cloud)**: [https://tirtabot.streamlit.app](https://tirtabot.streamlit.app)
* **Link Repository GitHub**: [https://github.com/hafidzrbn/tirtabot](https://github.com/hafidzrbn/tirtabot)

---

## 📌 Deskripsi Proyek

**TirtaBot** adalah sistem analisis data teks cerdas dan prototipe chatbot berbasis *Retrieval-Augmented Generation* (RAG) yang mengombinasikan **Eksplorasi Statistik Teks**, **Pemodelan AI Klasifikasi Sentimen Komparatif** (*Logistic Regression*, *Support Vector Machine*, dan *IndoBERT Transformer*), serta **Dynamic Similarity Threshold FAISS Vector Store** yang disintesis secara cerdas menggunakan **Groq LLM API (`llama-3.3-70b-versatile`)**.

Sistem ini mengekstrak dan menganalisis **24.325 komentar publik YouTube** dari 10 video populer dr. Tirta Mandira Hudhi, Sp.B. (mencakup topik *Edukasi Kesehatan*, *Review Sepatu Lari Lokal #Tirtalokal*, *Realitas Profesi Dokter*, *Opini Podcast*, dan *Perubahan Personal*).

---

## 📁 Struktur Berkas Utama

Repositori ini telah dirapikan secara khusus dan berfokus pada **6 berkas Python paling krusial** yang mendukung seluruh alur analisis:

| No | Berkas Source Code | Deskripsi & Peran Krusial | Subbab UAS |
| :---: | :--- | :--- | :---: |
| 1 | `scrape_comments.py` | Otomatisasi akuisisi data 24.325 komentar YouTube dari 10 video dr. Tirta via API downloader. | Soal No. 1 |
| 2 | `eda_preprocessing.py` | Pipeline prapemrosesan teks: *case folding*, cleaning, normalisasi kata *slang*, **penanganan negasi** (`tidak_bagus`), & *stopwords*. | Soal No. 2 |
| 3 | `text_exploration.py` | Ekstraksi frekuensi kata utama, top N-Gram (Bigram & Trigram), matriks TF-IDF, serta visualisasi *Word Cloud* dan *Network Graph*. | Soal No. 3 |
| 4 | `ai_modeling.py` | Benchmarking 3 arsitektur model AI (*Logistic Regression*, *SVM*, dan *IndoBERT Transformer*) serta pembuat *Confusion Matrix*. | Soal No. 4 |
| 5 | `rag_system.py` | Core engine RAG yang menggabungkan *Dynamic Threshold FAISS Vector Search* ($\ge 0.12$) dengan *Groq LLM API* (`llama-3.3-70b-versatile`). | Soal No. 5 |
| 6 | `app.py` | Berkas aplikasi web interaktif berbasis Streamlit (gaya ChatGPT UI 3-kolom) yang di-deploy publik ke Streamlit Community Cloud. | Soal No. 7 |

---

## 📊 Ringkasan Hasil Evaluasi Model AI

Pengujian dilakukan dengan pembagian dataset 80% Data Latih (Train = 17.584) dan 20% Data Uji (Test = 4.396):

| No | Model Klasifikasi AI | Accuracy | Precision | Recall | **F1-Score** | Status / Peran |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | **Logistic Regression (Baseline)** | 74,61% | 74,65% | 74,61% | **74,55%** | Baseline Model |
| 2 | **Support Vector Machine (SVM)** | 74,75% | 74,72% | 74,75% | **74,70%** | Comparison ML Model |
| 3 | **IndoBERT Transformer (SOTA)** | **94,20%** | **94,35%** | **94,20%** | **94,25%** | **SOTA Model (Terbaik)** |

---

## ⚡ Cara Menjalankan Aplikasi Secara Lokal

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/hafidzrbn/tirtabot.git
   cd tirtabot
   ```

2. **Install Dependensi Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi Web Streamlit**:
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan secara otomatis terbuka pada peramban Anda di alamat `http://localhost:8501`.

---
*Laporan dan repositori ini disusun secara komprehensif untuk memenuhi syarat Ujian Akhir Semester TToS Juli 2026.*

