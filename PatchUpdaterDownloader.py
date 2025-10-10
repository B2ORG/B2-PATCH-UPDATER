import aiohttp, asyncio, os
import config as cfg
from typing import Optional
from PatchUpdaterConfig import PatchUpdaterConfig


class PatchUpdaterDownloader:
    _tempdir: PatchUpdaterConfig
    _queue: dict[str, str]

    def __init__(self):
        self._pool = asyncio.Semaphore(8)


    def set_attributes(self, **attrs):
        for attr in attrs:
            setattr(self, attr, attrs[attr])


    async def fetch_all(self):
        async with aiohttp.ClientSession(headers={"User-Agent": cfg.USER_AGENT}) as session:
            tasks = []
            for fname, url in self._queue.items():
                tasks.append(self._task_wrapper(session, url, fname))
            await asyncio.gather(*tasks)


    async def _task_wrapper(self, session: aiohttp.ClientSession, url: str, filename: Optional[str]):
        async with self._pool:
            return await self._fetch_and_save(session, url, filename)


    async def _fetch_and_save(self, session: aiohttp.ClientSession, url: str, filename: Optional[str]):
        async with session.get(url, allow_redirects=True, timeout=30) as response:
            response.raise_for_status()
            tmp = os.path.join(self._tempdir, f"{filename}.part")
            with open(tmp, "wb") as f:
                async for chunk in response.content.iter_chunked(64 * 1024):
                    if not chunk:
                        continue
                    f.write(chunk)
            os.replace(tmp, tmp.replace(".part", ".b2"))
