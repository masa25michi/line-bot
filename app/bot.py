import requests
import json
import pprint
from models import *
from app.lib.display_words import get_words_for_display
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage, FlexSendMessage
)


def analyze_user_message(user_message):
    # 0: tell user's current level, 1: return today's chapter
    return 1


def reply_message(event):
    response = ''
    user_line_id = event.source.sender_id
    user = User.get_user(user_line_id)

    if (user == None):
        User.create_user(user_line_id)

        response = 'Hi~'
    else:
        user_message = event.message.text
        print('received: ' + user_message)
        user_message_type = analyze_user_message(user_message)

        if user_message_type == 0:
            textbook = Textbook.get_textbook(user.textbook_id)
            response = 'You are learning ' + textbook.name
        elif user_message_type == 1:
            words = Word.get_words(user_line_id)
            chapter = Chapter.get_chapter_by_id(words[0].chapter_id).number

            response = get_words_for_display(words, chapter)

    return response


def reply_postback(event):
    word = event.postback.data
    params = {'keyword': word}
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
                        "label": "Favorite",
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
                        "uri": "https://jisho.org/word/" + word
                    }
                }
            ],
            "flex": 0
        }
    }
    return FlexSendMessage(alt_text=word + 'ってどういう意味？', contents=messages)
