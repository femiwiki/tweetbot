import logging
import os
import random
import re
from urllib import parse

import mastodon
import mwclient

logger = logging.getLogger(__name__)

URL = "femiwiki.com"
MASTODON_SERVER = os.environ.get("MASTODON_SERVER", "https://planet.moe")
QUOTE_POSTS_PAGE_NAME = "페미위키:한줄인용"
RECENT_POSTS_PAGE_NAME = "페미위키:한줄인용/최근 트윗"
CHARACTER_LIMIT = 300  # 마스토돈은 500자이지만 블루스카이 브리지를 고려해 300으로 제한


def main():
    try:
        site = mwclient.Site(
            URL,
            path="/",
            # XXX: mwclient가 OAuth 2.0을 지원하지 않아 OAuth 1.0을 사용`
            consumer_token=os.environ["FEMIWIKI_OAUTH1_CONSUMER_TOKEN"],
            consumer_secret=os.environ["FEMIWIKI_OAUTH1_CONSUMER_SECRET"],
            access_token=os.environ["FEMIWIKI_OAUTH1_ACCESS_TOKEN"],
            access_secret=os.environ["FEMIWIKI_OAUTH1_ACCESS_SECRET"],
        )
    except Exception as err:
        logger.exception("위키에 로그인 실패", exc_info=err)
        exit(1)

    logging.basicConfig(level=logging.INFO)
    logger.info("마스토돈 뿌우봇 가동")
    text = get_wikitext(site, QUOTE_POSTS_PAGE_NAME)
    quotations = list(convert_to_quotations(text))
    quotation = choice_quotation(site, quotations, 300)

    # 마스토돈에 뿌우하기
    thread = list(
        break_text(
            f"{quotation}&utm_source=fediverse&utm_medium=post",
            CHARACTER_LIMIT,
        )
    )
    api = mastodon.Mastodon(
        access_token=os.environ["MASTODON_ACCESS_TOKEN"], api_base_url=MASTODON_SERVER
    )
    status = api.status_post(thread[0])
    for line in thread[1:]:
        status = api.status_post(line, in_reply_to_id=status)

    logger.info("뿌우 성공")


def get_wikitext(site, title):
    """해당 글의 위키텍스트를 반환합니다"""
    result = site.api("parse", page=title, prop="wikitext", formatversion=2)
    return result["parse"]["wikitext"]


def convert_to_quotations(text):
    lines = text.split("\n")

    title = None
    for line in lines:
        tweet = re.match(r"^\*\s*(.+)\s*$", line)

        if tweet:
            if not title:
                raise Exception(f"인용글 제목이 없음: {tweet.group(1)}")
            yield (
                f"{tweet.group(1)} https://{URL}/w/{parse.quote(title)}?utm_campaign=bot"
            )
        else:
            new_title = re.match(r"^=+\s*\[*([^=\]]+)\]*\s*=+$", line)
            if new_title:
                title = new_title.group(1)


def choice_quotation(site, tweets, saving_limit=300):
    page = site.pages[RECENT_POSTS_PAGE_NAME]
    recent_tweets = page.text().split("\n")
    for recent_tweet in recent_tweets:
        if recent_tweet in tweets:
            tweets.remove(recent_tweet)

    if len(recent_tweets) + 1 > saving_limit:
        del recent_tweets[0]

    chosen_tweet = random.choice(tweets)
    recent_tweets.append(chosen_tweet)

    new_wikitext = "\n".join(recent_tweets)
    page.save(new_wikitext, "최근 글 갱신")

    return chosen_tweet


def break_text(text, limit, cont="\u2026"):
    if len(text) <= limit:
        yield text
        return

    words = text.split(" ")
    line = ""
    for i, word in enumerate(words):
        if len(line + " " + word) >= limit:
            yield line + cont
            line = cont + word
        else:
            is_last_word = len(words) == i + 1
            if is_last_word:
                yield line + " " + word
                return
            else:
                line = (line + " " + word).strip()

    if len(line):
        yield line


__all__ = ["main"]
