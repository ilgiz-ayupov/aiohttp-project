import os

BOT_TOKEN = "1969091536:AAFHAq4kVmAx39t3dCsDvJveWZi9mqsMeqo"

# webhook settings
WEBHOOK_HOST = "https://heroku-webhook-bot.herokuapp.com"
# WEBHOOK_HOST = "http://0.0.0.0:5000"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
# WEBAPP_HOST = "0.0.0.0"
# WEBAPP_PORT = int(os.environ["PORT"])

