#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

import json

import github

from .checks import ArcGisOnlineChecker, MetaTableChecker, MSSqlTableChecker, OpenDataChecker, PGSqlTableChecker

try:
    from conductor.connections import DB
except ModuleNotFoundError:
    from conductor.connection_sample import DB


def startup():
    """the method called when invoking `conductor`
    """

    return main(github.Github().get_repo('agrc/porter', lazy=True))


def main(porter):
    """finds the issues and delegates them to the checkers
    issues will have metadata for the bot to use to check for items
    <!-- conductor = {"table":"schema.table","when":"2020-07-16T09:00:00.000Z"} -->
    """
    #: introduction or removal
    issues = porter.get_issues(state='open')

    introductions = []
    deprecations = []

    for issue in issues:
        labels = [label.name for label in issue.labels]

        if 'introduction' in labels and 'reminder' not in labels and 'scheduled' not in labels:
            introductions.append(issue)
        elif 'deprecation' in labels and 'reminder' not in labels and 'scheduled' not in labels:
            deprecations.append(issue)

    check_adds(introductions)
    # check_removes(deprecations)


def check_removes(issues):
    """
    checks that items have been removed
    issues: issues with a deprecation label
    """
    for issue in issues:
        extract_metadata_from_issue_body(issue.body)
    #: is the service in agol

    #: is the open data page still active

    #: is the table in the internal sgid

    #: is the record in the agol items table

    #: is the recrod in the change detection table

    #: is the table in the external sgid

    #: is the table in the open sgid

    #: has the cemetery link been added to the stewardship sheet


def check_adds(issues):
    """
    checks that the data has been added to the expected areas
    issues: issues with the introduction label
    """
    for issue in issues:
        report = {}
        metadata = extract_metadata_from_issue_body(issue, notify=False)

        if 'table' in metadata:
            check = MSSqlTableChecker(metadata['table'], DB['internalsgid'])
            report['internal sgid'] = check.exists()

            check = MSSqlTableChecker(metadata['table'], DB['sgid10'])
            report['sgid10'] = check.exists()

            check = MetaTableChecker(f'sgid.{metadata["table"]}', DB['internalsgid'])
            report['meta table'] = check.exists()
            meta_table_data = check.data

            if meta_table_data.exists != 'missing item name':
                check = PGSqlTableChecker(metadata['table'], DB['opensgid'])
                check.table = PGSqlTableChecker.postgresize(meta_table_data.item_name)

                report['open sgid'] = check.exists()

                check = OpenDataChecker(meta_table_data.item_name)
                report['open data'] = check.exists()

            if meta_table_data.exists != 'missing item id':
                check = ArcGisOnlineChecker(meta_table_data.item_id)
                report['arcgis online'] = check.exists()

        print(report)

    #: search for service in agol
    #: is it shared properly etc

    #: is the open data page created

    #: is the table in the internal sgid

    #: is the record in the agol items table

    #: is the recrod in the change detection table

    #: is the table in the external sgid

    #: is the table in the open sgid

    #: is there a record in the stewardship sheet
    #: are some of the fields populated


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
