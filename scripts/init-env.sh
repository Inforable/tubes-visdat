#!/bin/bash
# ============================================================
# init-env.sh — Auto-create .env dari .env.example jika belum ada
# ============================================================

set -e

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${PROJECT_DIR}/.env"
EXAMPLE_FILE="${PROJECT_DIR}/.env.example"

if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}[init-env]${NC} File .env sudah ada di ${ENV_FILE}. Melanjutkan..."
    exit 0
fi

if [ ! -f "$EXAMPLE_FILE" ]; then
    echo -e "${RED}[init-env ERROR]${NC} Tidak ditemukan .env.example di ${EXAMPLE_FILE}."
    echo "        Pastikan file .env.example ada di repository sebelum menjalankan script ini."
    exit 1
fi

echo -e "${YELLOW}[init-env]${NC} File .env tidak ditemukan."
echo -e "${YELLOW}[init-env]${NC} Meng-copy dari .env.example → .env ..."

cp "$EXAMPLE_FILE" "$ENV_FILE"

echo ""
echo -e "${GREEN}[init-env]${NC} .env berhasil dibuat dari .env.example!"
echo -e "${YELLOW}        WARNING:${NC} .env yang saat ini digunakan masih berisi nilai default."
echo -e "        Pastikan kamu sudah meng-edit file .env sebelum menjalankan init-letsencrypt.sh."
echo ""
echo "        File .env sekarang berada di: ${ENV_FILE}"
echo ""
