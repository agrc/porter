#!/usr/bin/env python
# * coding: utf8 *
"""
checks.py
a module with classes that check for the existence of things
"""

from textwrap import dedent

import psycopg2
import pyodbc


class Checker:  # pylint: disable=too-few-public-methods
    """base class for checkers
    """
    connection_info = None
    connection = None
    schema = None
    table = None

    def __init__(self, table, connection_info):
        self.connection_info = connection_info

        if '.' not in table:
            raise ValueError(f'Must provide the schema {table}')

        parts = table.split('.')

        if len(parts) == 3:
            self.schema = parts[1]
            table = parts[2]
        elif len(parts) == 2:
            self.schema = parts[0]
            table = parts[1]
        elif len(parts) > 3:
            raise ValueError(f'Invalid table name {table}')

        self.table = table


class MSSql(Checker):
    """sgid10 table checker
    """

    def sql(self):
        """generate sql to find a table
        """
        sql = '''SELECT
                    COUNT(*)
                FROM
                    sys.tables
                WHERE
                    LOWER(name) = ?
                '''

        if self.schema is not None:
            sql += ' AND LOWER(SCHEMA_NAME(schema_id)) = ?'

        return sql

    def connect(self):
        """opens a connection to the connection defined in the parent class
        """
        if self.connection_info is None or len(self.connection_info) < 1:
            raise ValueError('connection string is empty. set the values in your .env file')

        self.connection = pyodbc.connect(self.connection_info)

        return self.connection.cursor()

    def exists(self):
        """checks if the table exists
        """

        cursor = self.connect()
        with self.connection:
            cursor.execute(dedent(self.sql()), (self.table, self.schema))
            row = cursor.fetchone()

            return row is not None


class PGSql(Checker):
    """open sgid checker
    """

    sql = '''SELECT EXISTS(
                SELECT FROM
                    information_schema.tables
                WHERE
                    LOWER(table_schema) = %s
                    AND LOWER(table_name) = %s
                );
            '''

    def connect(self):
        """opens a connection to the connection defined in the parent class
        """
        if self.connection_info is None:
            raise ValueError('connection string is empty. set the values in your .env file')

        self.connection = psycopg2.connect(**self.connection_info)

        return self.connection.cursor()

    def exists(self):
        """checks if the table exists
        """

        cursor = self.connect()
        row = False
        with self.connection:
            cursor.execute(dedent(self.sql), (self.schema, self.table))
            row = cursor.fetchone()

        return row[0]
