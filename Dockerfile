FROM python:3-slim-stretch

COPY requirements.txt /root/tweetbot/
COPY tweet.py /srv/tweetbot/
COPY tweet.sh /srv/tweetbot/
COPY crontab /root/tweetbot/

VOLUME /var/tweetbot

RUN /usr/local/bin/python3 -m pip install --no-cache-dir -r /root/tweetbot/requirements.txt \
    && chmod +x /srv/tweetbot/tweet.sh \
    && apt-get update \
    && apt-get -y install cron \
    && crontab /root/tweetbot/crontab \
    && rm -rf /root/tweetbot

CMD sed -i s/\$TWITTER_CONSUMER_KEY/${TWITTER_CONSUMER_KEY}/ /srv/tweetbot/tweet.sh \
    && sed -i s/\$TWITTER_CONSUMER_SECRET/${TWITTER_CONSUMER_SECRET}/ /srv/tweetbot/tweet.sh \
    && sed -i s/\$TWITTER_ACCESS_TOKEN/${TWITTER_ACCESS_TOKEN}/ /srv/tweetbot/tweet.sh \
    && sed -i s/\$TWITTER_ACCESS_SECRET/${TWITTER_ACCESS_TOKEN_SECRET}/ /srv/tweetbot/tweet.sh \
    && sed -i s/\$WIKI_PASSWORD/${WIKI_PASSWORD}/ /srv/tweetbot/tweet.sh \
    && cron && sleep infinity
