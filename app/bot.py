from models import *
from app.lib.display_words import get_words_for_display


def analyze_user_message(user_message):
    # 0: tell user's current level, 1: return today's chapter
    return 1


def reply_message(event):
    print(event)
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
