#!/usr/bin/env python
# * coding: utf8 *
"""
checks.py
a module with classes that check for the existence of things
"""

from collections import namedtuple
from textwrap import dedent

import psycopg2
import pyodbc
import requests


class TableChecker:  # pylint: disable=too-few-public-methods
    """base class for checkers
    """
    driver = None
    connection_info = None
    connection = None
    original_table = None
    data = None
    database = None
    schema = None
    table = None
    sql = None

    def __init__(self, table, connection_info):
        self.connection_info = connection_info
        self.original_table = table

        if '.' not in table:
            raise ValueError(f'Must provide the schema {table}')

        parts = table.split('.')
        part_count = len(parts)

        if part_count > 3 or part_count < 2:
            raise ValueError(f'Invalid table name {table}')

        if part_count == 2:
            self.schema = parts[0]
            table = parts[1]
        else:
            self.database = parts[0]
            self.schema = parts[1]
            table = parts[2]

        self.table = table

    def connect(self):
        """opens a connection to the connection defined in the parent class
        """
        if self.connection_info is None or len(self.connection_info) < 1:
            raise ValueError('connection string is empty. set the values in your .env file')

        self.connection = self.driver.connect(**self.connection_info)

        return self.connection.cursor()

    def get_data(self, parameters):
        """checks if the table exists
        """

        cursor = self.connect()
        with self.connection:
            cursor.execute(dedent(self.sql), parameters)

            self.data = cursor.fetchone()

            return self.data


class MSSqlTableChecker(TableChecker):
    """sgid10 table checker
    """

    sql = '''SELECT
                COUNT(*)
            FROM
                sys.tables
            WHERE
                LOWER(SCHEMA_NAME(schema_id)) = LOWER(?)
                AND LOWER(name) = LOWER(?)
            '''

    def __init__(self, table, connection_info):
        TableChecker.__init__(self, table, connection_info)
        self.driver = pyodbc

    def exists(self):
        """checks if the table exists
        """
        TableChecker.get_data(self, (self.schema, self.table))
        count = self.data[0]

        return count > 0


class PGSqlTableChecker(TableChecker):
    """open sgid table checker
    """

    sql = '''SELECT EXISTS(
                SELECT FROM
                    information_schema.tables
                WHERE
                    LOWER(table_schema) = LOWER(%s)
                    AND LOWER(table_name) = LOWER(%s)
                );
            '''

    def __init__(self, table, connection_info):
        TableChecker.__init__(self, table, connection_info)
        self.driver = psycopg2

    @classmethod
    def postgresize(cls, name):
        """takes the agol name and makes it conform to pgsql conventions
        """
        if name is None:
            return name

        new_name = name.lower()
        new_name = new_name.replace('utah ', '', 1).replace(' ', '_')

        return new_name

    def exists(self):
        """checks if the table exists
        """

        TableChecker.get_data(self, (self.schema, self.table))
        exists = self.data[0]

        return exists


class MetaTableChecker(TableChecker):
    """meta table row checker
    """
    sql = '''SELECT AGOL_ITEM_ID, AGOL_PUBLISHED_NAME
            FROM
                SGID.META.AGOLITEMS
            WHERE
                LOWER(TABLENAME) = LOWER(?)
            '''

    def __init__(self, table, connection_info):
        TableChecker.__init__(self, table, connection_info)
        self.driver = pyodbc

    def exists(self):
        """checks if the row exists
        """
        item_id = None
        item_name = None
        MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')

        TableChecker.get_data(self, (self.original_table))

        if self.data is None:
            self.data = MetaResponse(False, item_id, item_name)

            return False

        item_id, item_name = self.data
        response = True

        if not item_id and not item_name:
            response = False
        elif not item_id:
            response = 'missing item id'
        elif not item_name:
            response = 'missing item name'

        self.data = MetaResponse(response, item_id, item_name)

        return response


class UrlChecker():  # pylint: disable=too-few-public-methods
    """checks if a url is good or bad
    """
    url = None
    data = None

    def get_data(self, args=None):
        """requests the data from the url
        """
        self.data = requests.get(self.url, params=args, allow_redirects=False)


class ArcGisOnlineChecker(UrlChecker):
    """check if the arcgis online item exists
    """

    def __init__(self, item_id):
        self.url = f'https://www.arcgis.com/sharing/rest/content/items/{item_id}'

    def get_data(self, args=None):
        """requests the data from the url
        """
        UrlChecker.get_data(self, {'f': 'json'})

    def exists(self):
        """checks if the url exists
        """
        self.get_data()
        self.data = self.data.json()

        return 'owner' in self.data


class OpenDataChecker(UrlChecker):
    """check if the arcgis online item exists
    """

    def __init__(self, item_name):
        self.url = f'https://opendata.gis.utah.gov/datasets/{OpenDataChecker.kebab_case(item_name)}'

    @classmethod
    def kebab_case(cls, string):
        """returns a lowercase kebab string
        """
        return string.lower().replace(' ', '-')

    def exists(self):
        """checks if the url exists
        """
        UrlChecker.get_data(self)
        self.data = self.data.status_code

        return self.data == 200
