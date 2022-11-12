from pathlib import Path

from sqlite3 import Connection

db_file = Path(__file__).parent.joinpath('ua.sqlite')


def connect():
    return Connection(db_file)
