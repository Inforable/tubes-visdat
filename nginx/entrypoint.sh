#!/bin/sh
set -e

# Substitute env vars ke template nginx
envsubst '$DOMAIN $WWW_DOMAIN' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Auto-reload nginx setiap 7 hari (sync dengan certbot renew interval)
while :; do
    sleep 7d
    nginx -s reload &
done &

exec nginx -g 'daemon off;'
