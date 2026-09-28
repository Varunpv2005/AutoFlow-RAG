#!/bin/sh
set -e

# Default values if environment variables are not set
export PORT="${PORT:-80}"
export BACKEND_URL="${BACKEND_URL:-http://backend:8000}"

echo "=========================================="
echo "Frontend Nginx Runtime Environment Config:"
echo "PORT=${PORT}"
echo "BACKEND_URL=${BACKEND_URL}"
echo "=========================================="

# Remove any trailing slash from BACKEND_URL to ensure Nginx proxy_pass preserves request paths (/api/...)
export BACKEND_URL=$(echo "${BACKEND_URL}" | sed 's|/*$||')

# Extract backend host (domain name without scheme or port) for Nginx Host header
# e.g., https://autoflow-rag-backend.onrender.com -> autoflow-rag-backend.onrender.com
# e.g., http://backend:8000 -> backend
export backend_host=$(echo "${BACKEND_URL}" | sed -e 's|^[^/]*//||' -e 's|/.*$||' -e 's|:.*$||')

echo "Extracted backend host for Host header: ${backend_host}"

# Substitute variables into default.conf
# Note: $backend_host is substituted, so proxy_set_header Host receives the clean domain name
envsubst '${PORT} ${BACKEND_URL} ${backend_host}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

echo "Generated Nginx default.conf:"
cat /etc/nginx/conf.d/default.conf

echo "Validating Nginx configuration..."
nginx -t

echo "Starting Nginx..."
exec nginx -g "daemon off;"
