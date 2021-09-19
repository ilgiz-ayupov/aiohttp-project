import os
import argparse

import aioreloader
from aiohttp import web
from mainapp import create_app, database
from mainapp import bot

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
    bot.start_webhook()
    database.create_tables()
    web.run_app(app, port=int(os.environ["PORT"]))
