---
title: TirtaBot AI Chatbot
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🩺 TirtaBot - Asisten AI Sentimen & Opini Publik dr. Tirta

TirtaBot adalah aplikasi web AI Chatbot interaktif (gaya ChatGPT) berbasis **HTML5 + Tailwind CSS + Vanilla JS + FastAPI + FAISS Vector Search + Groq LLM API (`llama-3.3-70b-versatile`)**.

## 📊 Kapabilitas & Objek Analisis
- Memilih & menganalisis **24.325 komentar masyarakat** dari 10 video YouTube populer tentang **dr. Tirta Mandira Hudhi, Sp.B**.
- Mengukur rasio sentimen (*Positif / Netral / Negatif*) dari dokumen rujukan.
- Mengirimkan dokumen rujukan hasil *Dynamic Threshold FAISS Search* ke **Groq LLM API** untuk merangkum ringkasan kecenderungan opini publik secara akurat dan bebas halusinasis.
- Menampilkan rujukan sitasi komentar asli lengkap dengan link URL video YouTube, nama author, dan jumlah likes.

## 🚀 Cara Menjalankan Secara Lokal
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan FastAPI Uvicorn Server
python server.py
# Atau: uvicorn server:app --host 0.0.0.0 --port 7860 --reload
```
Akses di browser pada: `http://localhost:7860`
