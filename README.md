# 🌊 Visualisasi Interaktif Banjir Regional Indonesia (2000 - 2025)

Sebuah dashboard analitik spasial-temporal interaktif premium yang menyajikan visualisasi data historis kejadian banjir di seluruh provinsi di Indonesia dari tahun **2000 hingga 2025**. Dashboard ini dirancang dengan estetika modern **Light Slate-Navy** untuk mempermudah pemahaman tren ekskalasi bencana secara regional dan kronologis.

---

## ✨ Fitur Utama Dashboard

1. **🗺️ Peta Kloroplet Interaktif Regional**
   * Peta spasial interaktif nasional yang menampilkan beban risiko kejadian banjir per provinsi.
   * **Kontinuitas Visual Penuh**: Provinsi dengan 0 kejadian tetap dirender dengan warna abu-abu slate (`#cbd5e1`) sehingga siluet peta Indonesia tetap terlihat utuh dan profesional.
2. **🎬 Mode Animasi Temporal (Autoplay)**
   * Dukungan dua mode analisis waktu: **Rentang Tahun (Statik)** dan **Animasi (Play/Pause)**.
   * Playback panel interaktif dengan tombol **Play ▶️**, **Pause ⏸️**, **Mundur ⏪**, dan **Maju ⏩** untuk menyapu perubahan tren kasus secara otomatis dari 2000 ke 2025.
3. **📊 Analisis Grafik Komparatif & Tren**
   * **Top 10 Provinsi**: Diagram batang horizontal interaktif yang menyorot provinsi terdampak terparah.
   * **Tren Tahunan**: Grafik garis tren dengan penunjuk garis vertikal dinamis (pada mode animasi) untuk melacak tren kenaikan historis.
4. **💡 Informasi Kunci & Wawasan Data (Glassmorphic Takeaways)**
   * Rangkuman analisis kunci otomatis mengenai beban risiko, konsentrasi geografis di pulau Jawa, serta rekomendasi mitigasi kebencanaan regional.

---

## 🚀 Panduan Setup & Menjalankan Dashboard

Ikuti langkah-langkah di bawah ini untuk menginstal dependensi dan menjalankan dashboard secara lokal dari repositori hasil kloning:

### 1. Pull dan Switch ke Branch `tubes-2`
Pastikan repositori Anda berada pada branch pengembangan visualisasi interaktif (`tubes-2`):
```bash
git fetch origin
git checkout tubes-2
git pull origin tubes-2
```

### 2. Buat & Aktifkan Virtual Environment
Membuat environment Python lokal agar dependensi tidak bentrok dengan library global sistem Anda:

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
Perbarui pip dan pasang semua library yang tercantum di dalam `requirements.txt` (Streamlit, Plotly, Pandas, PyArrow, dll.):
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
Jalankan server Streamlit lokal untuk memuat dashboard:
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
* **`.streamlit/config.toml`**: Konfigurasi tema global Streamlit untuk memaksa render *Light Theme* yang premium.