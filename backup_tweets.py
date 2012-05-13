#!/usr/bin/env python

import oauth2 as oauth

import logging
import warnings
warnings.simplefilter('ignore', DeprecationWarning)

import optparse
import ConfigParser

import httplib2
import urllib
import time
import sys
import re
import pickle
import os
import os.path

import time
import datetime
from dateutil import parser as _dateparser

try:
    import json
except ImportError:
    import simplejson as json

class mytweets:

    def __init__ (self, cfg):

        self.__cfg__ = cfg

        self.timedelta = datetime.timedelta(seconds=time.timezone)

        # Valid options for TIMELINE or -m, and the corresponding endpoints
        # at twitter.com/statuses/ and the local filenames we use.

        self.timelines = {

            'user': {
                'remote': 'user_timeline',
                'local': 'my_tweets'
                },

            'friends': {
                'remote': 'friends_timeline',
                'local': 'my_friends_tweets'
                }

            }

        _remote = self.timelines[ self.cfg('timeline') ]['remote']
        _local = self.timelines[ self.cfg('timeline') ]['local']

        if self.cfg('pickle') :
            _local += '.txt'
        else :
            _local += '.json'

        self.remote_timeline = "http://twitter.com/statuses/%s.json" % _remote
        self.local_timeline = _local

    def cfg (self, key):

        if not self.__cfg__.has_option('twitter', key):
            return False

        return self.__cfg__.get('twitter', key)

    # Simple length heuristic

    def normalize_url(self, url):

        if len(url) < 10:
            return None

        # Make sure we have some sort of protocol

        if not re.search('://', url):
            url = 'http://' + url

        return url

    def lookup_short_urls(self, tweet):

        # If short_urls are already there, skip

        if 'short_urls' in tweet:
            return

        # (Start of line or word)
        # (Maybe something like http://)
        # (A vaguely domain-like section, at least one dot which is not a double dot)
        # (Whatever else follows, liberally via non-whitespace)

        url_regex = '(\A|\\b)([\w-]+://)?\S+[.][^\s.]\S*'

        redir = httplib2.Http(timeout=10)
        redir.follow_redirects = False
        redir.force_exception_to_status_code = True

        short_urls = {}

        new_text = tweet['text']

        for sub in tweet['text'].split():
            orig_url_match = re.search(url_regex, sub)

            if not orig_url_match:
                continue

            orig_url = self.normalize_url(orig_url_match.group(0))

            if not orig_url:
                continue

            logging.debug("expand %s" % orig_url)

            try:
                response = redir.request(orig_url)[0]

                if 'status' in response and response['status'] == '301':
                    short_urls[response['location']] = orig_url
                    new_text = new_text.replace(orig_url, response['location'])
            except:
                logging.error("failed to expand %s: %s" % (orig_url, e))

        tweet['short_urls'] = short_urls
        tweet['text'] = new_text

    def fetch_and_save_new_tweets(self):

        tweets = self.load_all()

        old_tweet_ids = set(t['id'] for t in tweets)

        if tweets:
            since_id = max(t['id'] for t in tweets)
        else:
            since_id = None

        try:
            new_tweets = self.fetch_all(since_id)
        except ValueError, msg:
            logging.error("An error occurred while getting your tweets: ", msg)
            return False

        num_new_saved = 0

        for tweet in new_tweets:

            if tweet['id'] not in old_tweet_ids:
                tweets.append(tweet)
                num_new_saved += 1

            tweets.sort(key = lambda t: t['id'], reverse=True)

        logging.info("There are %s new Twitter messages" % num_new_saved)

        # Delete the 'user' key (unless this is the friends' timeline),
        # lookup short URLs

        for t in tweets:

            if self.cfg('timeline') == 'user' and 'user' in t:
                del t['user']

            self.lookup_short_urls(t)

        logging.info("writing stuff back to disk...")

        # Save back to disk
        self.write_all(tweets)

        return True

    def fetch_all(self, since_id = None):

        all_tweets = []
        seen_ids = set()
        page = 0

        args = {'count': 200}

        if since_id is not None:
            args['since_id'] = since_id

        all_tweets_len = len(all_tweets)

        while True:

            logging.debug("fetch page %s" % page)
            args['page'] = page

            # Via http://blog.yjl.im/2010/04/first-step-to-twitter-oauth-streaming.html

            consumer = oauth.Consumer(key=self.cfg('consumer_key'), secret=self.cfg('consumer_secret'))
            token = oauth.Token(key=self.cfg('access_token'), secret=self.cfg('access_token_secret'))
            client = oauth.Client(consumer, token)

            try:

                resp, content = client.request("%s?%s" % (self.remote_timeline, urllib.urlencode(args)), 'GET')
                logging.info(resp)

                # This usually seems to mean the request has timed out, but if we try again
                # the result has been cached and will work second time round.

                if resp['status'] == '502':
                    logging.warning("Twitter returned 502, sleeping for 2 seconds")
                    time.sleep(2)
                    resp, content = client.request("%s?%s" % (self.remote_timeline, urllib.urlencode(args)), 'GET')

            except Exception, e:
                logging.error("Aborting! HTTP request failed completely: %s" % e)
                break

            page += 1

            try:
                tweets = json.loads(content)
            except Exception, e:
                logging.error("JSON parsing failed: %s" % e)
                break

            if 'error' in tweets:
                logging.error("Twitter says NO: %s" % tweets['error'])
                break

            if not tweets:
                logging.debug("No tweets, stop looking")
                break

            for tweet in tweets:

                if tweet['id'] not in seen_ids:
                    seen_ids.add(tweet['id'])
                    all_tweets.append(tweet)
                    all_tweets_len = len(all_tweets)

            logging.debug("pause so as not to make Baby Twitter cry")
            time.sleep(2)

        all_tweets.sort(key = lambda t: t['id'], reverse=True)
        return all_tweets

    def load_all(self) :

        """
        if self.cfg('backup_ymd'):
            return self.load_all_files()
        """

        file = self.local_timeline

        if not os.path.exists(file):
            return []

        fh = open(file, 'r')

        if self.cfg('pickle'):
            all = pickle.load(fh)
        else:
            all = json.load(fh)

        return all

    def load_all_files(self):

        backup_dir = self.cfg('backup_dir')

        # os.walk here...

    def write_all(self, tweets):

        if self.cfg('backup_ymd'):
            return self.write_all_files(tweets)

        file = self.local_timeline
        fh = open(file, 'w')

        if self.cfg('pickle'):
            pickle.dump(tweets, fh)
        else :
            json.dump(tweets, fh, indent = 2)

        fh.close()
        return

    def write_all_files(self, tweets):

        backup_dir = self.cfg('backup_dir')

        for tweet in tweets:

            id = tweet['id']

            # Thu Dec 23 05:54:42 +0000 2010
            created = tweet['created_at']

            # fmt = '%a %b %d %H:%M:%S +0000 %Y'
            # dt = time.strptime(created, fmt)
            # ymd = time.strftime("%Y/%m/%d", dt)

            dt = _dateparser.parse(created)
            dt = dt - self.timedelta
            ymd = dt.strftime("%Y/%m/%d")

            tweet_dirname = os.path.join(backup_dir, ymd)
            tweet_basename = "%s/%s.json" % (tweet_dirname, tweet['id'])

            if not os.path.exists(tweet_dirname):
                os.makedirs(tweet_dirname)

            logging.info("write %s" % tweet_basename)

            fh = open(tweet_basename, 'w')
            json.dump(tweet, fh, indent = 2)
            fh.close()
            
        return

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config", default=None, help="")
    parser.add_option("-k", "--consumer-key", dest="consumer_key", default=None, help="")
    parser.add_option("-s", "--consumer-secret", dest="consumer_key", default=None, help="")
    parser.add_option("-o", "--access-token", dest="access_token", default=None, help="")
    parser.add_option("-e", "--access-token-secret", dest="access_token_secret", default=None, help="")
    parser.add_option("-m", "--timeline", dest="timeline", default="user", help="")
    parser.add_option("-t", "--as-text", dest="pickle", default=False, help="")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="")

    # TODO: allow for custom file name and/or custom YMD directory in which to store individual tweets

    (opts, args) = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if opts.config:
        cfg = ConfigParser.ConfigParser()
        cfg.read(opts.config)

    # TODO: check for config.py here

    else:
        cfg = ConfigParser.ConfigParser()
        cfg.add_section('twitter')

    # fill in the blanks

    for k, v in vars(opts).items():
        if v and not cfg.has_option('twitter', k):
            cfg.set('twitter', k, v)

    # TODO: ensure various parameters here

    tw = mytweets(cfg)
    tw.fetch_and_save_new_tweets()
