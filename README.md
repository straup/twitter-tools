twitter-tools
--

These are Aaron's Twitter tools. You might find them useful.

backup_tweets.py
--

This is a modified fork of
[Phil Gyford's mytweets repository](https://github.com/philgyford/mytweets). It's
been modified in two ways, principally:

* To allow for Twitter auth-y bits and other specifics to be defined in a
  configuration file (rather than as command line options).
  
* To write Twitter messages to individual JSON files in nested YYYY/MM/DD
  directories.

This is how I use it:

	$>python ./backup_tweets.py -c twitter.cfg

Pass the `-h` flag for a complete list of options.

A sample twitter.cfg file is included with this repository. It is called
[twitter.cfg.example)(https://github.com/straup/twitter-tools/blob/master/twitter.cfg.example). Aside from the Twitter authentication credentials ([that you'll need to set up on the dev.twitter site](https://dev.twitter.com/apps/new))
the important thing to update is the `backup_dir` configuration. As the name
suggests this where your Twitter messages will be stored.

mk_annual.php
--

This is the code that I use to generate a PDF book of all the tweets for a given
year. This is how I use it:

	$> php -q mk_annual.php -t ~/twitter/history -o 2012.pdf -u aaronofmontreal

Pass the `-h` flag for a complete list of options.

Printed, they look like this: [http://www.flickr.com/photos/straup/6649356617/](http://www.flickr.com/photos/straup/6649356617/)
