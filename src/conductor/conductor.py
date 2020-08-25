#!/usr/bin/env python
# * coding: utf8 *
"""
conductor.py a script that interacts with github issues, reads some metadata from the issue description,
searchings our SGID facets for the item in the metadata, and finally posts a comment with the completeness
"""

import json
from collections import namedtuple

import github
from colorama import Fore, init

from .checks import (
    ArcGisOnlineChecker, GSheetChecker, MetaTableChecker, MSSqlTableChecker, OpenDataChecker, PGSqlTableChecker
)


def startup(secrets):
    """the method called when invoking `conductor`
       secrets: a dictionary with the secrets
    """
    init()
    print('gathering issues...')

    issues = gather_issues(github.Github(secrets['github_token']).get_repo('agrc/porter', lazy=True))
    print(f'collected {Fore.MAGENTA}{len(issues)}{Fore.RESET} issues')

    if len(issues) == 0:
        print(f'{Fore.MAGENTA}finished{Fore.RESET}')
        return None

    reports = write_reports(issues, secrets)
    print(f'{Fore.BLUE}all tickets punched{Fore.RESET}')

    grades = grade_reports(reports)
    print('finished grading reports')

    publish_grades(grades)
    print(f'{Fore.MAGENTA}finished{Fore.RESET}')

    return grades


def gather_issues(porter):
    """finds the issues and delegates them to the checkers
    issues will have metadata for the bot to use to check for items
    <!-- conductor = {"table":"schema.table","when":"2020-07-16T09:00:00.000Z"} -->
    """
    issues = porter.get_issues(state='open')

    conductor_issues = []
    ConductorIssue = namedtuple('ConductorIssue', 'issue introduction')

    for issue in issues:
        labels = [label.name for label in issue.labels]
        introduction = False
        capture = False

        if 'reminder' in labels:
            continue
        if 'scheduled' in labels:
            continue

        if 'introduction' in labels:
            introduction = True
            capture = True
        elif 'deprecation' in labels:
            introduction = False
            capture = True

        if not capture:
            continue

        print(f'collecting {Fore.CYAN}{issue.title}{Fore.RESET}')
        conductor_issues.append(ConductorIssue(issue, introduction))

    return conductor_issues


def write_reports(conductor_issues, secrets):
    """
    checks that the data has been added to the expected areas
    conductor_issues: a named tuple with the issue and a introduction label boolean
    """
    reports = {}

    for issue in conductor_issues:
        Report = namedtuple('Report', 'check issue report grader')
        metadata = extract_metadata_from_issue_body(issue.issue, notify=False)

        if metadata is None:
            print(f'could not find metadata in {Fore.YELLOW}{issue.issue.title}{Fore.RESET}')
            continue

        if 'table' in metadata:
            table = metadata['table']
            print(f'punching ticket for {Fore.CYAN}{table}{Fore.RESET}')
            reports[table] = []

            check = MSSqlTableChecker(table, secrets['internalsgid'])
            reports[table].append(Report('internal sgid', issue, check.exists(), MSSqlTableChecker.grade))
            print(f'{Fore.GREEN}internal sgid{Fore.RESET} punched')

            check = MSSqlTableChecker(table, secrets['sgid10'])
            reports[table].append(Report('sgid10', issue, check.exists(), MSSqlTableChecker.grade))
            print(f'{Fore.GREEN}sgid 10{Fore.RESET} punched')

            check = MetaTableChecker(f'sgid.{metadata["table"]}', secrets['internalsgid'])
            reports[table].append(Report('meta table', issue, check.exists(), MetaTableChecker.grade))
            meta_table_data = check.data
            print(f'{Fore.GREEN}meta table{Fore.RESET} punched')

            if meta_table_data.exists:
                if meta_table_data.exists != 'missing item name':
                    check = PGSqlTableChecker(table, secrets['opensgid'])
                    check.table = PGSqlTableChecker.postgresize(meta_table_data.item_name)
                    reports[table].append(Report('open sgid', issue, check.exists(), PGSqlTableChecker.grade))
                    print(f'{Fore.GREEN}open sgid{Fore.RESET} punched')

                    check = OpenDataChecker(meta_table_data.item_name)
                    reports[table].append(Report('open data', issue, check.exists(), OpenDataChecker.grade))
                    print(f'{Fore.GREEN}open data{Fore.RESET} punched')

                if meta_table_data.exists != 'missing item id':
                    check = ArcGisOnlineChecker(meta_table_data.item_id)
                    reports[table].append(Report('arcgis online', issue, check.exists(), ArcGisOnlineChecker.grade))
                    print(f'{Fore.GREEN}arcgis online{Fore.RESET} punched')

            check = GSheetChecker(table, '11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ', 'SGID Stewardship Info')
            reports[table].append(Report('stewardship', issue, check.exists(), GSheetChecker.grade))
            print(f'{Fore.GREEN}stewardship sheet{Fore.RESET} punched')

    return reports


def grade_reports(all_reports):
    """turns the reports into actionable items that can be added to the issues as comments
       reports: [namedtuple('Report', 'check ConductorIssue report')]
    """

    grades = {}
    Grade = namedtuple('Grade', 'check grade issue')

    for table, reports in all_reports.items():
        grades[table] = []
        for report in reports:
            git_issue, is_introduction = report.issue

            grades[table].append(Grade(report.check, report.grader(is_introduction, report.report), git_issue))

    return grades


def publish_grades(all_grades):
    """adds a comment to the issue with the grades
        all_grades: dict table: [Grade(check grade issue)]
    """
    comments = []
    for _, grades in all_grades.items():
        issue = grades[0].issue
        comment_table = '| check | status |\n| - | :-: |\n'
        comment = '\n'.join([f'| {grade.check} | {grade.grade} |' for grade in grades])
        comments.append(f'## conductor results\n\n{comment_table}{comment}')

        issue.create_comment(f'## conductor results\n\n{comment_table}{comment}')

        print(f'comment left on issue {Fore.CYAN}{issue.title}{Fore.RESET}')

    return comments


def extract_metadata_from_issue_body(issue, notify=True):
    """extracts conductor metadata from an issue body
    """
    metadata = None
    for line in issue.body.splitlines():
        if not line.startswith('<!--'):
            continue

        if 'conductor' not in line:
            continue

        start = line.index('{')
        end = line.rindex('}') + 1

        metadata = json.loads(line[start:end])

    if notify and metadata is None:
        _notify_missing_metadata(issue)

    return metadata


def _notify_missing_metadata(issue):
    """leave a comment on an issue and add a label
    """
    issue.add_to_labels('missing-metadata')


def local():
    """a way to access local secrets to run conductor locally
    """
    print('starting conductor...')

    try:
        from .connections import SECRETS  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        from .connection_sample import SECRETS  # pylint: disable=import-outside-toplevel
        print('secrets not found')

    github.enable_console_debug_logging()
    startup(SECRETS)
