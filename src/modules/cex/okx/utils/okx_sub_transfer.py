from typing import Callable
from datetime import datetime
from asyncio import sleep

import base64
import hmac

from loguru import logger

from config import OKXSettings


def signature(timestamp: str, method: str, url: str, body: str | None):
    try:
        if not body:
            body = ""
        message = timestamp + method.upper() + url + body
        mac = hmac.new(
            bytes(OKXSettings.API_SECRET, encoding="utf-8"),
            bytes(message, encoding="utf-8"),
            digestmod="sha256",
        )
        d = mac.digest()
        return base64.b64encode(d).decode("utf-8")
    except Exception as ex:
        logger.error(ex)
        return signature(timestamp, method, url, body)


def generate_request_headers(url: str, method: str, body=''):
    dt_now = datetime.utcnow()
    ms = str(dt_now.microsecond).zfill(6)[:3]
    timestamp = f"{dt_now:%Y-%m-%dT%H:%M:%S}.{ms}Z"
    headers = {
        "Content-Type": "application/json",
        "OK-ACCESS-KEY": OKXSettings.API_KEY,
        "OK-ACCESS-SIGN": signature(timestamp, method, url, body),
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": OKXSettings.API_PASSWORD,
        'x-simulated-trading': '0'
    }
    return headers


async def send_request(
        url: str, headers: dict, method: str, data='', *, make_request: Callable
):
    try:
        response_json = await make_request(
            method=method,
            url=url,
            headers=headers,
            data=data,
        )

        if response_json:
            await sleep(2)
            return response_json
        logger.error(f"Couldn't send request {url}")
        return False
    except Exception as ex:
        logger.error(ex)
        return False


async def transfer_from_subaccs_to_main(token: str, make_request: Callable) -> None:
    try:
        headers = generate_request_headers(url='/api/v5/users/subaccount/list',
                                           method='GET')
        list_sub = await send_request(
            url=f"https://www.okx.com/api/v5/users/subaccount/list",
            headers=headers,
            method='GET',
            make_request=make_request
        )
        if not list_sub:
            logger.info(f"You don't have Sub Accounts!")
            return
        for sub_data in list_sub['data']:
            name = sub_data['subAcct']

            headers = generate_request_headers(
                url=f"/api/v5/asset/subaccount/balances?subAcct={name}&ccy={token}",
                method='GET')
            sub_balance = await send_request(
                url=f"https://www.okx.com/api/v5/asset/subaccount/balances?subAcct={name}&ccy={token}",
                headers=headers,
                method='GET',
                make_request=make_request
            )
            if not sub_balance:
                await sleep(10)
                continue
            sub_balance = float(sub_balance['data'][0]['bal'])
            if sub_balance == 0:
                logger.info(f'Sub Account: {name} | Balance: 0')
                await sleep(10)
                continue

            body = {
                "ccy": f"{token}",
                "amt": str(sub_balance),
                "from": 6,
                "to": 6,
                "type": "2",
                "subAcct": name
            }

            headers = generate_request_headers(
                url=f"/api/v5/asset/transfer", body=str(body), method='POST'
            )
            res = await send_request(
                url="https://www.okx.com/api/v5/asset/transfer",
                headers=headers,
                method='POST',
                data=str(body),
                make_request=make_request
            )
            if len(res['data']) != 0:
                logger.success(f'Successfully transferred from {name} => MAIN: {sub_balance} {token}')
                await sleep(30)
            else:
                if 'Insufficient balance' in str(res):
                    await sleep(2)
                    continue
                logger.warning(f'Error - {res}')
            await sleep(1)

    except Exception as ex:
        logger.error(ex)
        await sleep(2)
        return