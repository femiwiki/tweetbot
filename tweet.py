import json
import os
import random
import re
import urllib
import urllib.parse
from inspect import getsourcefile

import twitter
import mwclient

URL = 'femiwiki.com'
RECENT_TWEETS_DIR = '/var/tweetbot'


def main():
    text = get_wikitext('페미위키:한줄인용', True)
    tweets = list(convert_to_tweets(text))
    tweet = choice_tweet(tweets, 300)
    thread = list(break_text(tweet, twitter.api.CHARACTER_LIMIT))

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
    )
    status = api.PostUpdate(thread[0])
    for line in thread[1:]:
        status = api.PostUpdate(line, in_reply_to_status_id=status.id)


def get_wikitext(title, patrolled):
    """Returns wikitext of the document"""
    if patrolled:
        revid = get_patrolled_revid(title)
        if revid == None:
            return get_wikitext(title, False)
        url = (
            'https://' + URL +
            '/api.php?action=query&format=json&prop=revisions&'
            'rvprop=content&revids=' + str(revid)
        )
    else:
        quoted_title = urllib.parse.quote(title)
        url = (
            'https://' + URL +
            '/api.php?action=query&format=json&prop=revisions&'
            'rvprop=content&titles=' + quoted_title
        )

    obj = json_from_url(url)
    return next(iter(obj['query']['pages'].values()))['revisions'][0]['*']


def get_patrolled_revid(title):
    """Returns patrolled revision id of the document"""
    try:
        # Try to get rev id using API
        # We need the "patrol" or "patrolmarks" right to request the patrolled flag.
        site = mwclient.Site(URL, path='/')
        user = '트윗봇'
        pw = os.environ['WIKI_PASSWORD']
        site.login(user, pw)
        changes = []
        rccontinue = None
        while True:
            result = site.api(
                'query',
                list='recentchanges',
                rcnamespace=4,
                rctype='edit',
                rcshow='patrolled',
                rcprop='title|ids',
                rclimit='max',
                rcgeneraterevisions=1,
                rccontinue=rccontinue,
            )
            changes += result['query']['recentchanges']
            if 'continue' not in result:
                break
            else:
                rccontinue = result['continue']['rccontinue']

        revid = [ rc['revid'] for rc in changes if rc['title'] == title ]

        return revid[0] if len(revid) != 0 else None
    except:
        # (API returns nothing if recent logs don't contain patrol activity)
        return None


def json_from_url(url):
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode('utf-8'))


def get_module_dir():
    return os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

def convert_to_tweets(text):
    lines = text.split('\n')

    title = None
    for line in lines:
        tweet = re.match(r'^\*\s*(.+)\s*$', line)

        if tweet:
            yield ( tweet.group(1) + ' http://' + URL + '/w/' + urllib.parse.quote(title) +
                    '?utm_source=twitter&utm_campaign=bot&utm_medium=tweet'
            )
        else:
            new_title = re.match(r'^=+\s*\[*([^=\]]+)\]*\s*=+$', line)
            if new_title:
                title = new_title.group(1)

    return

def choice_tweet(tweets, saving_limit=300):
    recent_tweets_file = os.path.join(RECENT_TWEETS_DIR, 'recent_tweets')

    try:
        with open(recent_tweets_file, 'r') as f:
            recent_tweets = f.read().split('\n')
    except IOError:
        recent_tweets = []

    for recent_tweet in recent_tweets:
        if recent_tweet in tweets:
            tweets.remove(recent_tweet)

    if len(recent_tweets)+1 > saving_limit:
        del recent_tweets[0]

    chosen_tweet = random.choice(tweets)
    recent_tweets.append(chosen_tweet)

    with open(recent_tweets_file, 'w') as f:
        f.write('\n'.join(recent_tweets))

    return chosen_tweet


def break_text(text, limit=280, cont='\u2026'):
    if twitter.twitter_utils.calc_expected_status_length(text) <= limit:
        yield text
        return

    words = text.split(' ')
    line = ''
    for i, word in enumerate(words):
        if twitter.twitter_utils.calc_expected_status_length(line + ' ' + word) >= limit:
            yield line + cont
            line = cont + word
        else:
            is_last_word = len(words) == i + 1
            if is_last_word:
                yield line + ' ' + word
                return
            else:
                line = (line + ' ' + word).strip()

    if len(line):
        yield line


if __name__ == '__main__':
    main()
