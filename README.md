twitter-tools
--

These are Aaron's Twitter tools. You might find them useful.

**NOTE: I am publishing these as-is, right now. They mostly work except for the
  part where they don't and I'm the only one who knows the magic dance.** None
  of it is hard it's just not documented yet.

backup_tweets.py
--

This is a modified fork of Phil Gyford's backup_tweets.py script. If you run it
with the `-h(elp)` flag you'll see something like this:

	$> python ./backup_tweets.py -h
	Usage: backup_tweets.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -c CONFIG, --config=CONFIG
	  -k CONSUMER_KEY, --consumer-key=CONSUMER_KEY
	  -s CONSUMER_KEY, --consumer-secret=CONSUMER_KEY
	  -o ACCESS_TOKEN, --access-token=ACCESS_TOKEN
	  -e ACCESS_TOKEN_SECRET, --access-token-secret=ACCESS_TOKEN_SECRET
	  -m TIMELINE, --timeline=TIMELINE
	  -t PICKLE, --as-text=PICKLE
	  -v, --verbose         

This is how I use it:

	$>python ./backup_tweets.py -c twitter.cfg

Which is to say I am probably just going to remove all the command-line
flags. The script writes individual tweets as JSON files in a YYYY/MM/DD
directory structure.

mk_annual.php
--

This is the code that I use to generate a PDF book of all the tweets for a given
year. This is how I use it:

	$> php -q ./mk_annual.php ~/twitter/history/2012/ ~/Desktop/test.pdf 2012
