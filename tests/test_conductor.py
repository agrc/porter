#!/usr/bin/env python
# * coding: utf8 *
"""
test_conductor
.py
A module that contains tests for the project module.
"""

from collections import namedtuple

from github.Issue import Issue
from github.Label import Label
from github.Requester import Requester

from conductor import conductor
from conductor.checks import GSheetChecker, MetaTableChecker, TableChecker, UrlChecker
from conductor.connections_sample import SECRETS

REQUESTER = Requester('token', None, None, 'http://gis.utah.gov', 0, 'client-id', 'secret', '', 1, False, {})


def noop():
    pass


SECRETS['client_builder'] = noop


def test_imports():
    assert conductor is not None


def test_can_extract_metadata_from_issue_body():
    headers = {}
    attributes = {
        'body': 'text\n<!-- some comments -->\n<!-- conductor = {"table":"schema.table","when":"2020-07no_entry6T09:00:00.000Z"} -->\nmore text'
    }

    issue = Issue(REQUESTER, headers, attributes, True)

    metadata = conductor.extract_metadata_from_issue_body(issue, notify=False)

    assert list(metadata.keys()) == ['table', 'when']


def test_extract_metadata_from_issue_body_returns_none_when_not_found():
    headers = {}
    attributes = {'body': 'text\nmore text\n<!-- some comments -->'}

    issue = Issue(REQUESTER, headers, attributes, True)

    metadata = conductor.extract_metadata_from_issue_body(issue, notify=False)

    assert metadata is None


def test_notify_is_called_when_metadata_is_empty(mocker):
    mocker.patch('conductor.conductor._notify_missing_metadata')
    headers = {}
    attributes = {'body': 'text\nmore text\n<!-- some comments -->'}

    issue = Issue(REQUESTER, headers, attributes, True)

    metadata = conductor.extract_metadata_from_issue_body(issue, notify=True)

    assert metadata is None

    conductor._notify_missing_metadata.assert_called_once_with(issue)


def test_publish_grades_formats_table(mocker):
    Grade = namedtuple('Grade', 'check grade issue')

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('check', 'grade', issue)]}, True)

    spy.assert_called_once_with(
        '## conductor results for table.name\n\n| check | status |\n| - | :-: |\n| check | grade |'
    )


def test_publish_sheets_integration_test_add_mixed(mocker):
    SheetResponse = namedtuple('SheetResponse', 'valid messages')
    Grade = namedtuple('Grade', 'check grade issue')

    grades = {
        'Description': False,
        'Data Source': True,
        'Deprecated': False,
    }
    grade = GSheetChecker('fake.table', 'id', 'name', noop).grade(add=True, report_value=SheetResponse(True, grades))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('sheetchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| sheetchecker |  |
| - Description | :no_entry: |
| - Data Source | :+1: |'''
    )


def test_publish_sheets_integration_test_add_all_success(mocker):
    SheetResponse = namedtuple('SheetResponse', 'valid messages')
    Grade = namedtuple('Grade', 'check grade issue')

    grades = {
        'Description': True,
        'Data Source': True,
        'Deprecated': False,
    }
    grade = GSheetChecker('fake.table', 'id', 'name', noop).grade(add=True, report_value=SheetResponse(True, grades))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('sheetchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| sheetchecker |  |
| - Description | :+1: |
| - Data Source | :+1: |'''
    )


def test_publish_sheets_integration_test_add_all_fail(mocker):
    SheetResponse = namedtuple('SheetResponse', 'valid messages')
    Grade = namedtuple('Grade', 'check grade issue')

    grades = {
        'Description': False,
        'Data Source': False,
        'Deprecated': False,
    }
    grade = GSheetChecker('fake.table', 'id', 'name', noop).grade(add=True, report_value=SheetResponse(True, grades))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('sheetchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| sheetchecker |  |
| - Description | :no_entry: |
| - Data Source | :no_entry: |'''
    )


def test_publish_sheets_integration_test_remove_all_fail(mocker):
    SheetResponse = namedtuple('SheetResponse', 'valid messages')
    Grade = namedtuple('Grade', 'check grade issue')

    grades = {
        'Description': True,
        'Data Source': True,
        'Deprecated': False,
    }
    grade = GSheetChecker('fake.table', 'id', 'name', noop).grade(add=False, report_value=SheetResponse(True, grades))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('sheetchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| sheetchecker |  |
| - deprecation issue link | :no_entry: |'''
    )


