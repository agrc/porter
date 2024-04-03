# conductor

[![Push Events](https://github.com/agrc/porter/actions/workflows/push.yml/badge.svg)](https://github.com/agrc/porter/actions/workflows/push.yml)

a bot that checks on the existence of data and required fields

![conductor_sm](https://user-images.githubusercontent.com/325813/90076216-62563280-dcbc-11ea-8023-afa62e75b04b.png)

## Development

1. create new python environment: `python -m venv venv`
1. activate new environment: `source venv/bin/activate` (On Windows: `.env\Scripts\activate`)
1. install dependencies and editable project: `pip install -e ".[tests]"`
1. use `test_conductor` as the entry point
1. install the Microsoft ODBC driver for SQL Server for [Windows](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) or [macOS](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos)
1. create two secret files in `src/conductor/secrets`
   1. `/db/connections`

      ```json
      {
         "internalsgid": {
            "server": "",
            "database": "",
            "user": "",
            "password": "",
            "driver": "ODBC Driver 17 for SQL Server"
         },
         "opensgid": {
            "host": "",
            "database": "",
            "user": "",
            "password": ""
         },
         "github_token": "generate a [new GitHub personal access token](https://github.com/settings/tokens/new) with `public_repo`"
      }
      ```

   1. `/sheets/service-account`
      - a service account with read access to the google sheet
