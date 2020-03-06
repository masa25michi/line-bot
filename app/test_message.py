import os
import urllib.parse
from models import *
from database.sqlalchemy import init_db
from flask import Flask, request, abort
from app.lib.display_words import get_words_for_display
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, StickerSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction, URIAction
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


def send_message():
    with app.app_context():
        user_id = 'Ud6dc3bd52b1dac33a94a0023ee442854'

        # https://developers.line.biz/media/messaging-api/sticker_list.pdf
        messages = TextSendMessage('hi')
        sticker_message = StickerSendMessage(
            package_id='11538',
            sticker_id='51626503'
        )
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='Japanese Level N2',
                        text='Chapter 1-1',
                        actions=[
                            MessageAction(
                                label='aaaaa',
                                text='Word'
                            ),
                            URIAction(
                                label='uri1',
                                uri='http://example.com/1'
                            ),
                        ]
                    ),
                ]
            )
        )
        test = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "N2 Chapter"
                            }
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "N2 Chapter"
                            }
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                            {
                                "type": "text",
                                "text": "あああああ",
                                "wrap": True,
                                "size": "sm",
                                "margin": "lg",
                                "action": {
                                    "type": "uri",
                                    "label": "action",
                                    "uri": "http://linecorp.com/"
                                }
                            },
                        ]
                    }
                }
            ]
        }
        flex_message = FlexSendMessage(
            alt_text='Today \'s Words Here',
            contents=test)

        line_bot_api.push_message(
            user_id, messages=[flex_message])
