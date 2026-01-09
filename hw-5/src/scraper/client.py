import asyncio
import logging
import random
from types import TracebackType
from typing import Optional, Dict, Type

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

logger = logging.getLogger(__name__)


class AsyncHTTPClient:
    
    DEFAULT_HEADERS: Dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    
    def __init__(
        self,
        max_concurrent: int = 3,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
        timeout: float = 30.0,
    ):
        self.max_concurrent = max_concurrent
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout = timeout
        
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._client: Optional[httpx.AsyncClient] = None
        self._last_request_time: float = 0
    
    async def __aenter__(self) -> "AsyncHTTPClient":
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        self._client = httpx.AsyncClient(
            headers=self.DEFAULT_HEADERS,
            timeout=self.timeout,
            follow_redirects=True,
        )
        return self
    
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        async with self._semaphore:
            await self._dodge_rate_limit()
            
            try:
                if headers:
                    self._client.headers.update(headers)
                
                logger.debug(f"Fetching {url}")
                text = await self._fetch(url, params)
                logger.debug(f"Successfully fetched {url}")
                return text
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    logger.error(f"Access forbidden (403) for {url}")
                else:
                    logger.error(f"HTTP error {e.response.status_code} for {url}")
                return None
                
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
                return None

    async def _dodge_rate_limit(self):
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)
        
        self._last_request_time = asyncio.get_event_loop().time()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
    )
    async def _fetch(
        self, 
        url: str, 
        params: Optional[Dict[str, str]] = None,
    ) -> str:
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.text
