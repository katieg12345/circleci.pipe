#!/bin/sh


if [[ -n "${KUBERNETES_SERVICE_HOST}" ]]; then
  while [ ! -f /vault/secrets/apikey ];do
    sleep 1
  done
# Source the secrets file, this will export the API_KEY environment variable
source /vault/secrets/apikey
fi

# Execute the gunicorn command
exec gunicorn --bind=0.0.0.0:${BIND_PORT} --workers=${WORKERS} --log-level=${LOG_LEVEL} project:app
