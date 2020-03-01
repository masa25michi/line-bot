from models import *
from app.lib.display_words import get_words_for_display
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


def notify_morning_vocabs(app, line_bot_api):
    with app.app_context():
        users = User.get_all_users()

        if users == None:
            print('not found users. job finished')
            return 0

        for user in users:
            user_id = user.line_id
            words = Word.get_words(user_id)
            response = get_words_for_display(words)

            # update for next notification
            # User.update_chapter(user_id)

            # send line
            messages = TextSendMessage(text=response)
            line_bot_api.push_message(user_id, messages=messages)
