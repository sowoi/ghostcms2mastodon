# ghost2cms2mastodon
Send posts from GhostCMS to Mastodon.

# General design
Ghost CMS triggers new posts and sends a webhook with the new post to a local Python Flask instance.\
The Flask script fetches the relevant data from the payload and creates a Mastodon post.\
We use Mastodon.py for this.\
The Flask script is secured by UWSGI and access control.\
As a bonus, GhostCMS tags are converted to Mastodon hashtags.

# Remote use
If you are not running the instance on the same server as Ghost CMS, you need to encrypt the connection via https (e.g. using a reverse proxy).
Your GhostCMS must then be added to the trusted proxies list in .env

# Prequistes
- Mastodon access token 
- Custom integrations webhook in Ghost CMS
- You need to adjust .env

# Webhook endpoint
 http://<yourIP>:5000/webhook

# Docker
docker run -d -p 5000:5000/tcp \
-e ASTODON_ACCESS_TOKEN='**Add_your_Access_Token_Here**' \
-e MASTODON_BASE_URL='**https://Add_your_Mastodon_URL_Here**' \
-e TRUSTED_PROXIES='**LIST of IPs with access to local webhook endpoint**'\
okxo/ghostcms2mastodon

# Docker compose
See docker-compose.yml file \
You need to enter a fixed ip for the docker container. \
docker compose up -d


# Bare metal
apt install python3-dev python3-venv
 
pip3 install -r requirements
 
python3 -m venv webhook && source webhook/bin/activate
 
cd webhook
 
cp Pythonfiles and ini files to your webhook folder
 
create a .secret file with your credentials

start uwsgi server: uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

 
# Acknowledgements
This project uses https://github.com/halcy/Mastodon.py

# License
Licensed under the terms of Apache License Version 2. See LICENSE file.