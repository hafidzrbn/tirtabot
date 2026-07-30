# Prompt Lengkap — Desain & Build "TirtaBot" (UI/UX + Jalur Eksekusi + Hosting)

> Prompt ini ditujukan untuk AI code generator (mis. Claude Code) yang akan membangun frontend `index.html` (HTML5 + Tailwind CSS + Vanilla JS) yang terhubung ke backend RAG Python (`server.py`). Sertakan juga gambar referensi desain (screenshot "ChatEase") saat menjalankan prompt ini bila memungkinkan — pola visualnya juga sudah dijabarkan dalam teks di Bagian 9, supaya prompt ini tetap lengkap dipakai meski gambar tidak ikut ter-attach.

---

## 1. Konteks & Peran AI

Buatkan desain UI/UX untuk aplikasi web AI chatbot bernama **"TirtaBot"** — asisten AI yang membantu pengguna mengetahui bagaimana kecenderungan respons, opini, serta sentimen masyarakat terhadap dr. Tirta Mandira Hudhi dalam berbagai isu: kesehatan, bisnis sepatu lokal, kebijakan, profesi dokter, maupun personal.

Gaya visual: **modern, clean, dan friendly**, terinspirasi dari ChatGPT.

---

## 2. Jalur Eksekusi (Ditetapkan — Wajib Diikuti)

**Modern Single-Page App: HTML5 + Tailwind CSS + Vanilla JS + Python Server** ⭐⭐⭐⭐⭐ *(Sangat Direkomendasikan)*

**Cara kerja:**
- Buat satu file `index.html` berbasis **Tailwind CSS** + **Lucide Icons** + **JavaScript murni (vanilla)**, dibuat rapi dan presisi 100% sesuai spesifikasi UI/UX pada prompt ini (gaya ChatGPT).
- Hubungkan frontend tersebut dengan `server.py` (**FastAPI** atau **Flask**) yang menjalankan proses RAG: **FAISS** (vector search) + **Groq API** (LLM inference).
- Komunikasi frontend ↔ backend murni lewat REST API (`fetch`), tanpa reload halaman (SPA experience).

**Keunggulan jalur ini:**
- Paling cepat selesai dibanding setup React/Next.js penuh.
- 100% dinamis, tanpa reload halaman.
- Tampilan bisa pixel-perfect mengikuti prompt UI/UX — tidak dibatasi component library pihak ketiga.
- Sangat mudah dijalankan secara lokal maupun di-deploy (satu server Python cukup untuk melayani frontend statis + API backend sekaligus).

> ⚠️ **Penyesuaian penting:** Karena jalur eksekusi ini **tidak memakai React**, seluruh referensi ke *shadcn/ui* dan *Recharts* pada bagian teknis asli digantikan alternatif vanilla-JS yang setara — lihat Bagian 3.

---

## 3. Arsitektur Teknis

| Layer | Teknologi |
|---|---|
| Struktur halaman | HTML5 semantik — satu file `index.html` |
| Styling | Tailwind CSS |
| Ikon | Lucide Icons versi statis/CDN (bukan `lucide-react`) |
| Interaktivitas | Vanilla JavaScript (ES6+) + `fetch` API |
| Visualisasi sentimen | **Chart.js** (native JS — pengganti Recharts yang berbasis React) |
| Komponen dasar | Dibangun manual dengan Tailwind (button, card, input) — *shadcn/ui tidak dipakai karena berbasis React* |
| Backend | Python — **FastAPI** (disarankan) atau Flask |
| RAG engine | **FAISS** (vector store) + **Groq API** (LLM) |
| Serving | `server.py` men-serve file statis frontend sekaligus endpoint API dalam satu proses (same-origin, tanpa perlu konfigurasi CORS) |

---

## 4. Rencana Hosting & Deployment

**Platform: HuggingFace Spaces** *(Rekomendasi Utama & Paling Praktis)* ⭐⭐⭐⭐⭐

- **Biaya:** Gratis (CPU Basic — 2 vCPU & 16GB RAM pada tier default, sesuai dokumentasi resmi HuggingFace).
- **Alasan pemilihan:**
  - Mendukung *FastAPI/Python Docker Space* secara native.
  - Frontend (HTML + Tailwind CSS) dan backend RAG Python bisa disatukan dalam **satu Space** yang sama — tidak perlu hosting terpisah.
  - Cukup unggah berkas proyek satu kali, web langsung aktif.
  - Platform yang dikenal luas sebagai standar AI dunia — nilai plus untuk konteks akademik.
- **Format URL:** `https://huggingface.co/spaces/<username-anda>/tirtabot-ai`
- *Catatan:* kuota/harga tier gratis HuggingFace bisa berubah sewaktu-waktu — cek `huggingface.co/pricing` sesaat sebelum deploy untuk memastikan spesifikasi terbaru.

---

## 5. Struktur Layout (Desktop, 3 Kolom, Full Height)

1. **Sidebar kiri** (±260px) — navigasi & branding
2. **Area chat utama** (fleksibel, paling lebar) — percakapan & hasil analisis
3. **Panel riwayat kanan** (±300px) — daftar riwayat analisis

---

## 6. Design System

