from pathlib import Path

from sqlite3 import Connection

file = Path(__file__).parent.joinpath('ua.sqlite')


def connect():
    return Connection(file)


if not file.exists():
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
