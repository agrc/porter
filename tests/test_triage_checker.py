#!/usr/bin/env python
# * coding: utf8 *
"""
test_triage_checker.py
A module that contains tests for the TriageChecker module.
"""

from collections import namedtuple
from pathlib import Path

from conductor.checks import TriageChecker

body_mocks = {}

for filename in [
    'triage_issue_body_all_completed.txt', 'triage_issue_body_strikethrough.txt', 'triage_issue_body_uncompleted.txt'
]:
    path = Path(__file__).parent / 'data' / filename
    with path.open() as file:
        body_mocks[path.stem.replace('triage_issue_body_', '')] = file.read()


def test_builds_title():
    checker = TriageChecker('Super', body_mocks['all_completed'])

    assert checker.get_title() == 'triage - Super Team'


def test_exists_completed():
    checker = TriageChecker('Dev', body_mocks['all_completed'])

    response = checker.exists()

    assert response.valid
    assert response.message == None


def test_no_team_found():
    checker = TriageChecker('Bad', body_mocks['all_completed'])

    assert checker.exists() is None


def test_uncompleted():
    checker = TriageChecker('Dev', body_mocks['uncompleted'])

    response = checker.exists()

    assert not response.valid
    assert response.message == '@steveoh has not yet performed triage for this issue'


def test_ignore_strikethrough():
    checker = TriageChecker('Cadastre', body_mocks['strikethrough'])

    response = checker.exists()

    assert response.valid
    assert response.message is None


def test_grade_fail():
    Report = namedtuple('Report', 'valid message')
    message = '@stdavis has not yet performed triage for this issue'
    report = Report(False, message)

    result = TriageChecker.grade(True, report)

    assert result == f':no_entry: {message}'


def test_grade_pass():
    Report = namedtuple('Report', 'valid message')
    message = ''
    report = Report(True, message)

    result = TriageChecker.grade(True, report)

    assert result == ':+1:'
