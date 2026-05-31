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

### 1. Pull dan Switch ke Branch `app`
```bash
git fetch origin
git checkout app
git pull origin app
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
* **`Dockerfile`**, **`docker-compose.yml`**, **`docker-compose.override.yml`**, **`docker-compose.prod.yml`**: Konfigurasi containerisasi dan orkestrasi multi-environment (dev & production).
* **`nginx/templates/default.conf.template`**: Template konfigurasi Nginx yang menggunakan variabel environment `$DOMAIN` — diproses oleh `envsubst` saat container start.
* **`nginx/entrypoint.sh`**: Entrypoint Nginx container yang menangani `envsubst` template dan auto-reload sertifikat.
* **`init-letsencrypt.sh`**: Skrip otomatisasi pembuatan sertifikat SSL Let's Encrypt pertama kali. **Certbot dijalankan langsung di host VPS** (bukan container), sehingga Docker tidak perlu mengurus SSL.
* **`.env`** / **`.env.example`**: Konfigurasi central (domain, email). File `.env` di-`.gitignore` agar tidak masuk ke repository; `.env.example` selalu di-commit sebagai template.
* **`scripts/init-env.sh`**: Script helper yang otomatis membuat `.env` dari `.env.example` jika user lupa membuatnya sebelum deploy.

---

## 🐳 Deployment ke VPS (Ubuntu) — Docker + Nginx + SSL via Host Certbot

Semua konfigurasi domain & email di `.env`. **Certbot berjalan di host VPS**, bukan di dalam container. Docker cuma menjalankan `app` dan `nginx` saja.

### Prasyarat
1. VPS Ubuntu 20.04/22.04/24.04 dengan **Docker** & **Docker Compose Plugin** terinstall.
2. **Domain** (contoh: `fayyadh.rizain.wiweka.boye.jovandra.cloud`) sudah diarahkan (A record) ke IP publik VPS.
3. **Port 80 & 443** terbuka di firewall VPS.

### Langkah 1: Setup VPS (SSH ke server)
```bash
sudo apt update && sudo apt upgrade -y

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Clone repo
git clone <repo-url> tubes1-visdat
cd tubes1-visdat
git checkout app
```

### Langkah 2: Install Certbot di Host VPS
```bash
sudo apt install certbot -y
```

### Langkah 3: Konfigurasi `.env`

File `.env` sudah masuk `.gitignore`, sehingga tidak akan ikut ter-commit ke repository.

**Opsi A — Buat manual (direkomendasikan):**
```bash
cp .env.example .env
nano .env
```

**Opsi B — Biarkan script auto-copy (kalau lupa):**
Jika kamu lupa membuat `.env`, script `init-letsencrypt.sh` akan otomatis menjalankan `scripts/init-env.sh` yang meng-copy `.env.example → .env` dan menampilkan warning agar kamu meng-edit nilainya sebelum lanjut.

Isi `.env` sesuai domain kamu:
```bash
# Konfigurasi Domain & SSL
DOMAIN=fayyadh.rizain.wiweka.boye.jovandra.cloud
EMAIL=admin@fayyadh.rizain.wiweka.boye.jovandra.cloud
```

> **Catatan:** Cukup edit `.env` ini saja. Semua file lain akan membaca variabel dari sini secara otomatis.

### Langkah 4: Bangun Image & Jalankan Dev (Opsional — cek lokal di VPS)
```bash
# Mode development: port 8501 langsung terbuka
docker compose up -d
# Buka http://<IP-VPS>:8501
```

### Langkah 5: Inisialisasi SSL (Pertama Kali Saja!)
```bash
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

Skrip ini akan:
1. Membaca variabel dari `.env` (auto-copy dari `.env.example` jika belum ada).
2. Mengunduh TLS parameters recommended dari Certbot ke `/etc/letsencrypt/` di **host**.
3. Menyalakan nginx sementara (HTTP-only) via `docker run` untuk melayani ACME challenge.
4. Menjalankan **Certbot langsung di host VPS** (`certbot certonly --webroot`) untuk mendapatkan sertifikat SSL.
5. Membersihkan container nginx sementara dan menyalakan stack produksi penuh.
6. Menambahkan **cron job di host VPS** untuk auto-renew sertifikat setiap minggu + reload container nginx otomatis.

### Langkah 6: Verifikasi Stack Produksi
```bash
# Cek status container (hanya app + nginx)
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps

# Cek logs real-time
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
```

Akses dashboard:
👉 **https://fayyadh.rizain.wiweka.boye.jovandra.cloud** (ganti sesuai DOMAIN di `.env`)

HTTP (port 80) akan otomatis **redirect 301 → HTTPS**.

### Perintah Operasional Setelah Deploy
```bash
# Restart setelah update kode
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Renew manual (via host certbot)
sudo certbot renew --deploy-hook "docker exec visdat-nginx nginx -s reload"

# Hentikan semua service
docker compose -f docker-compose.yml -f docker-compose.prod.yml down

# Hentikan + bersihkan semua data SSL (hati-hati!)
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
sudo rm -rf /etc/letsencrypt/live/<domain-lama>
```

### Cara Kerja `.env` & `envsubst`
- **`nginx/templates/default.conf.template`** berisi placeholder `${DOMAIN}`.
- **`nginx/entrypoint.sh`** menjalankan `envsubst` saat container nginx start untuk menghasilkan `/etc/nginx/conf.d/default.conf` yang valid.
- **`docker-compose.prod.yml`** memuat variabel `.env` ke nginx dan mount `/etc/letsencrypt` dari host ke container (read-only).
- **`init-letsencrypt.sh`** membaca `.env`, menjalankan certbot di host, lalu menyalakan stack produksi.

Jika suatu saat ingin ganti domain, cukup:
1. Edit `.env` → `DOMAIN=domainbaru.com`
2. Hapus folder `/etc/letsencrypt/live/domain-lama`
3. Jalankan ulang `./init-letsencrypt.sh`

### Arsitektur Production
```
Host VPS
├── Certbot (install & renew SSL di /etc/letsencrypt)
│   └── Cron: Minggu 02:00 → renew + docker exec nginx reload
│
└── Docker Compose
    ├── visdat-nginx ──► :80 / :443 (mount /etc/letsencrypt:ro)
    └── visdat-app ────► :8501
```

| Service | Lokasi | Fungsi | Port Eksternal |
|---|---|---|---|
| `visdat-app` | Docker | Streamlit dashboard | — (internal 8501) |
| `visdat-nginx` | Docker | Reverse proxy + SSL + envsubst | **80**, **443** |
| `certbot` | **Host VPS** | Request & auto-renewal sertifikat Let's Encrypt | — |
