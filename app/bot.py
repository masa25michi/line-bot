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
    word_id = event.postback.data
    word_model = Word.get_word_by_id(word_id)
    # params = {'keyword': word}
    # r = requests.get(
    #     'https://jisho.org/api/v1/search/words',
    #     params=params)
    # response = r.json()

    # pp = pprint.PrettyPrinter(indent=4)

    # pp.pprint(response)

    # examples = [
    # {
    #     "type": "text",
    #     "text": word,
    #     "weight": "bold",
    #     "size": "xl"
    # },
    # {
    #     "type": "separator"
    # }
    # ]
    # count = 1
    # for data in response['data']:
    # example = data['japanese'][0]

    # text = '・ '

    # if 'word' in example:
    #     text = example['word'] + \
    #         ' (' + example['reading'] + ') \n'
    # else:
    #     text = example['reading'] + ' \n'

    # examples.append({
    #     "type": "text",
    #     "size": "xs",
    #     "wrap": True,
    #     "text": text
    # })

    # count += 1

    # examples.append({
    #     "type": "text",
    #     "size": "xs",
    #     "wrap": True,
    #     "text": text
    # })

    messages = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#800000",
            "align": "center",
            "size": "lg",
            "contents": [
                {
                    "type": "text",
                    "color": "#FFFFFF",
                    "text": word_model.name
                },
            ],
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "size": "md",
                    "wrap": True,
                    "text": 'いみ:  ' + word_model.meaning
                },
                {
                    "type": "text",
                    "size": "md",
                    "wrap": True,
                    "text": 'よみ:  ' + word_model.spell
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "Favorite",
                        "data": word_model.id,
                        "displayText": word_model.name
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "Dictionary",
                        "uri": "https://jisho.org/search/" + word_model.name + "%20%23words"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "Kanji",
                        "uri": "https://jisho.org/search/" + word_model.name + "%20%23kanji"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "Sentences",
                        "uri": "https://jisho.org/search/" + word_model.name + "%20%23sentences"
                    }
                }
            ],
            "flex": 0
        }
    }
    return FlexSendMessage(alt_text=word_model.name + 'ってどういう意味？', contents=messages)
