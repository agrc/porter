#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

import json
from collections import namedtuple

import github

from .checks import (
    ArcGisOnlineChecker, GSheetChecker, MetaTableChecker, MSSqlTableChecker, OpenDataChecker, PGSqlTableChecker
)

try:
    from conductor.connections import DB
except ModuleNotFoundError:
    from conductor.connection_sample import DB


def startup():
    """the method called when invoking `conductor`
    """

    reports = collect_issue_reports(github.Github().get_repo('agrc/porter', lazy=True))

    return reports


def collect_issue_reports(porter):
    """finds the issues and delegates them to the checkers
    issues will have metadata for the bot to use to check for items
    <!-- conductor = {"table":"schema.table","when":"2020-07-16T09:00:00.000Z"} -->
    """
    #: introduction or removal
    issues = porter.get_issues(state='open')

    conductor_issues = []
    ConductorIssue = namedtuple('ConductorIssue', 'issue introduction')

    for issue in issues:
        labels = [label.name for label in issue.labels]

        if (
            'introduction' in labels or 'deprecation' in labels
        ) and 'reminder' not in labels and 'scheduled' not in labels:
            conductor_issues.append(ConductorIssue(issue, 'introduction' in labels))

    return conduct_check(conductor_issues)


def conduct_check(conductor_issues):
    """
    checks that the data has been added to the expected areas
    conductor_issues: a named tuple with the issue and a introduction label boolean
    """
    reports = {}

    for issue in conductor_issues:
        Report = namedtuple('Report', 'check introduction result')
        metadata = extract_metadata_from_issue_body(issue.issue, notify=False)

        if 'table' in metadata:
            table = metadata['table']
            reports[table] = []

            check = MSSqlTableChecker(table, DB['internalsgid'])
            reports[table].append(Report('internal sgid', issue.introduction, check.exists()))

            check = MSSqlTableChecker(table, DB['sgid10'])
            reports[table].append(Report('sgid10', check.exists()))

            check = MetaTableChecker(f'sgid.{metadata["table"]}', DB['internalsgid'])
            reports[table].append(Report('meta table', issue.introduction, check.exists()))
            meta_table_data = check.data

            if meta_table_data.exists != 'missing item name':
                check = PGSqlTableChecker(table, DB['opensgid'])
                check.table = PGSqlTableChecker.postgresize(meta_table_data.item_name)

                reports[table].append(Report('open sgid', issue.introduction, check.exists()))

                check = OpenDataChecker(meta_table_data.item_name)
                reports[table].append(Report('open data', issue.introduction, check.exists()))

            if meta_table_data.exists != 'missing item id':
                check = ArcGisOnlineChecker(meta_table_data.item_id)
                reports[table].append(Report('arcgis online', issue.introduction, check.exists()))

            check = GSheetChecker(table, '11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ', 'SGID Stewardship Info')
            reports[table].append(Report('stewardship', issue.introduction, check.exists()))

    return reports


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


if __name__ == '__main__':
    github.enable_console_debug_logging()
    results = startup()

    #: pass in issue id
    #: use some metadata from the issue id to find the item being removed
    #: if it's an sgid table run the results
    #: otherwise these checks may not apply

    #: check results
    #: post comment on github issue
