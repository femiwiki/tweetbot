[tweetbot] [![Github checks status]][github checks link] [![codecov.io status]][codecov.io link]
========

[GitHub Action]을 통해 [페미위키]의 [페미위키:한줄인용] 문서에서 한 문장을 가져와 지정된 마스토돈
계정에 트윗합니다.

## 개발

```bash
# Run
export MASTODON_ACCESS_TOKEN=xxxxxxxx
export FEMIWIKI_OAUTH1_CONSUMER_TOKEN=xxxxxxxx
export FEMIWIKI_OAUTH1_CONSUMER_SECRET=xxxxxxxx
export FEMIWIKI_OAUTH1_ACCESS_TOKEN=xxxxxxxx
export FEMIWIKI_OAUTH1_ACCESS_SECRET=xxxxxxxx
uv run tweetbot

# Test
uv run pytest

# Lint
uv run flake8

# Packaging
uv build
```

--------

The source code of *tweetbot* is primarily distributed under the terms of
the [GNU Affero General Public License v3.0] or any later version. See
[COPYRIGHT] for details.

[github checks status]: https://badgen.net/github/checks/femiwiki/tweetbot
[github checks link]: https://github.com/femiwiki/tweetbot/actions
[codecov.io status]: https://badgen.net/codecov/c/github/femiwiki/tweetbot
[codecov.io link]: https://codecov.io/gh/femiwiki/tweetbot
[GitHub Action]: https://github.com/features/actions
[tweetbot]: https://femiwiki.com/w/%EC%82%AC%EC%9A%A9%EC%9E%90:%ED%8A%B8%EC%9C%97%EB%B4%87
[페미위키]: https://femiwiki.com
[페미위키:한줄인용]: https://femiwiki.com/w/%ED%8E%98%EB%AF%B8%EC%9C%84%ED%82%A4:%ED%95%9C%EC%A4%84%EC%9D%B8%EC%9A%A9
[GNU Affero General Public License v3.0]: LICENSE
[COPYRIGHT]: COPYRIGHT
