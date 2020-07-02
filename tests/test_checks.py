#!/usr/bin/env python
# * coding: utf8 *
"""
test_checks.py
A module that contains tests for the checks module.
"""

import psycopg2
import pytest

from conductor.checks import Checker, MSSql, PGSql

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
    table = 'some.incorrect.table.name'

    with pytest.raises(ValueError):
        Checker(table, CONNECTION_STRING)


def test_mssql_raises_with_empty_connection_string():
    with pytest.raises(ValueError):
        MSSql('table', '').connect()


def test_pgsql_raises_with_empty_connection_string():
    with pytest.raises(ValueError):
        PGSql('table', None).connect()


def test_open_sgid_can_connect():
    patient = PGSql(
        'boundaries.municipalities', {
            'host': 'opensgid.agrc.utah.gov',
            'database': 'opensgid',
            'user': 'agrc',
            'password': 'agrc',
        }
    )

    cursor = patient.connect()

    assert cursor.connection.status == psycopg2.extensions.STATUS_READY

    cursor.close()
    patient.connection.close()


def test_pgsql_table_exists_returns_true():
    patient = PGSql(
        'boundaries.municipal_boundaries', {
            'host': 'opensgid.agrc.utah.gov',
            'database': 'opensgid',
            'user': 'agrc',
            'password': 'agrc',
        }
    )

    assert patient.exists() == True

    patient.connection.close()


def test_pgsql_table_does_not_exists_returns_false():
    patient = PGSql(
        'fake.table', {
            'host': 'opensgid.agrc.utah.gov',
            'database': 'opensgid',
            'user': 'agrc',
            'password': 'agrc',
        }
    )

    assert patient.exists() == False

    patient.connection.close()
