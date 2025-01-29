from fastapi.responses import JSONResponse
import genshin
import asyncio

__all__ = ("claim_reward",)


async def claim_reward(
    client: genshin.Client, game: genshin.Game, *, retry: int = 0
) -> JSONResponse:
    try:
        reward = await client.claim_daily_reward(game=game)
    except ConnectionResetError:
        if retry < 3:
            await asyncio.sleep(1 << retry)
            return await claim_reward(client, game, retry=retry + 1)
        else:
            return JSONResponse(
                {"message": "Connection reset error", "game": game, "retcode": -1},
                status_code=500,
            )
    except genshin.DailyGeetestTriggered as e:
        return JSONResponse(
            {
                "message": e.msg,
                "game": game,
                "retcode": -9999,
                "data": {"gt": e.gt, "challenge": e.challenge},
            },
            status_code=400,
        )
    except genshin.GenshinException as e:
        return JSONResponse(
            {"message": e.msg, "game": game, "retcode": e.retcode}, status_code=400
        )
    except Exception as e:
        return JSONResponse(
            {"message": str(e), "game": game, "retcode": -1}, status_code=500
        )
    else:
        return JSONResponse(
            {
                "message": "OK",
                "game": game,
                "retcode": 0,
                "data": {
                    "name": reward.name,
                    "amount": reward.amount,
                    "icon": reward.icon,
                },
            }
        )
