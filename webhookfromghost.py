from flask import Flask, request, abort
from mastodon import Mastodon

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def get_webhook():
        #print(request)
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
           mastodon = Mastodon(access_token = '.secret', debug_requests=True)           
           mastodon.toot(ghostToot)
           return 'success', 200
          except:
           raise
        else:
          abort(400)

def tags_to_mastodon_has(ghostTags):
        # convert ghost cms tags to mastodon hashtags
        tagsList = ''
        #print(ghostTags)
        for tags in ghostTags:
         print(tags["name"])
         tagsList += " #"+tags["name"]
        return tagsList.lstrip()
          
if __name__ == '__main__':
	app.run(host="0.0.0.0")
