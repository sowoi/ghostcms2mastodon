# ghost2cms2mastodon
Send posts from GhostCMS to Mastodon.

# General design
Ghost CMS triggers new posts and sends a webhook with the new post to a local Python Flask instance.
The Flask script fetches the relevant data from the payload and creates a Mastodon post. We use Mastodon.py for this.
The Flask script is secured by UWSGI.
As a bonus, GhostCMS tags are converted to Mastodon hashtags.

# Docker
docker run -d -p 5000:5000/tcp -v $(pwd)/.secret:/.secret okxo/ghostcms2mastodon

# Docker compose
docker compse up -d
