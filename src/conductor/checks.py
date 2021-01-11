#!/usr/bin/env python
# * coding: utf8 *
"""
checks.py
a module with classes that check for the existence of things
"""

import json
import re
from collections import namedtuple
from pathlib import Path
from textwrap import dedent

import psycopg2
import pygsheets
import pyodbc
import requests
from google.cloud import secretmanager
from google.oauth2 import service_account


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
    sql = '''SELECT AGOL_ITEM_ID, AGOL_PUBLISHED_NAME, GEOMETRY_TYPE
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
        geometry_type = None
        MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name geometry_type')

        TableChecker.get_data(self, (self.original_table))

        if self.data is None:
            self.data = MetaResponse(False, item_id, item_name, geometry_type)

            return MetaResponse(False, item_id, item_name, geometry_type)

        item_id, item_name, geometry_type = self.data
        response = True

        if not item_id and not item_name and not geometry_type:
            return MetaResponse(False, item_id, item_name, geometry_type)

        errors = []
        if not item_id:
            errors.append('missing item id')

        if not item_name:
            errors.append('missing item name')

        if not geometry_type:
            errors.append('missing geometry type')

        if len(errors) > 0:
            response = ', '.join(errors)

        self.data = MetaResponse(response, item_id, item_name, geometry_type)

        return self.data

    @staticmethod
    def grade(add, report_value):
        """overrides the basic grading
        """
        if add:
            grade = ''
            if not report_value.item_id:
                grade += ' |\n| - item id | :no_entry: |'
            else:
                grade += ' |\n| - item id | :+1: |'

            if not report_value.item_name:
                grade += ' |\n| - item name | :no_entry: |'
            else:
                grade += ' |\n| - item name | :+1: |'

            if not report_value.geometry_type:
                grade += ' |\n| - geometry type | :no_entry: |'
            else:
                grade += ' |\n| - geometry type | :+1: |'

            grade = grade.replace('| |', '|').rstrip(' |')

            return grade

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

    def __init__(self, table, sheet_id, worksheet_name, client_builder):
        self.table = table
        self.sheet_id = sheet_id
        self.worksheet_name = worksheet_name
        self.field_index = {}
        self.client = client_builder()

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
        if not report_value.valid:
            return f':no_entry: {report_value.messages}'

        if add:
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

    @staticmethod
    def create_client_with_service_account(file_path):
        """creates a pygsheets authorized client from a service account json key
        file_path: the string path to a service account json file
        """
        path = Path(file_path)

        if not path.exists() or path.is_dir():
            raise Exception('The path to the service account file is incorrect; Could not create client.')

        return pygsheets.authorize(service_account_file=file_path)

    @staticmethod
    def create_client_with_secret_manager(project, secret_name):
        """creates a pygsheets authorized client from a secret in gcp
        project: the numeric google project number
        secret_name: the name of the secret in secret manager
        """
        client = secretmanager.SecretManagerServiceClient()
        name = client.secret_version_path(project, secret_name, 'latest')
        secrets = client.access_secret_version(name)

        if secrets is None:
            raise Exception('The project secret might not exist or is incorrect; Could not create client.')

        scopes = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
        secrets = service_account.Credentials.from_service_account_info(
            json.loads(secrets.payload.data.decode('UTF-8')), scopes=scopes
        )

        return pygsheets.authorize(custom_credentials=secrets)


class TaskChecker:
    """verifies that task boxes have been checked
    """

    def __init__(self, user, assigned, completed):
        self.user = user
        self.assigned = assigned
        self.completed = completed

    def get_title(self):
        """return a string representing the result of this check
        """

        #: don't ping a user if they have completed all of their tasks
        if self.has_completed_all_tasks():
            user = self.user[1:]
        else:
            user = self.user
        return f'{user} has completed **{self.completed}** out of **{self.assigned}** tasks'

    def has_completed_all_tasks(self):
        """check to see if the user has completed all of their tasks
        """
        return self.assigned == self.completed

    @staticmethod
    def grade(_, report_value):
        """convert the report value into a string suitable for the report table
        """

        if report_value:
            return ':+1:'

        return ':no_entry:'


def get_users_task_statuses(issue_body):
    """returns a list of tuples containing a user, the number of assigned tasks, and
    the number of completed tasks
    """
    users = {}
    expression = r'(?P<strikethrough>~?)- \[(?P<is_completed>[x| ]?)\] .* \(*?(?P<user>@..*?\b).*\)'

    for match in re.finditer(expression, issue_body, re.MULTILINE):
        user = match.group('user')
        if match.group('strikethrough') or user == '@assigned':
            continue
        is_complete = match.group('is_completed').strip().lower() == 'x' or len(match.group('strikethrough')) > 0
        users.setdefault(user, []).append(is_complete)

    tasks = []
    for user in users:
        task_results = users[user]
        tasks.append((user, len(task_results), task_results.count(True)))

    return tasks
