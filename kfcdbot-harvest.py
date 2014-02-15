import sys
import os
import twitter

LASTID_FILE='.lastid'

if len(sys.argv) < 2:
    print """
   %s - Python Twitter Timeline Harvestor
   
   Usage:
   
       %s <twitter account>[ <twitter account>...]

   The script will save all the tweets in a separate file for each account with
   the name <twitter account>-tweets.txt.
   
""" % (sys.argv[0], sys.argv[0])
    sys.exit()


api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                  consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                  access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                  access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))


for account in sys.argv[1:]:
    lastid_file = LASTID_FILE + '-' + account
    
    try:
        lastid = os.readlink(lastid_file)
    except:
        lastid = 0
    
    print "Last ID for %s: %r" % (account, lastid)

    statuses = api.GetUserTimeline(screen_name='@' + account, since_id=int(lastid), count=200)

    corpusfile = open(account + '-tweets.txt', "a")
    
    for status in statuses:
        print "[%s] id: %s  msg: %s" % (account, status.id, status.text)
        corpusfile.write(status.text.encode("UTF-8") + "\n")
        
        if int(status.id) > int(lastid):
            lastid = status.id
    
    corpusfile.close()
    
    print "Last ID: ", lastid
    if os.path.islink(lastid_file):
        os.unlink(lastid_file)
    os.symlink(str(lastid), lastid_file)
    
    
