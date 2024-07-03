from flask import Flask, request
from asyncio import run_coroutine_threadsafe, get_event_loop

from utils import format_request_to_message


app = Flask(__name__)


def run_flask_app(_bot):
    global bot
    bot = _bot
    app.run(host="0.0.0.0", debug=True)
