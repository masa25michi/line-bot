from models import *


def analyze_user_message(user_message):
    # 0: tell user's current level, 1: return today's chapter
    return 1


def reply_message(event):
    response = ''
    user_line_id = event.source.sender_id
    user = User.get_user(user_line_id)

    if (user == None):
        User.create_user(user_line_id)

        response = 'Hi! Please let me know your current level!'
    else:
        user_message = event.message.text
        user_message_type = analyze_user_message(user_message)

        if user_message_type == 0:
            textbook = Textbook.get_textbook(user.textbook_id)
            response = 'You are learning ' + textbook.name
        elif user_message_type == 1:
            words = Word.get_words(user_line_id)
            response = get_words_for_display(words)

    return response


def get_words_for_display(words):
    word_counts = 0
    total_word_counts = len(words)
    words_for_display = ''
    for word in words:
        word_counts += 1
        words_for_display += word.name + ': ' + word.meaning

        if word_counts != total_word_counts:
            words_for_display += '\n'

    return words_for_display
