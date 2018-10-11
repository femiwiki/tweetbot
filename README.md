# [tweetbot]

[페미위키](https://femiwiki.com)의 [페미위키:한줄인용](페미위키:한줄인용) 문서에서 한 트윗을 가져와 지정된 트위터 계정으로 트윗합니다.

```bash
python3 -mvenv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export TWITTER_CONSUMER_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx
export TWITTER_CONSUMER_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export WIKI_PASSWORD=xxxxxxxx
python tweet.py
```

--------

The source code of *ranking-bot* is primarily distributed under the terms of
the [GNU Affero General Public License v3.0] or any later version. See
[COPYRIGHT] for details.

[femiwiki]: https://femiwiki.com
[GNU Affero General Public License v3.0]: LICENSE
[COPYRIGHT]: COPYRIGHT
