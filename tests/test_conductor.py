#!/usr/bin/env python
# * coding: utf8 *
"""
test_conductor
.py
A module that contains tests for the project module.
"""

from github.Issue import Issue

from conductor import conductor


def test_imports():
    assert conductor is not None


def test_can_extract_metadata_from_issue_body():
    headers = {}
    attributes = {
        'body': 'text\n<!-- some comments -->\n<!-- conductor = {"table":"schema.table","when":"2020-07-16T09:00:00.000Z"} -->\nmore text'
    }

    issue = Issue(None, headers, attributes, True)

    metadata = conductor.extract_metadata_from_issue_body(issue, notify=False)

    assert list(metadata.keys()) == ['table', 'when']


def test_extract_metadata_from_issue_body_returns_none_when_not_found():
    headers = {}
    attributes = {'body': 'text\nmore text\n<!-- some comments -->'}

    issue = Issue(None, headers, attributes, True)

    metadata = conductor.extract_metadata_from_issue_body(issue, notify=False)

    assert metadata is None


def test_notify_is_called_when_metadata_is_empty(mocker):
    mocker.patch('conductor.conductor._notify_missing_metadata')
    headers = {}
    attributes = {'body': 'text\nmore text\n<!-- some comments -->'}

    issue = Issue(None, headers, attributes, True)

    metadata = conductor.extract_metadata_from_issue_body(issue, notify=True)

    assert metadata is None

    conductor._notify_missing_metadata.assert_called_once_with(issue)
