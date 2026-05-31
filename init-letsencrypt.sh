#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# 1. Cek certificate existing → langsung start docker
if [ -d "/etc/letsencrypt/live/${DOMAIN}" ] && [ -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
    echo -e "${YELLOW}[1/1] Certificate sudah ada, start docker ...${NC}"
    docker compose -f docker-compose.yml -f docker-compose.prod.yml down 2>/dev/null || true
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}  https://${DOMAIN}${NC}"
    echo -e "${GREEN}============================================================${NC}"
    exit 0
fi

# 2. Setup webroot & nginx temp untuk ACME
mkdir -p ./certbot-www

echo -e "${YELLOW}[1/3] Menyalakan nginx sementara untuk ACME ...${NC}"

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

# 3. Request certificate via host certbot
echo -e "${YELLOW}[2/3] Requesting Let's Encrypt certificate ...${NC}"

sudo certbot certonly --webroot \
    -w "$(pwd)/certbot-www" \
    --email "${EMAIL}" \
    -d "${DOMAIN}" \
    --rsa-key-size "${rsa_key_size}" \
    --agree-tos \
    --non-interactive

# 4. Cleanup & start stack
echo -e "${YELLOW}[3/3] Cleanup & start production stack ...${NC}"
docker stop nginx-temp 2>/dev/null || true
rm ./nginx/init.conf

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 5. Cron auto-renew
CRON_JOB="0 2 * * 0 certbot renew --quiet --deploy-hook 'docker exec visdat-nginx nginx -s reload'"
if ! sudo crontab -l 2>/dev/null | grep -q "certbot renew"; then
    (sudo crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo crontab -
    echo -e "${GREEN}Cron auto-renew: Minggu 02:00${NC}"
fi

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Setup SSL SELESAI!                                       ${NC}"
echo -e "${GREEN}============================================================${NC}"
echo -e "Akses dashboard di: ${GREEN}https://${DOMAIN}${NC}"
echo ""
