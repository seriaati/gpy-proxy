import typing

from fastapi.responses import JSONResponse
import genshin
from fastapi import FastAPI, HTTPException, Request, Response, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

from app.routes import (
    app_login,
    buy_mimo_shop_item,
    claim_mimo_task_reward,
    claim_reward,
    finish_mimo_task,
    get_mimo_shop_items,
    get_mimo_tasks,
    get_notes,
    redeem_code,
)
from app.models import (
    AppLoginRequest,
    MimoRequest,
    MimoShopRequest,
    MimoTaskRequest,
    RedeemCodeRequest,
    BaseAPIRequest,
)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI(docs_url=None, redoc_url=None)
security = HTTPBearer(auto_error=True)


async def validate_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    """Validate bearer token"""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    return credentials.credentials


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"message": str(exc)}, status_code=500)


@app.get("/")
async def root() -> typing.Dict[str, str]:
    return {"message": "genshin.py proxy API v1.0.1"}


@app.post("/redeem/", dependencies=[Security(validate_token)])
async def redeem_code_endpoint(data: RedeemCodeRequest) -> Response:
    return await redeem_code(data.get_client(), data.code, data.cookies)


@app.post("/checkin/", dependencies=[Security(validate_token)])
async def daily_checkin(data: BaseAPIRequest) -> Response:
    return await claim_reward(data.get_client(), genshin.Game(data.game))


@app.post("/login/", dependencies=[Security(validate_token)])
async def login_endpoint(data: AppLoginRequest) -> Response:
    return await app_login(data)


@app.post("/notes/", dependencies=[Security(validate_token)])
async def get_notes_endpoint(data: BaseAPIRequest) -> Response:
    return await get_notes(data.get_client(), data.uid, genshin.Game(data.game))


@app.post("/mimo/finish_task/", dependencies=[Security(validate_token)])
async def finish_mimo_task_endpoint(data: MimoTaskRequest) -> Response:
    return await finish_mimo_task(data)


@app.post("/mimo/claim_reward/", dependencies=[Security(validate_token)])
async def claim_mimo_task_reward_endpoint(data: MimoTaskRequest) -> Response:
    return await claim_mimo_task_reward(data)


@app.post("/mimo/buy_item/", dependencies=[Security(validate_token)])
async def buy_mimo_shop_item_endpoint(data: MimoShopRequest) -> Response:
    return await buy_mimo_shop_item(data)


@app.post("/mimo/tasks/", dependencies=[Security(validate_token)])
async def get_mimo_tasks_endpoint(data: MimoRequest) -> Response:
    return await get_mimo_tasks(data)


@app.post("/mimo/shop/", dependencies=[Security(validate_token)])
async def get_mimo_shop_items_endpoint(data: MimoRequest) -> Response:
    return await get_mimo_shop_items(data)