def test_publish_sheets_integration_test_remove_all_pass(mocker):
    SheetResponse = namedtuple('SheetResponse', 'valid messages')
    Grade = namedtuple('Grade', 'check grade issue')

    grades = {
        'Description': True,
        'Data Source': True,
        'Deprecated': True,
    }
    grade = GSheetChecker('fake.table', 'id', 'name', noop).grade(add=False, report_value=SheetResponse(True, grades))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('sheetchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| sheetchecker |  |
| - deprecation issue link | :+1: |'''
    )


def test_url_checker_grade_integration_add_success(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = UrlChecker().grade(add=True, report_value=True)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('urlchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| urlchecker | :+1: |'''
    )


def test_url_checker_grade_integration_add_fail(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = UrlChecker().grade(add=True, report_value=False)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('urlchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| urlchecker | :no_entry: |'''
    )


def test_url_checker_grade_integration_remove_success(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = UrlChecker().grade(add=False, report_value=False)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('urlchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| urlchecker | :+1: |'''
    )


def test_url_checker_grade_integration_remove_fail(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = UrlChecker().grade(add=False, report_value=True)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('urlchecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| urlchecker | :no_entry: |'''
    )


def test_table_checker_grade_integration_add_success(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = TableChecker('table.name', {}).grade(add=True, report_value=True)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('tablechecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| tablechecker | :+1: |'''
    )


def test_table_checker_grade_integration_add_fail(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = TableChecker('table.name', {}).grade(add=True, report_value=False)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('tablechecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| tablechecker | :no_entry: |'''
    )


def test_table_checker_grade_integration_remove_success(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = TableChecker('table.name', {}).grade(add=False, report_value=False)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('tablechecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| tablechecker | :+1: |'''
    )


def test_table_checker_grade_integration_remove_fail(mocker):
    Grade = namedtuple('Grade', 'check grade issue')
    grade = TableChecker('table.name', {}).grade(add=False, report_value=True)

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('tablechecker', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| tablechecker | :no_entry: |'''
    )


def test_metatable_checker_grade_integration_add_success(mocker):
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    Grade = namedtuple('Grade', 'check grade issue')
    grade = MetaTableChecker('table.name', {}).grade(add=True, report_value=MetaResponse(True, 'item id', 'item name'))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('meta table', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| meta table |  |
| - item id | :+1: |
| - item name | :+1: |'''
    )


def test_metatable_checker_grade_integration_add_mixed(mocker):
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    Grade = namedtuple('Grade', 'check grade issue')
    grade = MetaTableChecker('table.name', {}).grade(add=True, report_value=MetaResponse(True, None, 'item name'))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('meta table', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| meta table |  |
| - item id | :no_entry: |
| - item name | :+1: |'''
    )


def test_metatable_checker_grade_integration_add_mixed_2(mocker):
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    Grade = namedtuple('Grade', 'check grade issue')
    grade = MetaTableChecker('table.name', {}).grade(add=True, report_value=MetaResponse(True, 'item id', None))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('meta table', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| meta table |  |
| - item id | :+1: |
| - item name | :no_entry: |'''
    )


def test_metatable_checker_grade_integration_add_fail(mocker):
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    Grade = namedtuple('Grade', 'check grade issue')
    grade = MetaTableChecker('table.name', {}).grade(add=True, report_value=MetaResponse(True, None, None))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('meta table', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| meta table |  |
| - item id | :no_entry: |
| - item name | :no_entry: |'''
    )


def test_metatable_checker_grade_integration_remove_success(mocker):
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    Grade = namedtuple('Grade', 'check grade issue')
    grade = MetaTableChecker('table.name', {}).grade(add=False, report_value=MetaResponse(False, None, None))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('meta table', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| meta table | :+1: |'''
    )


def test_metatable_checker_grade_integration_remove_fail(mocker):
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    Grade = namedtuple('Grade', 'check grade issue')
    grade = MetaTableChecker('table.name', {}).grade(add=False, report_value=MetaResponse(True, None, None))

    attributes = {}
    issue = Issue(REQUESTER, {}, attributes, True)
    issue.create_comment = spy = mocker.MagicMock()

    conductor.publish_grades({'table.name': [Grade('meta table', grade, issue)]}, True)

    spy.assert_called_once_with(
        '''## conductor results for table.name

| check | status |
| - | :-: |
| meta table | :no_entry: |'''
    )


def test_grade_report(mocker):
    Report = namedtuple('Report', 'check issue report grader')
    Grade = namedtuple('Grade', 'check grade issue')
    ConductorIssue = namedtuple('ConductorIssue', 'issue introduction')

    issue = ConductorIssue(Issue(REQUESTER, {}, {}, True), True)

    grader = mocker.MagicMock(return_value='pass')

    grades = conductor.grade_reports({'table.name': [Report('check 1', issue, True, grader)]})

    grader.assert_called_once_with(True, True)
    assert len(grades) == 1
    assert grades['table.name'][0] == Grade('check 1', 'pass', issue.issue)


def test_gather_issues(mocker):
    porter = mocker.Mock(**{'get_issues.return_value': []})

    issues = conductor.gather_issues(porter)

    assert len(issues) == 0


def test_gather_issues_skips_reminders(mocker):
    reminder_issue = mocker.Mock(
        **{
            'title': 'issue with reminder',
            'labels': [Label(REQUESTER, {}, {'name': 'reminder'}, True)],
        }
    )

    schedule_issue = mocker.Mock(
        **{
            'title': 'issue with schedule',
            'labels': [Label(REQUESTER, {}, {'name': 'scheduled'}, True)],
        }
    )

    porter = mocker.Mock(**{'get_issues.return_value': [reminder_issue, schedule_issue]})

    issues = conductor.gather_issues(porter)

    assert len(issues) == 0


def test_gather_issues_skips_blocked(mocker):
    title = 'this should be included'
    issue = mocker.Mock(**{
        'title': title,
        'labels': [Label(REQUESTER, {}, {'name': 'introduction'}, True)],
    })

    skip_issue = mocker.Mock(
        **{
            'title': 'this should be skipped',
            'labels': [
                Label(REQUESTER, {}, {'name': 'introduction'}, True),
                Label(REQUESTER, {}, {'name': 'blocked'}, True)
            ],
        }
    )

    porter = mocker.Mock(**{'get_issues.return_value': [issue, skip_issue]})

    issues = conductor.gather_issues(porter)

    assert len(issues) == 1
    assert issues[0].issue.title == title


def test_gather_issues_skips_find_introductions_and_deprecations(mocker):
    reminder_issue = mocker.Mock(
        **{
            'title': 'issue with reminder',
            'labels': [Label(REQUESTER, {}, {'name': 'reminder'}, True)],
        }
    )

    schedule_issue = mocker.Mock(
        **{
            'title': 'issue with schedule',
            'labels': [Label(REQUESTER, {}, {'name': 'scheduled'}, True)],
        }
    )

    introduction_issue = mocker.Mock(
        **{
            'title': 'issue with introduction',
            'labels': [Label(REQUESTER, {}, {'name': 'introduction'}, True)],
        }
    )

    deprecation_issue = mocker.Mock(
        **{
            'title': 'issue with deprecation',
            'labels': [Label(REQUESTER, {}, {'name': 'deprecation'}, True)],
        }
    )

    other_issue = mocker.Mock(
        **{
            'title': 'issue with other',
            'labels': [Label(REQUESTER, {}, {'name': 'other'}, True)],
        }
    )

    porter = mocker.Mock(
        **{
            'get_issues.return_value': [
                deprecation_issue,
                reminder_issue,
                introduction_issue,
                schedule_issue,
                other_issue,
            ]
        }
    )

    issues = conductor.gather_issues(porter)

    assert len(issues) == 2


def test_write_report(mocker):
    GitHubIssue = namedtuple('GitHubIssue', 'body number title')
    ConductorIssue = namedtuple('ConductorIssue', 'issue introduction')
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    SheetResponse = namedtuple('SheetResponse', 'valid messages')

    conductor.extract_metadata_from_issue_body = mocker.MagicMock(
        side_effect=[None, {
            'no table': ''
        }, {
            'table': 'fake.table'
        }]
    )

    mocker.patch('conductor.checks.MSSqlTableChecker.exists', return_value=True)
    mocker.patch('conductor.checks.PGSqlTableChecker.exists', return_value=True)
    mocker.patch('conductor.checks.OpenDataChecker.exists', return_value=True)
    mocker.patch('conductor.checks.ArcGisOnlineChecker.exists', return_value=True)
    mocker.patch('conductor.checks.GSheetChecker.__init__', return_value=None)
    mocker.patch(
        'conductor.checks.GSheetChecker.exists',
        return_value=SheetResponse(True, {
            'Data source': True,
            'Deprecation': False,
        })
    )

    mocker.patch('conductor.checks.MetaTableChecker.exists', return_value=MetaResponse(True, 'item_id', 'item_name'))
    mock = mocker.patch('conductor.checks.MetaTableChecker.data', new_callable=mocker.PropertyMock)
    mock.return_value = MetaResponse(True, 'item_id', 'item_name')

    reports = conductor.write_reports([
        ConductorIssue(GitHubIssue('issue body text', 1, 'issue title'), True),
        ConductorIssue(GitHubIssue('issue body text', 1, 'issue title'), True),
        ConductorIssue(GitHubIssue('issue body text', 1, 'issue title'), True)
    ], SECRETS)

    assert len(reports) == 1
    assert len(reports['fake.table']) == 7


def test_write_report_without_item_id(mocker):
    GitHubIssue = namedtuple('GitHubIssue', 'body number title')
    ConductorIssue = namedtuple('ConductorIssue', 'issue introduction')
    MetaResponse = namedtuple('MetaResponse', 'exists item_id item_name')
    SheetResponse = namedtuple('SheetResponse', 'valid messages')

    conductor.extract_metadata_from_issue_body = mocker.MagicMock(
        side_effect=[None, {
            'no table': ''
        }, {
            'table': 'fake.table'
        }]
    )

    mocker.patch('conductor.checks.MSSqlTableChecker.exists', return_value=True)
    mocker.patch('conductor.checks.PGSqlTableChecker.exists', return_value=True)
    mocker.patch('conductor.checks.OpenDataChecker.exists', return_value=True)
    mocker.patch('conductor.checks.ArcGisOnlineChecker.exists', return_value=True)
    mocker.patch('conductor.checks.TaskChecker.has_completed_all_tasks', return_value=True)
    mocker.patch('conductor.checks.GSheetChecker.__init__', return_value=None)
    mocker.patch(
        'conductor.checks.GSheetChecker.exists',
        return_value=SheetResponse(True, {
            'Data source': True,
            'Deprecation': False,
        })
    )

    mocker.patch('conductor.checks.MetaTableChecker.exists', return_value=MetaResponse(False, None, None))
    mock = mocker.patch('conductor.checks.MetaTableChecker.data', new_callable=mocker.PropertyMock)
    mock.return_value = MetaResponse('missing item id', None, 'Name')

    reports = conductor.write_reports([
        ConductorIssue(GitHubIssue('issue body text', 1, 'issue title'), True),
        ConductorIssue(GitHubIssue('issue body text', 1, 'issue title'), True),
        ConductorIssue(GitHubIssue('issue body text', 1, 'issue title'), True)
    ], SECRETS)

    assert len(reports) == 1
    assert len(reports['fake.table']) == 6


def test_startup_with_no_issues_returns(mocker):
    mocker.patch('conductor.conductor.gather_issues', return_value=[])
    write_reports = mocker.patch('conductor.conductor.write_reports')

    conductor.startup({'github_token': ''}, False)

    write_reports.assert_not_called()


def test_startup(mocker):
    mocker.patch('conductor.conductor.gather_issues', return_value=[{}])
    write_reports = mocker.patch('conductor.conductor.write_reports')
    grade_reports = mocker.patch('conductor.conductor.grade_reports')
    publish_grades = mocker.patch('conductor.conductor.publish_grades')

    conductor.startup({'github_token': ''}, False)

    write_reports.assert_called_once()
    grade_reports.assert_called_once()
    publish_grades.assert_called_once()
