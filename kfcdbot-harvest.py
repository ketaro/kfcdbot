import os
import twitter

LASTID_FILE='.lastid'
CORPUS_FILE="kftweets.txt"

api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                  consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                  access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                  access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

try:
    lastid = os.readlink(LASTID_FILE)
except:
    lastid = 0

print "Last ID: ", lastid

statuses = api.GetUserTimeline(screen_name='@kf', since_id=int(lastid), count=200)

corpusfile = open(CORPUS_FILE, "a")

for status in statuses:
    print "id: %s  msg: %s" % (status.id, status.text)
    corpusfile.write(status.text.encode("UTF-8") + "\n")
    
    if int(status.id) > int(lastid):
        lastid = status.id

corpusfile.close()

print "Last ID: ", lastid
if os.path.islink(LASTID_FILE):
    os.unlink(LASTID_FILE)
os.symlink(str(lastid), LASTID_FILE)


