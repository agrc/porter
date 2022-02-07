#!/usr/bin/env python
# * coding: utf8 *
"""
server.py
a module that can receive web requests. this will be google cloud pub sub and
possibly github web hooks
"""

import json
import logging
import os
import sys
from pathlib import Path

from flask import Flask, request

from .conductor import startup

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@app.route('/gcp/schedule', methods=['POST'])
def schedule():
    """ schedule: the post route that gcp pub sub sends when conductor should execute
    """
    logging.debug('request accepted')
    body = request.get_json()
    logging.debug('scheduler request body: %s', body)

    if not body:
        msg = 'no message received'
        logging.error('error: %s', msg)

        return (f'Bad Request: {msg}', 400)

    secrets = json.loads(Path('/secrets/db/connection').read_text(encoding='utf-8'))
    secrets['sheets-sa'] = Path('/secrets/sheets/service-account').read_text(encoding='utf-8')

    if not isinstance(body, dict) or 'message' not in body:
        msg = 'invalid post data'
        logging.error('error: %s', msg)

        return (f'Bad Request: {msg}', 400)

    secrets = json.loads(Path('/secrets/db/connections').read_text())
    secrets['sheets-sa'] = Path('/secrets/sheets/service-account').read_text()

    try:
        startup(secrets, True)
    except Exception as error:
        logging.error('conductor failure %s', error)

        return (f'error: {error}', 500)

    logging.info('successful run')

    return ('', 204)


if __name__ == '__main__':
    PORT = int(str(os.getenv('PORT'))) if os.getenv('PORT') else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host='127.0.0.1', port=PORT, debug=True)
