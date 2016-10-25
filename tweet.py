import os
import re
import random
import json
import urllib.parse
import urllib
import twitter


def main():
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
    )
    text = get_wikitext('페미위키:한줄인용')
    lines = text.split('\n')
    tweets = [line[1:].strip() for line in lines if re.match(r'^\*\s+.+$', line)]
    tweet = random.choice(tweets)
    api.PostUpdate(tweet)


def get_wikitext(title):
    url_prefix = 'https://femiwiki.com/w/api.php?action=query&format=json&prop=revisions&rvprop=content&titles='
    url = url_prefix + urllib.parse.quote(title)
    with urllib.request.urlopen(url) as res:
        obj = json.loads(res.read().decode('utf-8'))
        return next(iter(obj['query']['pages'].values()))['revisions'][0]['*']


if __name__ == '__main__':
    main()

