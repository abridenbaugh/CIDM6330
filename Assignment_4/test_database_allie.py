import os
from datetime import datetime
import sqlite3

import pytest


from database import DatabaseManager


@pytest.fixture
def database_manager() -> DatabaseManager:
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()
    os.remove(filename)
    # used test fixture setup from Dr. Babb's code


def test_database_manager_create_table(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",  # name of table
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null"
        },  # fields and data type of contents of table
    )
    # act
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookmarks' ''')
    # assert
    assert cursor.fetchone()[0] == 1
    # referenced Dr. Babb's code


def test_database_manager_drop_table(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",  # name of table
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null"
        },  # fields and data type of contents of table
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()
    }

    database_manager.add("bookmarks", data)

    # act
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE bookmarks''')

    # assert
    assert cursor.fetchone() == None


def test_database_manager_add_bookmark(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",  # name of table
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null"
        },  # fields and data type of contents of table
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()
    }

    database_manager.add("bookmarks", data)

    # act
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bookmarks WHERE title='test_title' ''')

    # assert
    assert cursor.fetchone()[0] == 1


def test_database_manager_delete_bookmark(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",  # name of table
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null"
        },  # fields and data type of contents of table
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()
    }

    database_manager.add("bookmarks", data)

    # act
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM bookmarks WHERE title='test_title' ''')

    # assert
    assert cursor.fetchone() == None


def test_database_manager_select_bookmark(database_manager):
    # arrange
    database_manager.create_table(
        "bookmarks",  # name of table
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null"
        },  # fields and data type of contents of table
    )

    data = {
        "title": "test_1_title",
        "url": "http://example_1.com",
        "notes": "test 1 notes",
        "date_added": datetime.utcnow().isoformat()}
    new_data = {
        "title": "test_2_title",
        "url": "http://example_2.com",
        "notes": "test 2 notes",
        "date_added": datetime.utcnow().isoformat()
    }

    data.update(new_data)

    database_manager.add("bookmarks", data)

    # act
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bookmarks WHERE title='test_2_title' ''')

    # assert
    assert cursor.fetchone()[0] == 1
