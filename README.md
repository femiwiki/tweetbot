# tweetbot

[페미위키](https://femiwiki.com)의 [페미위키:한줄인용](페미위키:한줄인용) 문서에서 한 트윗을 가져와 지정된 트위터 계정으로 트윗합니다.

```bash
docker build --tag femiwiki/tweetbot .

docker run --detach \
  --name tweetbot \
  --restart always \
  --volume /var/tweetbot:/var/tweetbot:rw \
  -e "TWITTER_CONSUMER_KEY=xxxxxxxx" \
  -e "TWITTER_CONSUMER_SECRET=xxxxxxxx" \
  -e "TWITTER_ACCESS_TOKEN=xxxxxxxx" \
  -e "TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxx" \
  -e "WIKI_PASSWORD=xxxxxxxx" \
  femiwiki/tweetbot
```

```bash
# Setup venv first
pip install -r requirements.txt
export TWITTER_CONSUMER_KEY=xxxxxxxx
export TWITTER_CONSUMER_SECRET=xxxxxxxx
export TWITTER_ACCESS_TOKEN=xxxxxxxx
export TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxx
export WIKI_PASSWORD=xxxxxxxx
python tweet.py
python tests.py

```

--------

The source code of *ranking-bot* is primarily distributed under the terms of
the [GNU Affero General Public License v3.0] or any later version. See
[COPYRIGHT] for details.

[femiwiki]: https://femiwiki.com
[GNU Affero General Public License v3.0]: LICENSE
[COPYRIGHT]: COPYRIGHT
