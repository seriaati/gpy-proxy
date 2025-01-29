import genshin
from pydantic import BaseModel
import typing
import aiohttp
import random
import asyncio

MAX_RETRIES = 3
BACKOFF_FACTOR = 2
MAX_BACKOFF = 32


class GenshinClient(genshin.Client):
    async def request(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        attempt = 0
        err: Exception | None = None

        while attempt < MAX_RETRIES:
            try:
                return await super().request(*args, **kwargs)
            except (TimeoutError, aiohttp.ClientError) as e:
                # Attempt to retry request
                err = e
                attempt += 1

                backoff_time = min(
                    BACKOFF_FACTOR**attempt + random.uniform(0, 1), MAX_BACKOFF
                )
                await asyncio.sleep(backoff_time)
            except Exception:
                # Raise immediately for other exceptions
                raise

        msg = f"genshin.py client request failed after {MAX_RETRIES} attempts"
        raise RuntimeError(msg) from err


class BaseAPIRequest(BaseModel):
    cookies: str
    lang: str
    region: str
    game: str
    uid: int

    def get_client(self) -> genshin.Client:
        return GenshinClient(
            self.cookies,
            lang=self.lang,
            region=genshin.Region(self.region),
            game=genshin.Game(self.game),
            uid=self.uid,
        )


class MimoRequest(BaseAPIRequest):
    game_id: int
    version_id: int


class MimoTaskRequest(MimoRequest):
    task_id: int


class MimoShopRequest(MimoRequest):
    item_id: int


class RedeemCodeRequest(BaseAPIRequest):
    code: str


class AppLoginRequest(BaseModel):
    email: str
    password: str
    mmt_result: typing.Optional[str] = None
    ticket: typing.Optional[str] = None
