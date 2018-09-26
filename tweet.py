import json
import os
import random
import re
import urllib
import urllib.parse
from inspect import getsourcefile

import twitter

URL_PREFIX = 'https://femiwiki.com/api.php?'


def main():
    text = get_wikitext('페미위키:한줄인용', True)
    lines = text.split('\n')
    tweets = [line[1:].strip() for line in lines if
              re.match(r'^\*\s*.+$', line)]
    tweet = choice_tweet(tweets, 300)
    lines = list(break_text(tweet, 140))

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
    )
    status = api.PostUpdate(lines[0])
    for line in lines[1:]:
        status = api.PostUpdate(line, in_reply_to_status_id=status.id)


def get_wikitext(title, patrolled):
    """Returns wikitext of the document"""
    if patrolled:
        revid = get_patrolled_revid(title)
        url = (
            URL_PREFIX +
            'action=query&format=json&prop=revisions&'
            'rvprop=content&revids=' + str(revid)
        )
    else:
        quoted_title = urllib.parse.quote(title)
        url = (
            URL_PREFIX +
            'action=query&format=json&prop=revisions&'
            'rvprop=content&titles=' + quoted_title
        )

    obj = json_from_url(url)
    return next(iter(obj['query']['pages'].values()))['revisions'][0]['*']


def get_patrolled_revid(title):
    """Returns patrolled revision id of the document"""
    revid_file = os.path.join(get_module_dir(), 'patrolled_rev_id')

    try:
        # Try to get rev id using API
        quoted_title = urllib.parse.quote(title)
        patrolled_logs_url = (
            URL_PREFIX +
            'action=query&format=json&list=logevents&leprop=details&'
            'letype=patrol&lelimit=1&letitle=' +
            quoted_title
        )
        obj = json_from_url(patrolled_logs_url)
        revid = obj['query']['logevents'][0]['params']['curid']

        # Save revid for later use
        with open(revid_file, 'w') as f:
            f.write(str(revid))
    except:
        # Try to get revid from file.
        # (API returns nothing if recent logs don't contain patrol activity)
        with open(revid_file, 'r') as f:
            revid = f.readline()

    return revid


def json_from_url(url):
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode('utf-8'))


def get_module_dir():
    return os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

def choice_tweet(tweets, saving_limit=300):
    recent_tweets_file = os.path.join(get_module_dir(), 'recent_tweets')

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


def break_text(text, limit=150, cont='\u2026'):
    if len(text) <= limit:
        yield text
        return

    words = text.split(' ')
    line = ''
    for i, word in enumerate(words):
        if len(line + ' ' + word) >= limit:
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
