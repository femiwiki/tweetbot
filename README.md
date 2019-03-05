[tweetbot] [![Docker Badge]][Docker Hub]
========

[페미위키]의 [페미위키:한줄인용] 문서에서 한 문장을 가져와 지정된 트위터
계정 및 페이스북 페이지로 트윗합니다.

```bash
docker run --detach \
  --name tweetbot \
  --restart always \
  --volume /var/tweetbot:/var/tweetbot \
  -e 'WIKI_PASSWORD=xxxxxxxx' \
  -e 'TWITTER_CONSUMER_KEY=xxxxxxxx' \
  -e 'TWITTER_CONSUMER_SECRET=xxxxxxxx' \
  -e 'TWITTER_ACCESS_TOKEN=xxxxxxxx' \
  -e 'TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxx' \
  -e 'FACEBOOK_PAGE_TOKEN=xxxxxxxx' \
  femiwiki/tweetbot
```

&nbsp;

Development
--------
```bash
# Setup venv first

pip install -r requirements.txt
pip install --editable .

# Run
export TWITTER_CONSUMER_KEY=xxxxxxxx
export TWITTER_CONSUMER_SECRET=xxxxxxxx
export TWITTER_ACCESS_TOKEN=xxxxxxxx
export TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxx
export WIKI_PASSWORD=xxxxxxxx
python -m tweetbot

# Test
pip install pytest
pytest

# Lint
pip install flake8
flake8

# Packaging
pip install wheel
python setup.py sdist bdist_wheel
```

&nbsp;

--------

The source code of *tweetbot* is primarily distributed under the terms of
the [GNU Affero General Public License v3.0] or any later version. See
[COPYRIGHT] for details.

[Docker Badge]: https://badgen.net/docker/pulls/femiwiki/tweetbot?icon=docker&label=pulls
[Docker Hub]: https://hub.docker.com/r/femiwiki/tweetbot/
[tweetbot]: https://femiwiki.com/w/%EC%82%AC%EC%9A%A9%EC%9E%90:%ED%8A%B8%EC%9C%97%EB%B4%87
[페미위키]: https://femiwiki.com
[페미위키:한줄인용]: https://femiwiki.com/w/%ED%8E%98%EB%AF%B8%EC%9C%84%ED%82%A4:%ED%95%9C%EC%A4%84%EC%9D%B8%EC%9A%A9
[GNU Affero General Public License v3.0]: LICENSE
[COPYRIGHT]: COPYRIGHT
