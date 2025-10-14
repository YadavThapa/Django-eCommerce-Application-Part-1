"""Quick script to fetch a static asset for a local dev server.

This helper is used during development to verify static file
serving (intended to be run against a local dev server).
"""

import logging
import urllib.request
from urllib.error import HTTPError, URLError

FETCH_URL = "http://127.0.0.1:8000/static/img/products/running_shoes.jpg"


LOG = logging.getLogger(__name__)

try:
    with urllib.request.urlopen(FETCH_URL, timeout=5) as r:
        data = r.read()
        LOG.info("STATUS %s", getattr(r, "status", "n/a"))
        LOG.info("LENGTH %d", len(data))
except HTTPError as e:
    LOG.error("HTTP ERROR %s %s", e.code, e.reason)
except URLError as e:
    LOG.error("URL ERROR %s", e.reason)
