# ghost2cms2mastodon
Send posts from GhostCMS to Mastodon.

# General design
Ghost CMS triggers new posts and sends a webhook with the new post to a local Python Flask instance.\
The Flask script fetches the relevant data from the payload and creates a Mastodon post.\
We use Mastodon.py for this.\
The Flask script is secured by UWSGI and access control.\
As a bonus, GhostCMS tags are converted to Mastodon hashtags.

# Remote use / security
By default, the webhook endpoint should not be accessible from outside. \
Access to the webhook is unencrypted, because GhostCMS does not allow access (without major intervention) to self-signed certificates. \
If you are not running the instance on the same server as Ghost CMS, you need to encrypt the connection via https (e.g. using a reverse proxy). \
Your GhostCMS must then be added to the trusted proxies list in .env

# Prequistes
- Mastodon access token 
- Custom integrations webhook in Ghost CMS
- You need to adjust .env or pass the environment variables via docker run (see below)


# Mastodon access token
The only check you need to set is at "write:statuses".\
Leave all others unchecked! \
This container does not use any other settings and therefore does not need any other permissions!

# Webhook endpoint
 http://**dockerIP**:5000/webhook
You can of course change this port via Docker or in the source code.
if you are using the docker compose setting with fixed ip, that would be the IP 10.9.9.99
On bare metal installations it would be localhost.

# Ghost CMS
The settings in Ghost CMS are done via custom integrations.\
The event trigger is "Post published

# Docker
docker run -d -p 127.0.0.1:5000:5000/tcp \
-e MASTODON_ACCESS_TOKEN='**Add_your_Access_Token_Here**' \
-e MASTODON_BASE_URL='**https://Add_your_Mastodon_URL_Here**' \
-e TRUSTED_PROXIES='**LIST of IPs with access to local webhook endpoint**'\
okxo/ghostcms2mastodon

# Docker compose
See docker-compose.yml file \
You need to enter a fixed ip for the docker container. \
docker compose up -d


# Bare metal
apt install python3-dev python3-venv \
pip3 install -r requirements \
python3 -m venv webhook && source webhook/bin/activate \
cd webhook \
cp Pythonfiles and ini files to your webhook folder \
export MASTODON_ACCESS_TOKEN='**Add_your_Access_Token_Here**' \
export MASTODON_BASE_URL='**https://Add_your_Mastodon_URL_Here**' \
export TRUSTED_PROXIES='**LIST of IPs with access to local webhook endpoint**'\
start uwsgi server: uwsgi --socket 127.0.0.1:5000 --protocol=http -w wsgi:app

 
# Acknowledgements
This project uses https://github.com/halcy/Mastodon.py and would not be feasible without this advance work.

# License
Licensed under the terms of Apache License Version 2. See LICENSE file.

# Dev
https://okxo.de