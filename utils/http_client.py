"""
Resilient HTTP client with retry, exponential backoff, timeouts.
"""
from __future__ import annotations

import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 60
_DEFAULT_RETRIES = 3
_BACKOFF_FACTOR = 1.0
_RETRY_STATUS_CODES = [429, 500, 502, 503, 504]


def create_session(
    retries: int = _DEFAULT_RETRIES,
    backoff_factor: float = _BACKOFF_FACTOR,
    status_forcelist: list[int] | None = None,
    timeout: int = _DEFAULT_TIMEOUT,
) -> requests.Session:
    """Create a requests.Session with retry and backoff."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist or _RETRY_STATUS_CODES,
        allowed_methods=["GET", "POST", "PUT", "DELETE"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.timeout = timeout
    return session


class APIClient:
    """Wrapper around a resilient session for specific API endpoints."""

    def __init__(self, base_url: str, api_key: str, timeout: int = _DEFAULT_TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = create_session(timeout=timeout)
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def post(self, endpoint: str, json_data: dict, timeout: int | None = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        t = timeout or self.timeout
        logger.debug("POST %s (timeout=%ds)", url, t)
        resp = self.session.post(url, json=json_data, timeout=t)
        if resp.status_code == 401:
            raise requests.exceptions.HTTPError(f"401 Unauthorized for {url}", response=resp)
        if resp.status_code == 429:
            logger.warning("Rate limited (429) on %s", url)
        return resp

    def get(self, endpoint: str, timeout: int | None = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        t = timeout or self.timeout
        logger.debug("GET %s (timeout=%ds)", url, t)
        resp = self.session.get(url, timeout=t)
        return resp

    def download_file(self, url: str, dest: str, min_size: int = 1024) -> str:
        """Download file with verification."""
        logger.info("Downloading %s -> %s", url, dest)
        resp = self.session.get(url, stream=True, timeout=self.timeout)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        import os
        size = os.path.getsize(dest)
        if size < min_size:
            raise IOError(f"Downloaded file too small ({size} bytes < {min_size}): {dest}")
        logger.info("Downloaded %s (%d bytes)", dest, size)
        return dest
