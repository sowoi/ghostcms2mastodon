# ghostcms2mastodon
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
You can of course change this port via Docker or in the source code. \
If you are using the docker compose setting with fixed ip, that would be the IP 10.9.9.99 \
On bare metal installations it would be localhost/127.0.0.1.

# Ghost CMS
The settings in Ghost CMS are done via custom integrations.\
The event trigger is "Post published

# Create secrets
Secrets are parsed to the folder .secrets in your docker folder:

```
.
├── docker-compose.yml
├── .secrets
│   ├── MASTODON_ACCESS_TOKEN
│   ├── MASTODON_BASE_URL
│   ├── TRUSTED_PROXIES
│   └── WEBHOOK_SECRET

```

Populate the files in the .secrets directory as follows:\
Copy your Mastodon token to MASTODON_ACCESS_TOKEN.\
Copy your Webhook token from Ghost CMS to WEBHOOK_SECRET.\
Enter in MASTODON_BASE_URL the address of your Mastodon instance, e.g. https://mastodon.social .\
At TRUSTED_PROXIES you enter a list of IPs that should have access to your webhook instance. \
By default, only localhost and access via Docker subnet from the Docker compose example is entered with a fixed IP, i.e. 10.9.9.0/24.\

# Docker
```
docker run -d -p 5000:5000/tcp \
-v "${PWD}/.secrets/WEBHOOK_SECRET:/run/secrets/WEBHOOK_SECRET:ro" \
-v "${PWD}/.secrets/MASTODON_ACCESS_TOKEN:/run/secrets/MASTODON_ACCESS_TOKEN:ro" \
-v "${PWD}/.secrets/MASTODON_BASE_URL:/run/secrets/MASTODON_BASE_URL:ro" \
-v "${PWD}/.secrets/TRUSTED_PROXIES:/run/secrets/TRUSTED_PROXIES:ro" \
--net webhookSubnet \
--ip 10.9.9.99 okxo/ghostcms2mastodon
```



# Docker compose
```
version: '3.1'

secrets:
  WEBHOOK_SECRET:
    file: ${PWD}/.secrets/WEBHOOK_SECRET
  MASTODON_ACCESS_TOKEN:
    file: ${PWD}/.secrets/MASTODON_ACCESS_TOKEN
  MASTODON_BASE_URL:
    file: ${PWD}/.secrets/MASTODON_BASE_URL
  TRUSTED_PROXIES:
    file: ${PWD}/.secrets/TRUSTED_PROXIES
    
services:
  ghostcms2mastodon:
    image: okxo/ghostcms2mastodon:latest
    restart: always
    ports:
      - 127.0.0.1:5000:5000
    secrets: [WEBHOOK_SECRET,MASTODON_ACCESS_TOKEN,MASTODON_BASE_URL,TRUSTED_PROXIES]
    environment:
       WEBHOOK_SECRET: /run/secrets/WEBHOOK_SECRET
       MASTODON_ACCESS_TOKEN: /run/secrets/MASTODON_ACCESS_TOKEN
       MASTODON_BASE_URL: /run/secrets/MASTODON_BASE_URL
       TRUSTED_PROXIES: /run/secrets/TRUSTED_PROXIES
    networks:
      vpcbr:
        ipv4_address: 10.9.9.99
    tty: true

networks:
  vpcbr:
     driver: bridge
     ipam:
       config:
         - subnet: 10.9.9.0/24
           gateway: 10.9.9.1
```
You need to enter a fixed ip for the docker container. \
docker compose up -d

# NGINX reverse proxy
Create an upstream in /etc/nginx/nginx.conf

```
  upstream mastodonwebhook {
  server 127.0.0.1:5000;
  keepalive 64;
  }
```

Add webhook location to your GhostCMS NGINX conf:

```
location /webhook {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Uri $request_uri;
        proxy_set_header X-Forwarded-Ssl on;
        proxy_redirect  http://  $scheme://;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_cache_bypass $cookie_session;
        proxy_no_cache $cookie_session;
        proxy_buffers 64 256k;

        # If behind reverse proxy, forwards the correct IP                                                                                                                                                                                                                                                                                                                                                                                                                      
        set_real_ip_from 10.0.0.0/8;
        set_real_ip_from 172.0.0.0/8;
        set_real_ip_from 10.9.0.0/16;
q        set_real_ip_from 192.168.0.0/16;
        set_real_ip_from fc00::/7;
        real_ip_header X-Forwarded-For;
        real_ip_recursive on;

        proxy_pass http://mastodonwebhook;
}

```
Restart Nginx.


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