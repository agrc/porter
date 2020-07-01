#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

import json
import os

import github
from dotenv import load_dotenv

from .checks import MSSql, PGSql

load_dotenv()


def startup():
    """the method called when invoking `conductor`
    """

    return main(github.Github('18a2f7bd25fbd98af0d08ee0a9f0cadeaad1f945').get_repo('agrc/porter'))


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
    check_removes(deprecations)


def check_removes(issues):
    """
    checks that items have been removed
    issues: issues with a deprecation label
    """
    for issue in issues:
        _extract_metadata_from_body(issue.body)
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
        checks = []
        metadata = _extract_metadata_from_body(issue)
        if 'table' in metadata:
            checks.append(MSSql(metadata['table'], os.getenv('sgid10')))
            checks.append(MSSql(metadata['table'], os.getenv('internalsgid')))
            checks.append(
                PGSql(
                    metadata['table'], {
                        'host': 'opensgid.agrc.utah.gov',
                        'database': 'opensgid',
                        'user': 'agrc',
                        'password': 'agrc',
                    }
                )
            )

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


def _extract_metadata_from_body(issue):
    metadata = None
    for line in issue.body.splitlines():
        if not line.startswith('<!--'):
            continue

        if 'conductor' not in line:
            continue

        start = line.index('{')
        end = line.rindex('}') + 1

        metadata = json.loads(line[start:end])

    if metadata is None:
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
