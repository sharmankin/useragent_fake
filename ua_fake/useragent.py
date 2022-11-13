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

    def __call__(self, *args, **kwargs) -> str:
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
    _opera = Browser('opera')
    _safari = Browser('safari')
    _yandex_browser = Browser('yandex-browser')

    def __call__(self, *args, **kwargs) -> str:

        return choice(
            [
                self._firefox,
                self._chrome,
                self._edge,
                self._opera,
                self._safari
            ]
        )()

    @property
    def firefox(self) -> str:
        return self._firefox()

    @property
    def chrome(self) -> str:
        return self._chrome()

    @property
    def edge(self) -> str:
        return self._edge()

    @property
    def opera(self) -> str:
        return self._opera()

    @property
    def safari(self) -> str:
        return self._safari()

    @property
    def yandex_browser(self) -> str:
        return self._yandex_browser()

    @staticmethod
    def update():
        update_database()
