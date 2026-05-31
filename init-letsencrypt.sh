#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auto-init .env jika belum ada
chmod +x "${SCRIPT_DIR}/scripts/init-env.sh"
"${SCRIPT_DIR}/scripts/init-env.sh"

if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "ERROR: DOMAIN dan EMAIL harus di-set di file .env"
    exit 1
fi

rsa_key_size=4096
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  SSL Init untuk ${DOMAIN}              ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Helper: cek file valid (ada dan size > 0)
file_valid() {
    [ -s "$1" ]
}

# 1. Setup direktori
mkdir -p ./certbot-www
sudo mkdir -p /etc/letsencrypt

# 2. Download/fix TLS parameters jika belum ada atau rusak (size 0)
if ! file_valid "/etc/letsencrypt/options-ssl-nginx.conf" || ! file_valid "/etc/letsencrypt/ssl-dhparams.pem"; then
    curl -sL https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf | sudo tee /etc/letsencrypt/options-ssl-nginx.conf > /dev/null
    curl -sL https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/ssl-dhparams.pem | sudo tee /etc/letsencrypt/ssl-dhparams.pem > /dev/null
    echo -e "${GREEN}[1/3] TLS parameters diunduh ke host.${NC}"
else
    echo -e "${GREEN}[1/3] TLS parameters OK, skip.${NC}"
fi

# 3. Cek certificate existing → kalau ada, langsung start docker dan selesai
if [ -d "/etc/letsencrypt/live/${DOMAIN}" ] && file_valid "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"; then
    echo -e "${YELLOW}[2/3] Certificate sudah ada di host. Start docker ...${NC}"
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}  Stack aktif!                                             ${NC}"
    echo -e "${GREEN}  https://${DOMAIN}                                       ${NC}"
    echo -e "${GREEN}============================================================${NC}"
    exit 0
fi

# 4. Jalankan nginx sementara (HTTP-only) untuk ACME challenge
echo -e "${YELLOW}[2/3] Menyalakan nginx sementara untuk ACME ...${NC}"

cat > ./nginx/init.conf <<EOF
server {
    listen 80;
    server_name ${DOMAIN};
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 200 "SSL Init ..."; add_header Content-Type text/plain; }
}
EOF

docker run -d --rm --name nginx-temp \
    -p 80:80 \
    -v "$(pwd)/nginx/init.conf:/etc/nginx/conf.d/default.conf:ro" \
    -v "$(pwd)/certbot-www:/var/www/certbot" \
    nginx:alpine

# 5. Request certificate via certbot DI HOST (webroot)
echo -e "${YELLOW}[3/3] Requesting Let's Encrypt certificate via host certbot ...${NC}"

sudo certbot certonly --webroot \
    -w "$(pwd)/certbot-www" \
    --email "${EMAIL}" \
    -d "${DOMAIN}" \
    --rsa-key-size "${rsa_key_size}" \
    --agree-tos \
    --non-interactive

# 6. Cleanup & start production stack
docker stop nginx-temp 2>/dev/null || true
rm ./nginx/init.conf

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 7. Setup cron auto-renew (mingguan) + reload nginx container
CRON_JOB="0 2 * * 0 certbot renew --quiet --deploy-hook 'docker exec visdat-nginx nginx -s reload'"
if ! sudo crontab -l 2>/dev/null | grep -q "certbot renew"; then
    (sudo crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo crontab -
    echo -e "${GREEN}Cron auto-renew ditambahkan: setiap Minggu jam 02:00${NC}"
else
    echo -e "${GREEN}Cron auto-renew sudah ada.${NC}"
fi

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Setup SSL SELESAI!                                       ${NC}"
echo -e "${GREEN}============================================================${NC}"
echo -e "Akses dashboard di: ${GREEN}https://${DOMAIN}${NC}"
echo ""
