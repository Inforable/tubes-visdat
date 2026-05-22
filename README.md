# 🌊 Visualisasi Interaktif Banjir Regional Indonesia (2000 - 2025)

---

## ✨ Fitur Utama Dashboard

1. **🗺️ Peta Kloroplet Interaktif Regional**
2. **🎬 Mode Animasi Temporal (Autoplay)**
3. **📊 Analisis Grafik Komparatif & Tren**
4. **💡 Informasi Kunci & Wawasan Data**

---

## 🚀 Panduan Setup & Menjalankan Dashboard

Ikuti langkah-langkah di bawah ini untuk menginstal dependensi dan menjalankan dashboard secara lokal dari repositori hasil kloning:

### 1. Pull dan Switch ke Branch `tubes-2`
```bash
git fetch origin
git checkout tubes-2
git pull origin tubes-2
```

### 2. Buat & Aktifkan Virtual Environment

* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
* **Windows (Command Prompt):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

### 3. Install Dependensi
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

Aplikasi secara otomatis akan terbuka di browser Anda pada alamat default:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 📁 Struktur Proyek Utama
* **`app.py`**: Berkas kode utama aplikasi Streamlit (layout, interaktivitas, dan visualisasi).
* **`assets/`**: Berkas aset ikon SVG yang dimuat secara inline untuk mempertahankan kecepatan render dan warna yang seragam.
* **`data/processed/`**: Dataset olahan agregasi spasial-tahunan yang sudah siap pakai secara instan.
* **`requirements.txt`**: Daftar dependensi modul Python yang dibutuhkan proyek.
* **`.streamlit/config.toml`**: Konfigurasi tema global Streamlit.