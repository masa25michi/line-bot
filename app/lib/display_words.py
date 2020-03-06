def get_words_for_display_old(words):
    word_counts = 0
    total_word_counts = len(words)
    words_for_display = ''
    for word in words:
        word_counts += 1
        words_for_display += '[' + str(word_counts) + '] '

        if word.name == word.spell:
            words_for_display += word.name + ': ' + word.meaning
        else:
            words_for_display += word.name + \
                ' ( ' + word.spell + ' ): ' + word.meaning

        if word_counts != total_word_counts:
            words_for_display += '\n\n'

    return words_for_display


def get_words_for_display(words, chapter):
    word_contents = {}
    title = 'N2 '

    word_counts = 0
    sub_chapter_count = 1
    for word in words:
        words_for_display = '[' + str(word_counts + 1) + ']   '

        if word.name == word.spell:
            words_for_display += word.name + ':  ' + word.meaning
        else:
            words_for_display += word.name + \
                ' ( ' + word.spell + ' ):  ' + word.meaning

        if str(sub_chapter_count) not in word_contents:
            word_contents[str(sub_chapter_count)] = []

        word_contents[str(sub_chapter_count)].append(
            {
                "type": "text",
                "text": words_for_display,
                "size": "sm",
                "margin": "lg",
                "wrap": True,
                "action": {
                    "type": "uri",
                    "label": "action",
                    "uri": "http://linecorp.com/"
                }
            }
        )

        word_counts += 1
        if word_counts % 5 == 0:
            sub_chapter_count += 1

    carousels = []

    for sub_chapter, contents in word_contents.items():
        carousels.append(
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#800000",
                    "contents": [
                        {
                            "type": "text",
                            "color": "#FFFFFF",
                            "text": title + '  Chapter ' + str(chapter) + ' - ' + str(sub_chapter)
                        },
                    ],
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents
                }
            }
        )

    return {
        "type": "carousel",
        "contents": carousels
    }
