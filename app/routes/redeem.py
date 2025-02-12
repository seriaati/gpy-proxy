from fastapi.responses import JSONResponse
import genshin
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

__all__ = ("redeem_code",)


load_dotenv()


def encrypt_string(string: str) -> str:
    key = Fernet(os.environ["FERNET_KEY"])
    return key.encrypt(string.encode()).decode()


async def redeem_code(client: genshin.Client, code: str, cookies: str) -> JSONResponse:
    try:
        await client.redeem_code(code)
    except genshin.InvalidCookies:
        if "stoken" in cookies and "ltmid" in cookies:
            try:
                parsed_cookies = genshin.parse_cookie(cookies)
                new_cookies = await genshin.fetch_cookie_with_stoken_v2(
                    parsed_cookies, token_types=[2, 4]
                )
                parsed_cookies.update(new_cookies)
                client.set_cookies(parsed_cookies)
                new_cookies = "; ".join(f"{k}={v}" for k, v in parsed_cookies.items())
            except Exception as e:
                return JSONResponse(
                    {"message": str(e), "retcode": 1000}, status_code=400
                )
            else:
                return await redeem_code(client, code, new_cookies)
        else:
            return JSONResponse({"retcode": 999}, status_code=400)
    except genshin.GenshinException as e:
        return JSONResponse(
            {
                "message": e.msg,
                "retcode": e.retcode,
                "cookies": encrypt_string(cookies),
            },
            status_code=400,
        )
    except Exception as e:
        return JSONResponse({"message": str(e), "retcode": -1}, status_code=500)
    else:
        return JSONResponse(
            {
                "message": "OK",
                "retcode": 0,
                "cookies": encrypt_string(cookies),
            },
        )
