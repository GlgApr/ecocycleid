# EcoCycle ID - Technical Documentation

## 1. System Overview
**EcoCycle ID** adalah platform berbasis web yang menghubungkan penyedia limbah organik dengan pengelola limbah. Sistem ini menggunakan pendekatan **Hybrid Frontend** dan didukung oleh **Generative AI** untuk analisis data otomatis.

## 2. Technology Stack

| Komponen | Teknologi | Deskripsi |
| :--- | :--- | :--- |
| **AI Model** | **Google Gemini 2.5 Flash** | Multimodal AI untuk analisis visual, estimasi berat, dan validasi organik. |
| **Backend** | **FastAPI (Python)** | REST API performa tinggi (Asynchronous) untuk melayani data ke frontend. |
| **Frontend (Seeker)** | **React + Vite** | SPA modern dengan TypeScript, Tailwind CSS, dan React Leaflet untuk peta interaktif. |
| **Frontend (Provider)** | **Streamlit** | Rapid prototyping interface untuk upload foto dan manajemen data. |
| **Database** | **SQLite** | Penyimpanan relasional ringan (Metadata + Image Blobs). |
| **Geospatial** | **Folium & Leaflet** | Visualisasi peta dan penanganan koordinat. |

## 3. Core Modules

### AI Service (`ai_service.py`)
Modul kecerdasan buatan yang berinteraksi dengan Google Gemini API.
*   **Fungsi Utama:** `analyze_waste_image(image_data)`
*   **Kapabilitas:**
    *   Mendeteksi apakah gambar adalah limbah organik (Boolean).
    *   Mengestimasi berat limbah (Kg).
    *   Memberikan rekomendasi pengolahan (Maggot/Kompos/Pakan Ternak).
    *   Mendeteksi kontaminan berbahaya (Plastik/Logam).

### 🛡️ Privacy Logic (`main.py` / `api.py`)
Implementasi keamanan privasi lokasi (*Location Jittering*).
*   **Algoritma:** Menambahkan *random offset* (±200 meter) pada koordinat Latitude/Longitude asli pengguna sebelum disimpan ke database.
*   **Tujuan:** Mencegah identifikasi rumah spesifik pada peta publik.

### 🔌 API Gateway (`api.py`)
Jembatan data antara Database dan Frontend React.
*   **Endpoint Utama:**
    *   `GET /waste_posts`: Mengambil semua data titik sampah (tanpa gambar berat).
    *   `GET /waste_posts/filtered`: Filter data berdasarkan tag (misal: "Maggot BSF").
*   **Optimasi:** Menghapus field `image_blob` dari respon JSON untuk mempercepat load time peta.

## 4. Data Flow Diagram

1.  **Data Ingestion (Streamlit):**
    *   User upload foto -> `ai_service.py` memvalidasi -> Jika Valid, data + lokasi (jittered) disimpan ke SQLite (`db.py`).
2.  **Data Retrieval (React):**
    *   Browser request ke FastAPI -> API query SQLite -> API serialize data ke JSON -> Browser render Marker di Peta.
3.  **Action (WhatsApp):**
    *   User klik Marker -> Sistem generate *Deep Link* WhatsApp dengan pesan template otomatis berisi detail sampah.

## 5. Database Schema (Simplified)

Tabel utama: `waste_posts`

| Kolom | Tipe | Deskripsi |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key |
| `image_blob` | BLOB | Data binary gambar (untuk verifikasi admin) |
| `analysis_json` | TEXT | Hasil analisis Gemini (Berat, Kategori, Tips) |
| `lat` / `lon` | REAL | Koordinat lokasi (sudah di-*jitter*) |
| `contact_info` | TEXT | Nomor WhatsApp Provider |
| `created_at` | DATETIME | Timestamp upload |

## 6. Setup & Run

**Prasyarat:** Python 3.9+, Node.js, Google Gemini API Key.

1.  **Setup Backend:**
    ```bash
    pip install -r requirements.txt
    # Buat .streamlit/secrets.toml berisi [gemini] api_key="..."
    ```

2.  **Jalankan Komponen:**
    *   **Terminal 1 (Provider UI):** `streamlit run main.py`
    *   **Terminal 2 (Backend API):** `uvicorn api:app --reload --port 8000`
    *   **Terminal 3 (Seeker UI):** `cd ui && npm install && npm run dev`

---

*Dokumen ini ditujukan untuk pengembang dan juri teknis ITB Hackathon 2025.*
