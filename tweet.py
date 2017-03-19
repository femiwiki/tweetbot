import json
import os
import random
import re
import urllib
import urllib.parse
from inspect import getsourcefile

import twitter

URL_PREFIX = 'https://femiwiki.com/w/api.php?'


def main():
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
    )
    text = get_wikitext('페미위키:한줄인용', True)
    lines = text.split('\n')
    tweets = [line[1:].strip() for line in lines if
              re.match(r'^\*\s+.+$', line)]
    tweet = random.choice(tweets)
    api.PostUpdate(tweet)


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


if __name__ == '__main__':
    main()
