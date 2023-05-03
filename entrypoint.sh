#!/bin/bash
export WEBHOOK_SECRET=$(cat /run/secrets/WEBHOOK_SECRET)
export MASTODON_ACCESS_TOKEN=$(cat /run/secrets/MASTODON_ACCESS_TOKEN)
export MASTODON_BASE_URL=$(cat /run/secrets/MASTODON_BASE_URL)
export TRUSTED_PROXIES=$(cat /run/secrets/TRUSTED_PROXIES)
echo "Starting poetry shell"
echo `poetry --version`
echo "Starting uwsgi"
poetry run uwsgi --ini /home/appuser/webhookfromghost.ini
