import os
import urllib.parse
from models import *
from database.sqlalchemy import init_db
from flask import Flask, request, abort
from app.lib.display_words import get_words_for_display
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)
app.config.from_object('database.config.Config')
init_db(app)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def notify_morning_vocabs():
    with app.app_context():
        users = User.get_all_users()

        if users == None:
            print('not found users. job finished')
            return 0

        for user in users:
            user_id = user.line_id
            words = Word.get_words(user_id)
            response = get_words_for_display(words)

            # # update for next notification
            User.update_chapter(user_id)

            messages = TextSendMessage(response)
            line_bot_api.push_message(user_id, messages=messages)
