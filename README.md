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

Printed, they look like this:

	NNNMMNNNNNNNNNNNNNDNNDDDDDDNDDDNNNNDNNNDDDZMMMMMMMMODDDNNNND
	DNNMMNNNNNNNNDDNDNDDDDDDDDDDDNNDNDDDDNNNNNNMMMMMMMMMMMMMMMMN
	MMMMMNNNNND777$ZZZ$DDDDDDDDDDDDDDNNNNNNNNNNMMMMMMMMMMMMMMMMN
	NNNMMNNNNNN++IZ$Z$$$7$DDDDDNNNNNNNNNNNNNNNNNNNMMMMMMMMMMMNNN
	NNNMMNNNNNI+?$$$$$7777777DDDDDDNDDNDDDNDNNNNNNMMMMMMDNMMMMNN
	MMMMMNNNNN=+I$$777777IIIIIIIZDDDDDDDDDDDDNNNNNNNMMM~::~:~~=Z
	MMMMNNNNN==?77777IIIII?IIIIIIIID8DDDDDDNDO8MM,,,:::::::~:=IO
	MMMMMNNNN+=I77IIII?III????III????ID888MM.,,,,,:::::::::~~~I8
	MMMMNNNN~~=77IIIII??I??I??II?I??????D8:,,,,,,,,,:::::~~~~~?D
	NNMMMNNN~+7III?????IMM???II??IIIIIIIZ~,,,,,,,,,,:::::~:~~~?D
	NNMNNNN~=IIII????M????ID7NIIIIII??I$D:,.,,,,,,,,,:::::~~~=7D
	NNMNNN::=7II????M+??ZIM7IIIIMII???IZ+,,,,,,,,,,,,:::::~~~=7D
	MMMNND=~III???+??+NM?IIIII7II?II??78:,,,MD+.Z,+:::::::~~==ID
	MMNND::?I?????+8M????M?MIIIIZ????I$M,,,.,,.,.:,,~MM::~~~~~?D
	NDDD8::?????++????=MM??II8MI7III?IZ~,,,,,,~.,,,,,::::~~~~=I8
	NDDD,~????+++++7~Z????DMIIIIZ88??7D:,,,..,,,,,,,,::::~~~==?8
	DDD8~=I??+?+++++?+?M+D??IIIIIII?I$O,,,,.,,,,,,,,,:::::~===IO
	DDD:~7I??+++++++???????8MIIIII??IO~,.,,,,,,,,,,,::::~~~==+7O
	DD8~$7II??+++++++??????III$I?I??7N,,,.,,,,,,,,:::::~~===++$8
	DD:~77I?+++++++++??????IIIIIII?IZ+,,,,,,,,,,,,,::::~~~=++?$O
	D8:III???+++++++++++??IIIIIIIIII8:,,.,,,,,,,,,::::~~~===++78
	D:IIIII???+++++++++????IIIII?I?$D,.,,,,,,,,,:::::~~~~==+++I8
	I:IIII??++++++++++++???IIIIII?IO~,...,,,,,,,:::::~~~==+++?7D
	:I7IIII???+++++=++++???II77II?7D,,,,,,,,,,:::::~~~~==++??7$D
	=777III???++++++++++????I77III$?,,,,,,,,,:::::~~~~==+???I7OD
	$$$III?I7N$Z++++++++++?II7II778:,,,,,,,::::::~~~===++?II$$8D
	$777I?IZNN8O++++++++++??I7777$D::,,,,,:::::~~~~==++?II7$ZO8D
	$77I7II$NN$?+++++++++++?I777$Z+~::,:::::::~~~=~=+??I7$$ZOODD
	77777II??ZI???+++++++++?I$$ZZD=~::::::~:~~~===++?7I7$ZOOOODD
	IIIII7IIII?II?????++++?$ZZZOOO=~~~~~~~~~===++?II777ZZOO8OODD
	=?I?II777IIIII?II???OD88OO88DZ?===~~===+=+??I7777$ZOOOO888DD
	DDD~~?IIII7IIII?I?8NDDDN88DDMO$?++++++++???I77N8MDNOO88888DN
	888NND8~~+IIII??DDNNMDDNNDDNN8Z7IIII??III777$Z8MZ88O888888DD
	8888DDDDDDDD:~DDNNNMMMNNNMNNNDOZ$7$$7777$$ZZZOODMON888888DDD
	8D88DDDDDDDDD$8DNNNMMMMNNNNNND8OOZZZZZ$ZZZOOO888NN8888888DDN
	88DD8DDDDDDDD7ONNNMMMMNNNNMMNDD888OO8NNMNDOO8O8888888D88DDDD
	8888DDDDDDDDDZODNNNMMMMMMMMMNNDDD88NNMMMMD8888888888DD88DDDD
	88888D8DDDDDDZODNMMMMMMMMMMMMMMMMMNMMMMMDD8888888888888888DD

See also: [http://www.flickr.com/photos/straup/6649356617/](http://www.flickr.com/photos/straup/6649356617/)
