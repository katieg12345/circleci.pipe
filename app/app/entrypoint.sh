#!/bin/bash

# Source the secrets file, this will export the API_KEY environment variable
source /vault/secrets/apiKey

# Execute the gunicorn command
exec gunicorn --bind=0.0.0.0:${BIND_PORT} --workers=${WORKERS} --log-level=${LOG_LEVEL} project:app
