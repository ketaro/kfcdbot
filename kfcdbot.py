#!/usr/bin/env python

import sys
import os
import re
from random import choice
import twitter


STARTKEY='STARTPAIR'


def make_chains(wordfiles):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    
    chain = {}
    chain[STARTKEY] = []
    
    for filename in wordfiles:
        try:
            wordfile = open(filename, "r")
        
            line = wordfile.readline()
            while line != '':
                words = line.split()
                
                for i in range(len(words)-2):
                    pair = (words[i], words[i+1])
                    if i == 0:
                        chain[STARTKEY].append(pair)
                        
                    if (pair in chain):
                        chain[pair] += [ words[i+2] ]
                    else:
                        chain[pair] = [ words[i+2] ]
                
                line = wordfile.readline()
            
            wordfile.close()
        except:
            print "Unable to load file: ", filename
        
    return chain

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    # To start, we want a word that starts with a capital letter
#    start = 'z'
#    while (start[0][0] != start[0][0].upper()):
#        start = choice(chains.keys())
    
    # Select a random pair from the start list
    if len(chains[STARTKEY]) < 1:
        sys.exit("Empty Chain Dictionary!")
    
    start = choice(chains[STARTKEY])
    
    line = list(start)
    
    last = line[-1][-1]
#    while (len(line) < 10):
    while (not line[-1][-1] in ['.','?'] and tuple(line[-2:]) in chains):
    	next = chains[tuple(line[-2:])]
    	line += [ choice(next) ]
#    	print "line: %r" % line
    
#    print "line: %r" % line
    
    return " ".join(line)


def main():
    args = sys.argv
    atpattern = re.compile(r'@(\w+)\b')

    if len(args) < 2:
        print """
   %s - Python Markov Twitter Bot
   
   Usage:
   
       %s <corpse file>[ <corpusfile>...]

   This script read in corpus files passed as command-line arguments and
   generate a randomized tweet using markov chains.
   
""" % (sys.argv[0], sys.argv[0])
        sys.exit()


    # Create the markov chain dictionary
    chain_dict = make_chains(args[1:])

    api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                     consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                     access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                     access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

    answer = ""
    while answer.lower() != 'q':
        tweet = make_text(chain_dict)
        
        # Replace @'s with ()'s
        tweet = atpattern.sub(r'(\1)', tweet)
        
        print "\nGenerated %d characters:\n%s\n" % (len(tweet), tweet)
        
        print "Tweet this? ([n]/y/q): ",
        
        answer = sys.stdin.readline().strip()
        
        if answer.lower() == 'y':
            api.PostUpdate(tweet)
        
#    random_text = make_text(chain_dict)
#    print random_text

if __name__ == "__main__":
    main()


