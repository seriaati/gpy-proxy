from fastapi.responses import JSONResponse
import genshin

from ..models import MimoRequest, MimoShopRequest, MimoTaskRequest

__all__ = (
    "finish_mimo_task",
    "claim_mimo_task_reward",
    "buy_mimo_shop_item",
    "get_mimo_tasks",
    "get_mimo_shop_items",
)


async def finish_mimo_task(data: MimoTaskRequest) -> JSONResponse:
    try:
        client = data.get_client()
        await client.finish_mimo_task(
            data.task_id, game_id=data.game_id, version_id=data.version_id
        )
    except genshin.GenshinException as e:
        return JSONResponse({"message": e.msg, "retcode": e.retcode}, status_code=400)
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)
    else:
        return JSONResponse({"message": "OK", "retcode": 0})


async def claim_mimo_task_reward(data: MimoTaskRequest) -> JSONResponse:
    try:
        client = data.get_client()
        await client.claim_mimo_task_reward(
            data.task_id, game_id=data.game_id, version_id=data.version_id
        )
    except genshin.GenshinException as e:
        return JSONResponse({"message": e.msg, "retcode": e.retcode}, status_code=400)
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)
    else:
        return JSONResponse({"message": "OK", "retcode": 0})


async def buy_mimo_shop_item(data: MimoShopRequest) -> JSONResponse:
    try:
        client = data.get_client()
        code = await client.buy_mimo_shop_item(
            data.item_id, game_id=data.game_id, version_id=data.version_id
        )
    except genshin.GenshinException as e:
        return JSONResponse({"message": e.msg, "retcode": e.retcode}, status_code=400)
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)
    else:
        return JSONResponse({"message": "OK", "retcode": 0, "code": code})


async def get_mimo_tasks(data: MimoRequest) -> JSONResponse:
    try:
        client = data.get_client()
        tasks = await client.get_mimo_tasks(
            game_id=data.game_id, version_id=data.version_id
        )
    except genshin.GenshinException as e:
        return JSONResponse({"message": e.msg, "retcode": e.retcode}, status_code=400)
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)
    else:
        return JSONResponse(
            {
                "message": "OK",
                "retcode": 0,
                "tasks": [task.model_dump_json(by_alias=True) for task in tasks],
            }
        )


async def get_mimo_shop_items(data: MimoRequest) -> JSONResponse:
    try:
        client = data.get_client()
        items = await client.get_mimo_shop_items(
            game_id=data.game_id, version_id=data.version_id
        )
    except genshin.GenshinException as e:
        return JSONResponse({"message": e.msg, "retcode": e.retcode}, status_code=400)
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)
    else:
        return JSONResponse(
            {
                "message": "OK",
                "retcode": 0,
                "items": [item.model_dump_json(by_alias=True) for item in items],
            }
        )
