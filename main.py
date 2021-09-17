import os
import asyncio
import argparse

import aioreloader
from aiohttp import web
from mainapp import create_app
from mainapp import bot

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Library uvloop is not available.")

parser = argparse.ArgumentParser(description="Aiohttp project")
parser.add_argument("--host", help="YOUR HOST", default="localhost")
parser.add_argument("--port", help="YOUR PORT", default=5000)
parser.add_argument("--reload", action="store_true",
                    help="Автоперезагразка сервера при изменении в коде")

args = parser.parse_args()

app = create_app()
if args.reload:
    print("Start with code reload")
    aioreloader.start()

if __name__ == "__main__":
    print("Запуск сервера !")
    if args:
        web.run_app(app, host=args.host, port=args.port)
    else:
        web.run_app(app, port=int(os.environ["PORT"]))
    bot.start_bot()
