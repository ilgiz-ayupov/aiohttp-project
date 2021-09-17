from aiohttp import web
from aiohttp_jinja2 import template
from aiogram import types

from . import bot


@template("index.html")
async def index(request: web.Request):
    print(request)
    return {"username": "Ильгиз"}


async def webhook(request: web.Request):
    json_string = request.json()
    print(json_string)
    update = types.Update().as_json()
    print(update)
    bot.dp.process_update(update)
    return "!", 200
