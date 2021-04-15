import os
import random
import re
import logging
from urllib import parse, request

import mwclient
import twitter


logger = logging.getLogger(__name__)

URL = 'femiwiki.com'
RECENT_TWEETS_PAGE_NAME = '페미위키:한줄인용/최근 트윗'

SITE = mwclient.Site(URL, path='/')
USER = '트윗봇@트윗봇'


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting the tweetbot')

    if 'WIKI_PASSWORD' in os.environ:
        SITE.login(USER, os.environ['WIKI_PASSWORD'])
    text = get_wikitext('페미위키:한줄인용', True)
    quotations = list(convert_to_quotations(text))
    quotation = choice_quotation(quotations, 300)

    # Post for Twitter
    thread = list(break_text(f'{quotation}&utm_source=twitter&utm_medium=tweet', twitter.api.CHARACTER_LIMIT))
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
    )
    status = api.PostUpdate(thread[0])
    for line in thread[1:]:
        status = api.PostUpdate(line, in_reply_to_status_id=status.id)

    logger.info('Successfully tweeted')


def get_wikitext(title, stable):
    """Returns wikitext of the title"""
    url = f'https://{URL}/index.php?action=raw&'
    if stable:
        revid = get_stable_revid(title)
        if revid is None:
            return get_wikitext(title, False)
        url = url + f'oldid={revid}'
    else:
        quoted_title = parse.quote(title)
        url = url + f'title={quoted_title}'

    with request.urlopen(url) as res:
        return res.read().decode('utf-8')


def get_stable_revid(title):
    """Returns the stable revision id of the given title"""
    try:
        # Try to get the stable rev id using API
        result = SITE.api(
            'query',
            prop='info|flagged',
            titles=title
        )
        page = next(iter(result['query']['pages'].values()[0]))

        if 'flagged' in page and 'stable_revid' in page['flagged']:
            return page['flagged']['stable_revid']
        return page['lastrevid']
    except Exception:
        # (API returns nothing if recent logs don't contain patrol activity)
        return None


def convert_to_quotations(text):
    lines = text.split('\n')

    title = None
    for line in lines:
        tweet = re.match(r'^\*\s*(.+)\s*$', line)

        if tweet:
            yield (
                f'{tweet.group(1)} https://{URL}/w/{parse.quote(title)}?utm_campaign=bot'
            )
        else:
            new_title = re.match(r'^=+\s*\[*([^=\]]+)\]*\s*=+$', line)
            if new_title:
                title = new_title.group(1)


def choice_quotation(tweets, saving_limit=300):
    page = SITE.pages[RECENT_TWEETS_PAGE_NAME]
    recent_tweets = page.text().split('\n')
    for recent_tweet in recent_tweets:
        if recent_tweet in tweets:
            tweets.remove(recent_tweet)

    if len(recent_tweets) + 1 > saving_limit:
        del recent_tweets[0]

    chosen_tweet = random.choice(tweets)
    recent_tweets.append(chosen_tweet)

    new_wikitext = '\n'.join(recent_tweets)
    page.save(new_wikitext, '최근 트윗 갱신')

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


__all__ = [
    "main"
]
