import os
import urllib.parse
from models import *
from database.sqlalchemy import init_db
from flask import Flask, request, abort
from app.lib.display_words import get_words_for_display
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, FlexSendMessage
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
            # user_id = 'Ud6dc3bd52b1dac33a94a0023ee442854'
            words = Word.get_words(user_id)
            chapter = Chapter.get_chapter_by_id(words[0].chapter_id).number

            notification_message = get_words_for_display(words, chapter)

            messages = TextSendMessage('おはよう〜　今日も一日がんばろう〜')

            flex_message = FlexSendMessage(
                alt_text='Today \'s Words Here',
                contents=notification_message)

            # sticker_message = StickerSendMessage(
            #     package_id='11538',
            #     sticker_id='51626503'
            # )

            line_bot_api.push_message(
                user_id, messages=[messages, flex_message])

            break
