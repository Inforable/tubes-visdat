#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auto-init .env jika belum ada
chmod +x "${SCRIPT_DIR}/scripts/init-env.sh"
"${SCRIPT_DIR}/scripts/init-env.sh"

# Load variabel dari .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "ERROR: DOMAIN dan EMAIL harus di-set di file .env"
    exit 1
fi

domains=("${DOMAIN}")
rsa_key_size=4096
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  SSL Init Script untuk ${DOMAIN}        ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# 1. Setup direktori certbot
mkdir -p ./certbot-data/live/${DOMAIN} ./certbot-www

# 2. Download TLS parameters jika belum ada
if [ ! -e "./certbot-data/options-ssl-nginx.conf" ]; then
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > ./certbot-data/options-ssl-nginx.conf
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/ssl-dhparams.pem > ./certbot-data/ssl-dhparams.pem
    echo -e "${GREEN}[1/5] TLS parameters diunduh.${NC}"
else
    echo -e "${GREEN}[1/5] TLS parameters sudah ada, skip.${NC}"
fi

# 3. Cek certificate existing
if [ -d "./certbot-data/live/${DOMAIN}" ] && [ -e "./certbot-data/live/${DOMAIN}/fullchain.pem" ]; then
    echo -e "${YELLOW}[2/5] Certificate sudah ada.${NC}"
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    exit 0
fi

# 4. Jalankan nginx sementara (HTTP-only) untuk ACME challenge
echo -e "${YELLOW}[2/5] Menyalakan nginx sementara untuk ACME ...${NC}"

cat > ./nginx/init.conf <<EOF
server {
    listen 80;
    server_name ${DOMAIN};
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 200 "SSL Init ..."; add_header Content-Type text/plain; }
}
EOF

docker compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.init.yml up -d nginx

# 5. Request certificate
echo -e "${YELLOW}[3/5] Requesting Let's Encrypt certificate ...${NC}"

domain_args=""
for domain in "${domains[@]}"; do
    domain_args="${domain_args} -d ${domain}"
done

staging_arg=""
[ "${STAGING:-0}" != "0" ] && staging_arg="--staging"

docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    ${staging_arg} --email ${EMAIL} ${domain_args} \
    --rsa-key-size ${rsa_key_size} --agree-tos --force-renewal --non-interactive" certbot

# 6. Cleanup & start production stack
echo -e "${YELLOW}[4/5] Cleanup & start production stack ...${NC}"
rm ./nginx/init.conf
docker compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.init.yml down

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Setup SSL SELESAI!                                       ${NC}"
echo -e "${GREEN}============================================================${NC}"
echo -e "Akses dashboard di: ${GREEN}https://${DOMAIN}${NC}"
echo ""
