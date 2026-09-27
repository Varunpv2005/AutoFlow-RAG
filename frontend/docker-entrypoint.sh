#!/bin/sh
set -e

# Default values if environment variables are not set
export PORT="${PORT:-80}"
export BACKEND_HOST="${BACKEND_HOST:-backend:8000}"

echo "Configuring Nginx with PORT=${PORT} and BACKEND_HOST=${BACKEND_HOST}..."

# Substitute ${PORT} and ${BACKEND_HOST} into nginx.conf
envsubst '${PORT} ${BACKEND_HOST}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Validate Nginx configuration syntax before starting
echo "Validating Nginx configuration..."
nginx -t

echo "Starting Nginx..."
exec nginx -g "daemon off;"
