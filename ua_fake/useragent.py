from .db import connect, db_file
from .updater import update_database
from random import choice

if not db_file.exists():
    with connect() as cn:
        cn.execute(
            """
            create table if not exists useragent
                (
                    id         INTEGER not null
                        constraint useragent_pk
                            primary key autoincrement,
                    app        TEXT    not null,
                    os         TEXT    not null,
                    user_agent TEXT    not null,
                    constraint useragent_unique_index
                        unique (user_agent, app)
                );
            """
        )
        update_database()


class Browser:
    _cn = connect()

    def __init__(self, browser):
        self._name = browser

    def __del__(self):
        self._cn.close()

    def __call__(self, *args, **kwargs):
        cr = self._cn.cursor()
        cr.execute(
            """
            select user_agent from useragent where app = ?
            """,
            [
                self._name
            ]
        )

        data = [ua for ua, in cr.fetchall()]

        cr.close()
        return choice(data)


class UserAgent:
    _firefox = Browser('firefox')
    _chrome = Browser('chrome')
    _edge = Browser('edge')

    def __call__(self, *args, **kwargs) -> Browser:
        r = choice(
            [
                self._firefox,
                self._chrome,
                self._edge
            ]
        )
        return r()

    @property
    def firefox(self) -> Browser:
        return self._firefox()

    @property
    def chrome(self) -> Browser:
        return self._chrome()

    @property
    def edge(self) -> Browser:
        return self._edge()

    @staticmethod
    def update():
        update_database()
