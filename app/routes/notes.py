from fastapi.responses import JSONResponse
import genshin

__all__ = ("get_notes",)


async def get_notes(
    client: genshin.Client, uid: int, game: genshin.Game
) -> JSONResponse:
    try:
        if game is genshin.Game.GENSHIN:
            notes = await client.get_genshin_notes(uid, return_raw_data=True)
        elif game is genshin.Game.HONKAI:
            notes = await client.get_honkai_notes(uid, return_raw_data=True)
        elif game is genshin.Game.STARRAIL:
            notes = await client.get_starrail_notes(uid, return_raw_data=True)
        elif game is genshin.Game.ZZZ:
            notes = await client.get_zzz_notes(uid, return_raw_data=True)
        else:
            return JSONResponse(
                {"message": "Invalid game", "game": game, "retcode": 1000},
                status_code=500,
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
                "data": notes,
            }
        )
