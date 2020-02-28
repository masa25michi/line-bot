import src.chapter


def analyze_user_message(user_message):
    return 'Analyzed'


def reply_message(event):
    return analyze_user_message(event.message.text)
