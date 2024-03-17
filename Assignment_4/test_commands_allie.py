import os
from datetime import datetime
import sqlite3

import pytest


import commands
from abc import ABC, abstractmethod

from database import DatabaseManager

@pytest.fixture
def db():
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()
    os.remove(filename)


def test_create_bookmarks_table_command(db):
    # act and arrange
    commands.CreateBookmarksTableCommand()
    conn = db.connection
    cursor = conn.cursor()

    cursor.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookmarks' ''')
    # assert
    assert cursor.fetchone()[0] == 1


def test_add_bookmark_command():
