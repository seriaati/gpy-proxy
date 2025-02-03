import genshin
from pydantic import BaseModel
import typing

MAX_RETRIES = 3
BACKOFF_FACTOR = 2
MAX_BACKOFF = 32


class BaseAPIRequest(BaseModel):
    cookies: str
    lang: str
    region: str
    game: str
    uid: int

    def get_client(self) -> genshin.Client:
        return genshin.Client(
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
