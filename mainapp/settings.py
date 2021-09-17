import os

BOT_TOKEN = "2025046509:AAFb52T3xQNd1fv3Md2oZUD1BiMme2JtQLI"

# webhook settings
WEBHOOK_HOST = "https://heroku-webhook-bot.herokuapp.com"
# WEBHOOK_HOST = "http://0.0.0.0:5000"
WEBHOOK_PATH = f"/webhook{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ["PORT"])

