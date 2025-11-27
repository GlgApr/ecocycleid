# ♻️ EcoCycle ID

**EcoCycle ID** adalah platform pertukaran limbah organik hiper-lokal yang mengutamakan privasi, menghubungkan penyedia limbah (rumah tangga, restoran) dengan pencari limbah (peternak maggot, peternak unggas, pengompos).

Platform ini menggunakan **Artificial Intelligence (Google Gemini 2.5 Flash)** untuk menganalisis kualitas limbah secara otomatis dan **Location Jittering** untuk melindungi privasi lokasi pengguna.

---

## ✨ Fitur Utama

### 🧠 AI-Powered Analysis
- **Deteksi Otomatis:** Mengidentifikasi apakah gambar yang diunggah adalah limbah organik atau bukan.
- **Estimasi Berat:** Memperkirakan berat limbah (kg) berdasarkan visual.
- **Rekomendasi Pemanfaatan:** Memberikan saran penggunaan terbaik (misal: Pakan Maggot, Kompos, Pakan Ternak).
- **Peringatan Keamanan:** Mendeteksi kontaminan berbahaya (plastik, logam).

### 🔒 Privacy-First (Geospatial Protection)
- **Location Jittering:** Koordinat lokasi penyedia limbah diacak secara otomatis (±200m) sebelum ditampilkan di peta publik. Privasi rumah tangga tetap terjaga.

### 🗺️ Dual-Interface
- **Provider Interface (Streamlit):** Antarmuka sederhana untuk mengunggah foto limbah dan mendapatkan analisis AI instan.
- **Seeker Interface (React + Leaflet):** Peta interaktif untuk pencari limbah melihat ketersediaan stok di sekitar mereka dengan filter cerdas.

### 💬 Direct Social Transaction
- **WhatsApp Integration:** Tombol "Hubungi" yang langsung menghubungkan pencari dan penyedia via WhatsApp dengan pesan templat otomatis untuk negosiasi cepat.

---

## 🛠️ Tech Stack

### Backend & AI
- **Language:** Python 3.9+
- **API Framework:** FastAPI
- **AI Model:** Google Gemini 2.5 Flash (via Google Generative AI SDK)
- **Database:** SQLite
- **Image Processing:** Pillow

### Frontend (Provider/Admin)
- **Framework:** Streamlit
- **Mapping:** Folium, Streamlit-Folium

### Frontend (Seeker/Public)
- **Framework:** React 18 (TypeScript)
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Maps:** React Leaflet

---

## 📋 Prasyarat

Sebelum memulai, pastikan Anda telah menginstal:
1.  **Python 3.9** atau lebih baru.
2.  **Node.js** dan **npm** (untuk menjalankan frontend React).
3.  **Google Gemini API Key** (Dapatkan di [Google AI Studio](https://aistudio.google.com/)).

---

## 🚀 Panduan Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/glgapr/ecocycleid.git
cd ecocycleid
```

### 2. Setup Backend & Streamlit
Instal dependensi Python:
```bash
pip install -r requirements.txt
```

Konfigurasi API Key Gemini:
Buat file `.streamlit/secrets.toml` dan tambahkan API key Anda:
```toml
# .streamlit/secrets.toml
[gemini]
api_key = "MASUKKAN_API_KEY_GEMINI_ANDA_DISINI"
```

### 3. Setup Frontend (React)
Masuk ke direktori `ui` dan instal dependensi:
```bash
cd ui
npm install
cd ..
```

---

## ▶️ Cara Menjalankan Aplikasi

Sistem ini terdiri dari 3 komponen yang perlu dijalankan (idealnya di terminal terpisah):

### 1. Jalankan Aplikasi Provider (Streamlit)
Ini adalah tempat untuk **mengupload data sampah**.
```bash
streamlit run main.py
```
Akses di: `http://localhost:8501`

### 2. Jalankan Backend API (FastAPI)
Ini melayani data JSON untuk frontend React.
```bash
uvicorn api:app --reload --port 8000
```
Akses API Docs di: `http://localhost:8000/docs`

### 3. Jalankan Aplikasi Seeker (React)
Ini adalah peta interaktif untuk pencari sampah.
```bash
cd ui
npm run dev
```
Akses di: `http://localhost:5173`

---

## 📂 Struktur Proyek

```
ecocycle-id/
├── ai_service.py       # Logika analisis gambar dengan Gemini AI
├── api.py              # Backend FastAPI (melayani data ke React)
├── db.py               # Manajemen database SQLite
├── main.py             # Aplikasi Streamlit (Provider UI)
├── ecocycle.db         # Database SQLite (dibuat otomatis)
├── ui/                 # Frontend React Project
│   ├── src/            # Source code React
│   ├── public/         # Aset statis
│   └── package.json    # Dependensi Node.js
└── .streamlit/         # Konfigurasi Streamlit & Secrets
```

---

## 🔌 API Endpoints

Backend FastAPI menyediakan endpoint berikut:

- `GET /waste_posts`: Mengambil semua data pos limbah (tanpa gambar binary berat).
- `GET /waste_posts/filtered`: Mengambil data dengan filter tag (contoh: `?filters=Maggot BSF`).

---

## 📝 Catatan Pengembangan

- **Database:** File `ecocycle.db` akan dibuat otomatis saat pertama kali menjalankan `main.py` atau `api.py`.
- **Images:** Gambar disimpan sebagai BLOB di database SQLite untuk kesederhanaan MVP. Untuk produksi, disarankan menggunakan Object Storage (S3/GCS).

---

Dibuat dengan ❤️ untuk **ITB Hackathon 2025**.
