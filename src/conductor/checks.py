#!/usr/bin/env python
# * coding: utf8 *
"""
checks.py
a module with classes that check for the existence of things
"""

from textwrap import dedent

import psycopg2
import pyodbc


class TableChecker:  # pylint: disable=too-few-public-methods
    """base class for checkers
    """
    driver = None
    connection_info = None
    connection = None
    schema = None
    table = None
    sql = None

    def __init__(self, table, connection_info):
        self.connection_info = connection_info

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

    def exists(self):
        """checks if the table exists
        """

        cursor = self.connect()
        with self.connection:
            cursor.execute(dedent(self.sql), (self.schema, self.table))

            return cursor.fetchone()


class MSSqlTableChecker(TableChecker):
    """sgid10 table checker
    """

    sql = '''SELECT
                COUNT(*)
            FROM
                sys.tables
            WHERE
                LOWER(SCHEMA_NAME(schema_id)) = ?
                AND LOWER(name) = ?
            '''

    def __init__(self, table, connection_info):
        TableChecker.__init__(self, table, connection_info)
        self.driver = pyodbc

    def exists(self):
        """checks if the table exists
        """
        count, = TableChecker.exists(self)

        return count > 0


class PGSqlTableChecker(TableChecker):
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

    def __init__(self, table, connection_info):
        TableChecker.__init__(self, table, connection_info)
        self.driver = psycopg2

    def exists(self):
        """checks if the table exists
        """

        exists, = TableChecker.exists(self)

        return exists
