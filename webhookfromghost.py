from flask import Flask, request, abort
from mastodon import Mastodon
import os

access_token = os.environ.get('MASTODON_ACCESS_TOKEN')
base_url = os.environ.get('MASTODON_BASE_URL')
trusted_proxies = "127.0.0.1", "10.9.9.1", "10.9.9.99", os.environ.get('TRUSTED_PROXIES')
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def get_webhook():
        print("Posting to Mastodon")
        if request.method == 'POST':
          try:
           # extract post title, URL, excerpt and tags
           ghostTitle = str(request.json["post"]["current"]["title"])
           ghostURL = str(request.json["post"]["current"]["url"])
           ghostExcerpt = str(request.json["post"]["current"]["custom_excerpt"])
           ghostTags = request.json["post"]["current"]["tags"]         
           ghostToot = ghostTitle + "\n" + ghostExcerpt + "\n" + ghostURL

           hashtags = tags_to_mastodon_has(ghostTags)
           print("Adding Hashtags: ", hashtags)
           ghostToot = ghostTitle + "\n" + ghostExcerpt + "\n" + ghostURL + "\n" + hashtags
           print("Creating toot: ", ghostToot)
           mastodon = Mastodon(access_token = access_token, api_base_url = base_url, debug_requests=True)           
           mastodon.toot(ghostToot)
           return 'Send to Mastodon completed', 200
          except:
           raise
        else:
          abort(400)

def tags_to_mastodon_has(ghostTags):
# convert ghost cms tags to mastodon hashtags
        tagsList = ''
        for tags in ghostTags:
                print(tags["name"])
                tagsList += " #"+tags["name"]
        return tagsList.lstrip()

@app.before_request
def limit_remote_addr():
# check if remote ip is in trusted proxies
    print("Checking IP")
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            remote = request.environ['REMOTE_ADDR']
    else:
            remote = request.environ['HTTP_X_FORWARDED_FOR']
    print("Got IP ", remote) 
    if remote not in str(trusted_proxies):
            print("Your IP is not in trusted proxies list!")
            print(str(trusted_proxies))
            # forbidden
            abort(403)
         
@app.before_request
def check_access():
        print("Checking token and URL...")
        # check if token and url are set
        if access_token == None:
          print("Missing Mastodon access token")
          raise RuntimeError('Missing Mastodon access token')
        elif base_url == None:
          print("Missing Mastodon base URL")
          raise RuntimeError('Missing Mastodon base URL')
        else:
          print("Got Mastodon access token and base URL")
          
@app.before_request        
def check_if_valid_ghost_post():
# check for valid ghost post
         print("Checking valid Header")
         if "Ghost" not in str(request.headers.get('User-Agent')):
           return 'Bad Request', abort(400)
         elif "application/json" != str(request.headers.get('Content-Type')):
           return 'Bad Request', abort(400)
         else:
           print("Seems to be valid Ghost CMS post")

    
if __name__ == '__main__':
        app.run(host="0.0.0.0", debug=True)
