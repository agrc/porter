#!/usr/bin/env python
# * coding: utf8 *
"""
test_checks.py
A module that contains tests for the checks module.
"""

import psycopg2
import pytest

from conductor.checks import Checker, MSSql, PGSql
from conductor.connections import DB

CONNECTION_STRING = ''


def test_imports():
    assert True


def test_checker_raises_for_table_without_schema():
    with pytest.raises(ValueError):
        table = 'city'
        Checker(table, CONNECTION_STRING)


def test_checker_parses_table_with_schema():
    table = 'location.city'
    patient = Checker(table, CONNECTION_STRING)

    assert patient.table == 'city'
    assert patient.schema == 'location'


def test_checker_parses_table_with_schema_and_db():
    table = 'dbo.location.city'
    patient = Checker(table, CONNECTION_STRING)

    assert patient.table == 'city'
    assert patient.schema == 'location'


def test_checker_raises_with_too_many_parts():
    table = 'some.very.long.table.name'

    with pytest.raises(ValueError):
        Checker(table, CONNECTION_STRING)


def test_checker_raises_with_empty_connection_string():
    with pytest.raises(ValueError):
        Checker('schema.table', '').connect()


def test_checker_raises_with_no_connection_string():
    with pytest.raises(ValueError):
        Checker('schema.table', None).connect()


def test_open_sgid_can_connect():
    patient = PGSql('boundaries.municipal_boundaries', DB['opensgid'])

    cursor = patient.connect()

    assert cursor.connection.status == psycopg2.extensions.STATUS_READY

    cursor.close()
    patient.connection.close()


@pytest.mark.vpn
def test_mssql_table_can_connect():
    patient = MSSql('boundaries.municipalities', DB['sgid10'])

    cursor = patient.connect()

    assert cursor is not None


def test_pgsql_table_exists_returns_true():
    patient = PGSql('boundaries.municipal_boundaries', DB['opensgid'])

    assert patient.exists() == True

    patient.connection.close()


@pytest.mark.vpn
def test_mssql_table_exists_returns_true():
    patient = MSSql('boundaries.municipalities', DB['sgid10'])

    assert patient.exists() == True

    patient.connection.close()


def test_pgsql_table_does_not_exist_returns_false():
    patient = PGSql('fake.table', DB['opensgid'])

    assert patient.exists() == False

    patient.connection.close()


@pytest.mark.vpn
def test_mssql_table_does_not_exist_returns_false():
    patient = MSSql('fake.table', DB['sgid10'])

    assert patient.exists() == False

    patient.connection.close()
