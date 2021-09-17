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
    update = types.Update().as_json()
    print("UPDATE", update)
    bot.dp.process_update(data)
    return "!", 200
