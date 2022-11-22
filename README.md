# ghost2cms2mastodon
Send posts from GhostCMS to Mastodon.

# General design
Ghost CMS triggers new posts and sends a webhook with the new post to a local Python Flask instance.
The Flask script fetches the relevant data from the payload and creates a Mastodon post. We use Mastodon.py for this.
The Flask script is secured by UWSGI.
As a bonus, GhostCMS tags are converted to Mastodon hashtags.

# Prequistes
- Mastodon access token 
- Custom integrations webhook in Ghost CMS
- You need to adjust .secrets 

# Webhook endpoint
 https://<yourIP>:5000/webhook

# Docker
docker run -d -p 5000:5000/tcp -v $(pwd)/.secret:/.secret okxo/ghostcms2mastodon

# Docker compose
docker compse up -d

# Bare metal
apt install python3-dev python3-venv
pip3 install -r requirements
python3 -m venv webhook && source webhook/bin/activate
cd webhook
cp Pythonfiles and ini files to your webhook folder
create a .secret file with your credentials
start uwsgi server: uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
