from . import views
from aiohttp import web
from .settings import BOT_TOKEN


def setup_routes(app: web.Application):
    app.router.add_route("GET", "/", views.index)
    app.router.add_route("POST", "/webhook" + BOT_TOKEN, views.webhook)
    app.router.add_route("GET", "/save_image", views.save_image)

