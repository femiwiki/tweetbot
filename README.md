[tweetbot]
========

[Github Action]을 통해 [페미위키]의 [페미위키:한줄인용] 문서에서 한 문장을 가져와 지정된 트위터
계정에 트윗합니다.

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

[Github Action]: https://github.com/features/actions
[tweetbot]: https://femiwiki.com/w/%EC%82%AC%EC%9A%A9%EC%9E%90:%ED%8A%B8%EC%9C%97%EB%B4%87
[페미위키]: https://femiwiki.com
[페미위키:한줄인용]: https://femiwiki.com/w/%ED%8E%98%EB%AF%B8%EC%9C%84%ED%82%A4:%ED%95%9C%EC%A4%84%EC%9D%B8%EC%9A%A9
[GNU Affero General Public License v3.0]: LICENSE
[COPYRIGHT]: COPYRIGHT
