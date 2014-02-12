#!/usr/bin/env python

import sys
from random import choice
import twitter

CORPUS_FILE="kftweets.txt"


api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                  consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                  access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                  access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))


def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    
    chain = {}
    words = corpus.split()
    
    for i in range(len(words)-2):
        pair = (words[i], words[i+1])
        if (pair in chain):
            chain[pair] += [ words[i+2] ]
        else:
            chain[pair] = [ words[i+2] ]
        
    return chain

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    # To start, we want a word that starts with a capital letter
    start = 'z'
    while (start[0][0] != start[0][0].upper()):
        start = choice(chains.keys())
    
    line = list(start)
    
    last = line[-1][-1]
#    while (len(line) < 10):
    while (not line[-1][-1] in ['.','?']):
    	next = chains[tuple(line[-2:])]
    	line += [ choice(next) ]
#    	print "line: %r" % line
    
#    print "line: %r" % line
    
    return " ".join(line)


def main():
    args = sys.argv
    #filename = args[1]

    # Change this to read input_text from a file
    f = open(CORPUS_FILE, "r")
    chain_dict = make_chains(f.read())

    print make_text(chain_dict)
            
#    random_text = make_text(chain_dict)
#    print random_text

if __name__ == "__main__":
    main()


