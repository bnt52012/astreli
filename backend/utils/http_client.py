"""
Resilient HTTP client with automatic retry, exponential backoff,
rate limiting awareness, and request ID tracking.

Used by video generation (Kling API) and any other direct HTTP calls.
Gemini and OpenAI use their own SDK clients which handle retries internally.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Default retry configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_BASE = 2.0
DEFAULT_BACKOFF_MAX = 60.0
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class RetryTransport(httpx.AsyncBaseTransport):
    """Custom HTTPX transport that retries on transient failures.

    Implements exponential backoff with jitter for:
    - HTTP 429 (rate limit)
    - HTTP 5xx (server errors)
    - Connection errors
    - Timeout errors

    Every request gets a unique X-Request-ID header for tracing.
    """

    def __init__(
        self,
        wrapped: httpx.AsyncHTTPTransport,
        *,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_base: float = DEFAULT_BACKOFF_BASE,
        backoff_max: float = DEFAULT_BACKOFF_MAX,
        retryable_status_codes: set[int] | None = None,
    ) -> None:
        self._wrapped = wrapped
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._backoff_max = backoff_max
        self._retryable_codes = retryable_status_codes or RETRYABLE_STATUS_CODES

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        import asyncio
        import random

        # Inject request ID for tracing
        request_id = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
        request.headers["x-request-id"] = request_id

        last_exception: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._wrapped.handle_async_request(request)

                if response.status_code not in self._retryable_codes:
                    return response

                if attempt == self._max_retries:
                    logger.warning(
                        "[HTTP] Max retries reached for %s %s (status=%d, req_id=%s)",
                        request.method,
                        request.url,
                        response.status_code,
                        request_id,
                    )
                    return response

                # Check for Retry-After header
                retry_after = response.headers.get("retry-after")
                if retry_after:
                    try:
                        wait = float(retry_after)
                    except ValueError:
                        wait = self._calculate_backoff(attempt)
                else:
                    wait = self._calculate_backoff(attempt)

                logger.info(
                    "[HTTP] Retrying %s %s in %.1fs (status=%d, attempt=%d/%d, req_id=%s)",
                    request.method,
                    request.url,
                    wait,
                    response.status_code,
                    attempt + 1,
                    self._max_retries,
                    request_id,
                )
                await asyncio.sleep(wait)

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_exception = exc
                if attempt == self._max_retries:
                    logger.error(
                        "[HTTP] Connection failed after %d retries: %s %s (req_id=%s, error=%s)",
                        self._max_retries,
                        request.method,
                        request.url,
                        request_id,
                        exc,
                    )
                    raise

                wait = self._calculate_backoff(attempt)
                logger.warning(
                    "[HTTP] Connection error, retrying in %.1fs (attempt=%d/%d, req_id=%s): %s",
                    wait,
                    attempt + 1,
                    self._max_retries,
                    request_id,
                    exc,
                )
                await asyncio.sleep(wait)

        # Should not reach here, but satisfy type checker
        if last_exception:
            raise last_exception
        raise httpx.TransportError("Unexpected retry loop exit")

    def _calculate_backoff(self, attempt: int) -> float:
        """Exponential backoff with jitter."""
        import random

        base_wait = min(self._backoff_base ** attempt, self._backoff_max)
        jitter = random.uniform(0, base_wait * 0.5)
        return base_wait + jitter


def create_resilient_client(
    *,
    base_url: str = "",
    headers: dict[str, str] | None = None,
    timeout: float = 60.0,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_base: float = DEFAULT_BACKOFF_BASE,
) -> httpx.AsyncClient:
    """Create an httpx.AsyncClient with automatic retry and backoff.

    Args:
        base_url: Base URL for all requests.
        headers: Default headers for all requests.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts.
        backoff_base: Base for exponential backoff calculation.

    Returns:
        Configured httpx.AsyncClient with retry transport.
    """
    transport = RetryTransport(
        httpx.AsyncHTTPTransport(retries=0),
        max_retries=max_retries,
        backoff_base=backoff_base,
    )

    return httpx.AsyncClient(
        base_url=base_url,
        headers=headers or {},
        timeout=httpx.Timeout(timeout),
        transport=transport,
    )
