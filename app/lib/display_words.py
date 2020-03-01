def get_words_for_display(words):
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
