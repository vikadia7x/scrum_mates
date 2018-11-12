#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir -p /code/logs
touch /code/logs/gunicorn.log
touch /code/logs/gunicorn-access.log
tail -n 0 -f /code/logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=MovieShowTimeFinder.settings
export AppID = '69f71ca9-d764-4aa5-996b-293c580b7995'
export SecretAppKey = 'ocQ7HQP2s5uDE7+/nEWR6Mp3pu1KcAeWbnzS0GILjmE='
export TenantId = '41f88ecb-ca63-404d-97dd-ab0a169fd138'
export VaultUrl = 'https://showtimefinderkeyvault.vault.azure.net/'

exec gunicorn MovieShowTimeFinder.wsgi:application \
     --name MovieShowTimeFinder \
     --bind 0.0.0.0:8000 \
     --workers 5 \
     --log-level=info \
     --log-file=/code/logs/gunicorn.log \
     --access-logfile=/code/logs/gunicorn-access.log \
"$@"
