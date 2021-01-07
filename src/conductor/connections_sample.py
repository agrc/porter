#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
connections.py
A module that holds connection information
"""
#: this is a template so of course it will have duplicate code
# pylint: disable-all
SECRETS = {
    'internalsgid': {
        'server': '',
        'database': '',
        'user': '',
        'password': '',
        'driver': '{ODBC Driver 17 for SQL Server}'
    },
    'opensgid': {
        'host': 'opensgid.agrc.utah.gov',
        'database': 'opensgid',
        'user': 'agrc',
        'password': 'agrc'
    },
    'github_token': 'https://github.com/settings/tokens/new with public repo access',
    'local': {
        'service_account_file': 'client-secret.json',
    },
    'dev': {
        'project_id': '746866000386',
        'secret_name': 'stewardship-sa'
    },
    'prod': {
        'project_id': '174444704019',
        'secret_name': 'stewardship-sa'
    }
}
