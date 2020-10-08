#!/usr/bin/env python
# * coding: utf8 *
"""
test_triage_checker.py
A module that contains tests for the TaskChecker module.
"""

from collections import namedtuple
from pathlib import Path

from conductor.checks import TaskChecker, get_users_task_statuses

body_mocks = {}

for name in ['simple', 'strikethrough']:
    path = Path(__file__).parent / 'data' / f'tasks_issue_body_mock_{name}.txt'
    with path.open() as file:
        body_mocks[path.stem.replace('tasks_issue_body_mock_', '')] = file.read()


def test_get_users_task_statuses():
    tasks = get_users_task_statuses(body_mocks['simple'])

    assert len(tasks) == 3
    assert tasks == [('@gregbunce', 1, 1), ('@steveoh', 2, 0), ('@rkelson', 1, 0)]

    tasks = get_users_task_statuses(body_mocks['strikethrough'])

    assert len(tasks) == 3
    assert tasks == [('@gregbunce', 3, 0), ('@steveoh', 2, 0), ('@ZachBeck', 4, 3)]


def test_get_title():
    check = TaskChecker('@user', 4, 4)

    assert check.get_title() == 'user has completed **4** out of **4** tasks'

    check = TaskChecker('@user', 4, 3)

    assert check.get_title() == '@user has completed **3** out of **4** tasks'


def test_has_completed_all_tasks():
    assert TaskChecker('@user', 4, 4).has_completed_all_tasks()
    assert not TaskChecker('@user', 4, 3).has_completed_all_tasks()


def test_grade():
    assert TaskChecker.grade(None, True) == ':+1:'
    assert TaskChecker.grade(None, False) == ':no_entry:'
