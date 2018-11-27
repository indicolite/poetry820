# poetry820

push a Tang poetry every day with [mail_tang.py](https://github.com/indicolite/poetry820/blob/master/mail_tang.py) with [tang_poetry](https://github.com/hxgdzyuyi/tang_poetry/blob/master/tang_poetry.sql)

push a Song poetry every day with [mail_song.py](https://github.com/indicolite/poetry820/blob/master/mail_song.py) with [ci.db](https://github.com/chinese-poetry/chinese-poetry/blob/master/ci/ci.db)

use pgloader: from source sqlite3 to dest pg10 with [ci.db](https://github.com/chinese-poetry/chinese-poetry/blob/master/ci/ci.db) to [ci.pgdump](https://github.com/indicolite/poetry820/blob/master/ci.pgdump)
```
/usr/local/bin/pgloader ./ci.db postgresql:///ci
```

```
begin;
update ci set content=regexp_replace("content", '词牌介绍', '');
update ci set content = regexp_replace("content", E'>>', '');
update ci set content=regexp_replace(content, '\s+$', E'');
commit;
```
