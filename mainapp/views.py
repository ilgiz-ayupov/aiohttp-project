import gzip
import json

from aiohttp import web
from aiohttp_jinja2 import template
from aiogram import types

from . import bot
from .database import db


@template("index.html")
async def index(request: web.Request):
    return {"username": "Ильгиз"}


async def webhook(request: web.Request):
    data = await request.json()
    update = types.Update().to_object(data=data)
    await bot.dp.process_update(update)
    return web.Response(
        headers={
            "Content-Encoding": "gzip"
        },
        status=201
    )


async def save_image(request: web.Request):
    data = await request.json()
    print(data)


async def get_image(request: web.Request):
    return {
        "ID": 1,
        "question_pk": 1,
        "image_path": "media/python.png"
    }
