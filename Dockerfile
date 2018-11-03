FROM python:3-slim-stretch

# Set timezone
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add Tini
# See https://github.com/krallin/tini for the further details
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Install cron
RUN apt-get update && apt-get -y install cron

# Register a cronjob
COPY crontab .
RUN crontab crontab && rm crontab

# Install dependencies
WORKDIR /a
COPY requirements.txt .
RUN /usr/local/bin/python3 -m pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY tweet.py .

VOLUME /var/tweetbot

CMD { \
        echo "export TWITTER_CONSUMER_KEY='$TWITTER_CONSUMER_KEY'"; \
        echo "export TWITTER_CONSUMER_SECRET='$TWITTER_CONSUMER_SECRET'"; \
        echo "export TWITTER_ACCESS_TOKEN='$TWITTER_ACCESS_TOKEN'"; \
        echo "export TWITTER_ACCESS_TOKEN_SECRET='$TWITTER_ACCESS_TOKEN_SECRET'"; \
        echo "export WIKI_PASSWORD='$WIKI_PASSWORD'"; \
    } > /a/env &&\
    cron &&\
    sleep infinity
