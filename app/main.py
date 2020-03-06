import os
import atexit
import app.bot as bot
import requests
import json
import pprint
# import app.scheduler as line_scheduler
from database.sqlalchemy import init_db
# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage, FlexSendMessage
)


app = Flask(__name__)

# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(e.message)
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = bot.reply_message(event)

    flex_message = FlexSendMessage(
        alt_text='Today \'s Words Here',
        contents=reply_message)

    line_bot_api.reply_message(event.reply_token, flex_message)


@handler.add(PostbackEvent)
def on_postback(event):
    word = event.postback.data
    params = {
        'keyword': word,
    }
    r = requests.get(
        'https://jisho.org/api/v1/search/words',
        params=params)
    response = r.json()

    examples = [
        {
            "type": "text",
            "text": word,
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "separator"
        }
    ]
    count = 1
    for data in response['data']:
        example = data['japanese'][0]

        if 'word' in example:
            text = ' [' + str(count) + ']  ' + example['word'] + \
                ' (' + example['reading'] + ') \n'
        else:
            text = ' [' + str(count) + ']  ' + example['reading'] + ' \n'

        examples.append({
            "type": "text",
            "wrap": True,
            "text": text})

        count += 1

    messages = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": examples
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "'❤️ Favorite",
                        "data": word,
                        "displayText": word
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "More Detail",
                        "uri": "https://linecorp.com"
                    }
                }
            ],
            "flex": 0
        }
    }

    flex_message = FlexSendMessage(
        alt_text='Example Here',
        contents=messages)

    line_bot_api.reply_message(event.reply_token, flex_message)


app.config.from_object('database.config.Config')
init_db(app)
