from fastapi.responses import JSONResponse
import json
import genshin

from ..models import AppLoginRequest

__all__ = ("app_login",)


async def app_login(data: AppLoginRequest) -> JSONResponse:
    client = genshin.Client()
    try:
        if data.mmt_result is not None:
            result = await client._app_login(
                data.email,
                data.password,
                mmt_result=genshin.models.SessionMMTResult(
                    **json.loads(data.mmt_result)
                ),
                encrypted=True,
            )
        elif data.ticket is not None:
            result = await client._app_login(
                data.email,
                data.password,
                ticket=genshin.models.ActionTicket(**json.loads(data.ticket)),
                encrypted=True,
            )
        else:
            result = await client._app_login(data.email, data.password, encrypted=True)
    except genshin.GenshinException as e:
        return JSONResponse({"message": str(e), "retcode": e.retcode}, status_code=400)
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)

    if isinstance(result, genshin.models.AppLoginResult):
        return JSONResponse(
            {
                "message": "OK",
                "retcode": 0,
                "data": result.model_dump_json(by_alias=True),
            }
        )
    if isinstance(result, genshin.models.SessionMMT):
        return JSONResponse(
            {
                "message": "OK",
                "retcode": -9999,
                "data": result.model_dump_json(by_alias=True),
            }
        )

    return JSONResponse(
        {
            "message": "OK",
            "retcode": -9998,
            "data": result.model_dump_json(by_alias=True),
        }
    )
