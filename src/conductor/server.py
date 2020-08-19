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

from flask import Flask, request
from google.cloud import secretmanager

from .conductor import startup

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@app.route('/gcp/schedule', methods=['POST'])
def schedule():
    """ schedule: the post route that gcp pub sub sends when conductor should execute
    """
    logging.debug('request accepted')
    body = request.get_json()
    if not body:
        msg = 'no Pub/Sub message received'
        logging.error('error: %s', msg)

        return (f'Bad Request: {msg}', 400)

    if not isinstance(body, dict) or 'message' not in body:
        msg = 'invalid Pub/Sub message format'
        logging.error('error: %s', msg)

        return (f'Bad Request: {msg}', 400)

    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path('174444704019', 'conductor-connections', 'latest')
    secrets = client.access_secret_version(name)
    secrets = json.loads(secrets.payload.data.decode('UTF-8'))

    try:
        startup(secrets)
    except Exception as error:
        logging.error('conductor failure %s', error)

        return (f'error: {error}', 500)

    logging.info('successful run')

    return ('', 204)


if __name__ == '__main__':
    PORT = int(os.getenv('PORT')) if os.getenv('PORT') else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host='127.0.0.1', port=PORT, debug=True)