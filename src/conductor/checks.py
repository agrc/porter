#!/usr/bin/env python
# * coding: utf8 *
"""
checks.py
a module with classes that check for the existence of things
"""

import re
from collections import namedtuple
from textwrap import dedent

import psycopg2
import pygsheets
import pyodbc
import requests


class TableChecker:
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

    @staticmethod
    def grade(add, report_value):
        """grades the basic boolean report
            report - boolean exists result
        """
        if add:
            if report_value:
                return ':+1:'

            return ':no_entry:'

        if report_value:
            return ':no_entry:'

        return ':+1:'


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

    @staticmethod
    def postgresize(name):
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

            return MetaResponse(False, item_id, item_name)

        item_id, item_name = self.data
        response = True

        if not item_id and not item_name:
            response = False
        elif not item_id:
            response = 'missing item id'
        elif not item_name:
            response = 'missing item name'
        #: TODO: add geometry type

        self.data = MetaResponse(response, item_id, item_name)

        return self.data

    @staticmethod
    def grade(add, report_value):
        """overrides the basic grading
        """
        if add:
            if not report_value.item_id and not report_value.item_name:
                return ' |\n| - item id | :no_entry: |\n| - item name | :no_entry:'

            if not report_value.item_id:
                return ' |\n| - item id | :no_entry: |\n| - item name | :+1:'

            if not report_value.item_name:
                return ' |\n| - item id | :+1: |\n| - item name | :no_entry:'

            return ' |\n| - item id | :+1: |\n| - item name | :+1:'

        #: deletions should not contain a row
        if report_value.exists:
            return ':no_entry:'

        return ':+1:'


class UrlChecker():  # pylint: disable=too-few-public-methods
    """checks if a url is good or bad
    """
    url = None
    data = None

    def get_data(self, args=None):
        """requests the data from the url
        """
        self.data = requests.get(self.url, params=args, allow_redirects=False)

    @staticmethod
    def grade(add, report_value):
        """grades the basic boolean report
            report - boolean exists result
        """
        if add:
            if report_value:
                return ':+1:'

            return ':no_entry:'

        if report_value:
            return ':no_entry:'

        return ':+1:'


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
        url = OpenDataChecker.kebab_case(item_name)

        if not url:
            raise ValueError('url cannot be empty')

        self.url = f'https://opendata.gis.utah.gov/datasets/{url}'

    @staticmethod
    def kebab_case(string):
        """returns a lowercase kebab string
        """
        if string is None:
            raise ValueError('string cannot be empty')

        return string.lower().replace(' ', '-')

    def exists(self):
        """checks if the url exists
        """
        UrlChecker.get_data(self)
        self.data = self.data.status_code

        return self.data == 200


class GSheetChecker():
    """look for a record and attributes in the stewardship worksheet
    """
    required_fields = ['Description', 'Data Source', 'Website URL', 'Data Type', 'Endpoint', 'Deprecated']
    client = None
    worksheet = None

    def __init__(self, table, sheet_id, worksheet_name, service_account_file):
        self.table = table
        if service_account_file is not None and len(service_account_file) > 1:
            self.client = pygsheets.authorize(service_account_file=service_account_file)
        self.sheet_id = sheet_id
        self.worksheet_name = worksheet_name
        self.field_index = {}

    def build_header_row_index(self, header_row):
        """builds an column index map to help with finding neighboring cells
        """
        for index, title in enumerate(header_row):
            if title in self.required_fields:
                self.field_index[title] = index

    def _get_data(self):
        """search the worksheet for the table in SGID Data Layer
        """
        self.worksheet = self.client.open_by_key(self.sheet_id).worksheet_by_title(self.worksheet_name)
        header_row = self.worksheet.get_row(1)
        self.build_header_row_index(header_row)

        return self.worksheet.find(self.table, matchEntireCell=True)

    def exists(self):
        """tests for if the row exists in the sheet
        """
        cells = self._get_data()
        SheetResponse = namedtuple('SheetResponse', 'valid messages')

        if len(cells) > 1:
            row_indexes = ', '.join([str(cell.row) for cell in cells])

            return SheetResponse(
                False, f'There are multiple items with this name on rows {row_indexes}. Please remove the duplicates.'
            )

        if len(cells) == 0:
            return SheetResponse(False, f'Did not find {self.table} in the worksheet')

        cell = cells[0]
        cell.link(self.worksheet, update=False)

        status = {}
        fields = self.field_index
        starting_position = cell.col

        for key, position in fields.items():
            status[key] = False

            delta = (0, (position + 1) - starting_position)
            value = cell.neighbour(delta).value.strip()

            if value:
                status[key] = True

        return SheetResponse(True, status)

    @staticmethod
    def grade(add, report_value):
        """grades the report
            report - SheetResponse
        """
        if add:
            if not report_value.valid:
                return f':no_entry: {report_value.messages}'

            failures = ''.join([
                f'\n| - {key} | :no_entry: |' for key in report_value.messages
                if not report_value.messages[key] and key != 'Deprecated'
            ])
            success = ''.join([
                f'\n| - {key} | :+1: |' for key in report_value.messages
                if report_value.messages[key] and key != 'Deprecated'
            ])

            return f' |{failures}{success}'.rstrip(' |').strip('\n\n')

        #: removal
        has_linked_deprecation_issue = report_value.messages['Deprecated']

        if not has_linked_deprecation_issue:
            return ' |\n| - deprecation issue link | :no_entry:'

        return ' |\n| - deprecation issue link | :+1:'


class TriageChecker:
    """verifies that triage boxes have been checked
    """

    def __init__(self, team, issue_body):
        self.team = team
        self.issue_body = issue_body

    def get_title(self):
        """return the issue label for the specific team
        """
        return f'triage - {self.team} Team'

    def exists(self):
        """parse the issue body and validate that the triage item has been checked
        """
        TriageResponse = namedtuple('TriageResponse', 'valid message')

        expression = fr'(?P<strikethrough>~?)- \[(?P<is_completed>[x| ]?)\] {self.team} Team Triage \((?P<user>@\S*)\)'
        match = re.search(expression, self.issue_body, re.MULTILINE)

        if match:
            is_complete = match.group('is_completed').strip().lower() == 'x' or len(match.group('strikethrough')) > 0
            user = match.group('user')

            message = None if is_complete else f'{user} has not yet performed triage for this issue'

            return TriageResponse(is_complete, message)

        return None

    @staticmethod
    def grade(_, report_value):
        """convert the report value into a string suitable for the report table
        """

        if report_value.valid:
            return ':+1:'

        return f':no_entry: {report_value.message}'
