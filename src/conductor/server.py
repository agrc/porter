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

from flask import Flask

from .conductor import startup

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@app.route("/gcp/schedule", methods=["POST"])
def schedule():
    """schedule: the post route that gcp pub sub sends when conductor should execute"""
    logging.debug("request accepted")

    secrets = json.loads(Path("/secrets/db/connection").read_text(encoding="utf-8"))
    secrets["sheets-sa"] = Path("/secrets/sheets/service-account").read_text(encoding="utf-8")

    is_production = True
    if "PORTER_DEVELOPMENT" in os.environ:
        is_production = False

    try:
        startup(secrets, is_production)
    except Exception as error:
        logging.error("conductor failure %s", error)

        return (f"error: {error}", 500)

    logging.info("successful run")

    return ("", 204)


if __name__ == "__main__":
    PORT = int(str(os.getenv("PORT"))) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
