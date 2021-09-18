import gzip
import json

from aiohttp import web
from aiohttp_jinja2 import template
from aiogram import types

from . import bot


@template("index.html")
async def index(request: web.Request):
    print(request)
    return {"username": "Ильгиз"}


async def webhook(request: web.Request):
    data = await request.json()
    print("DATA", data)
    update = types.Update().to_object(data=data)
    print("UPDATE", update)
    await bot.dp.process_update(update)

    data_as_bytes = bytes(json.dumps(data), encoding="UTF-8")
    out_data = gzip.compress(data_as_bytes, compresslevel=5)
    return web.Response(
        body=out_data,
        headers={
            "Content-Encoding": "gzip"
        }
    )