| Elemen | Spesifikasi |
|---|---|
| Warna aksen utama | Gradasi biru-teal `#0EA5B7` → `#2E9BE6` — untuk link, tombol utama, ikon aktif |
| Background sidebar & panel kanan | Putih/off-white (`#FFFFFF`–`#FAFAFA`) |
| Background area chat | Gradient lembut `#F4F9FC` → `#EAF3FB` (putih-kebiruan ke biru muda pucat) |
| Teks utama | Abu gelap `#1E1E2D` |
| Teks sekunder | Abu `#8B8B9A` |
| Border-radius | Card 16–20px · tombol pill full-rounded · chart card 12–16px |
| Shadow | Lembut — pada card, input bar, tombol mengambang |
| Font | Sans-serif modern (Inter / Poppins / SF Pro) — bold untuk heading, regular untuk body |
| Ikon | Outline minimal (Lucide Icons); pakai ikon chart/analytics untuk elemen terkait data |

---

## 7. Detail Komponen

### 7.1 Sidebar Kiri
- **Logo:** gunakan file `logo dokter tirta.png` (lihat catatan di bawah) + teks **"TirtaBot"** (bold) di sebelahnya.
- **Tombol "+ Chat Baru"** — biru, menonjol, tepat di bawah logo.
- **Menu navigasi vertikal:**
  - Template Pertanyaan — kumpulan contoh pertanyaan.
- **Kartu penjelasan TirtaBot** menempel di bagian bawah sidebar:
  - Background gradient biru-teal.
  - Judul **"TirtaBot"** (putih, bold).
  - Sub-teks: *"Asisten AI yang siap membantumu mengetahui bagaimana kecenderungan respon, opini, serta sentimen masyarakat terhadap dr. Tirta Mandira Hudhi dalam berbagai isu"* — ditampilkan dalam chip/badge putih dengan teks biru.

> 📁 **Catatan logo:** Path `C:\Users\Hafidz\Downloads\UAS TRENDING TOPIC ON STATISTICS\logo dokter tirta.png` adalah path lokal di komputer Anda dan tidak akan terbaca oleh server atau AI code generator manapun. Saat implementasi, salin file logo ke folder assets proyek (mis. `/assets/logo-tirta.png`) lalu gunakan path relatif tersebut di `index.html`.

### 7.2 Area Chat Utama
- **Header:** judul chat (contoh: *"Halo! Saya TirtaBot 👋"*).
- **Input bar** (card mengambang, putih, shadow lembut):
  - Baris tombol *pill* quick-action.
  - Baris input: ikon attachment (upload artikel/screenshot) + microphone di kiri → placeholder *"Tanyakan isu/topik tentang dr. Tirta di sini..."* → tombol send bulat biru + ikon paper-plane di kanan.
- **Bubble AI:** teks polos tanpa background, rata kiri.
- **Bubble user:** card abu muda rounded dengan shadow, rata kanan, disertai avatar kecil.

### 7.3 Panel Kanan — Riwayat Analisis
- Judul **"Riwayat Analisis"** (bold, besar).
- List item riwayat (scrollable), tiap item terdiri dari:
  - Ikon folder/dokumen kecil.
  - Judul analisis (bold, truncate).
  - Preview pertanyaan awal (abu-abu, truncate).
  - *(Opsional)* dot kecil berwarna menandakan sentimen dominan (mis. hijau = positif, merah = negatif, kuning = netral/campuran).
- **Tombol "Hapus Riwayat"** (ikon trash, teks merah, background putih) di bagian bawah panel.

---

## 8. Interaksi & Responsivitas
- Hover state lembut pada semua nav item & history item.
- Sidebar & panel kanan collapsible di layar sempit; mobile → drawer/overlay via hamburger.
- Input field auto-expand untuk teks panjang.
- Typing/loading indicator saat AI memproses & mengambil data (mis. saat backend memanggil FAISS + Groq API).
- Transisi smooth (200–300ms ease) untuk hover/klik.

---

## 9. Referensi Desain Visual

Ikuti pola tata letak dan gaya komponen pada gambar referensi (screenshot aplikasi "ChatEase") berikut — sesuaikan warna & konten dengan branding TirtaBot pada Bagian 6:

- **Sidebar:** badge logo bulat + nama app tebal di kiri atas; tombol "+ New chat" / "+ Chat Baru" berupa teks biru tebal (bukan tombol solid berwarna penuh); nav list ikon + label dengan spacing longgar; kartu promosi gradient di bagian bawah sidebar (judul + deskripsi + tombol pill); "Log out" polos di paling bawah.
- **Header chat:** judul besar di kiri; kumpulan tombol aksi (share pill-button, bookmark, more/ellipsis) rounded dengan shadow tipis di kanan.
- **Pesan AI:** teks polos rata kiri tanpa bubble; dapat menyisipkan grid kartu hasil (untuk TirtaBot berupa kartu ringkasan sentimen/chart, bukan foto).
- **Pesan user:** bubble abu muda rounded dengan shadow, rata kanan, avatar kecil di sampingnya.
- **Input bar mengambang:** card putih rounded dengan shadow; baris pill quick-action di atas; baris input (attachment + mic di kiri, placeholder di tengah, tombol send bulat biru di kanan) di bawah.
- **Panel kanan:** judul besar di atas; list item dengan ikon folder + judul tebal + preview abu-abu; spacing antar-item cukup lega agar mudah di-scan.

> **Catatan warna:** latar pada gambar referensi bernuansa pastel ungu-pink-biru. Untuk TirtaBot, tetap gunakan skema warna pada Bagian 6 (`#F4F9FC → #EAF3FB`) — yang diadaptasi dari gambar referensi adalah **pola layout & gaya komponennya**, bukan warna secara literal.
