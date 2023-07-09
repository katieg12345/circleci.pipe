#!/bin/sh

if [[ -n "${KUBERNETES_SERVICE_HOST}" ]]; then
# Source the secrets file, this will export the API_KEY environment variable
source /vault/secrets/apiKey
fi
# Execute the gunicorn command
exec gunicorn --bind=0.0.0.0:${BIND_PORT} --workers=${WORKERS} --log-level=${LOG_LEVEL} project:app
