# 문장 부호_한글
front_punctuation_list = {"⠸⠌": "/", "⠦": "\"", "⠠⠦": "'",
                          "⠦⠄": "(", "⠦⠂": "{", "⠦⠆": "[", "⠐⠦": "〈", "⠔⠔": "*", "⠰⠆": "〃", "⠈⠺": "₩", "⠈⠙": "$", "⠠⠄": " "}
# 22 Jan 2022: "⠠⠄": "" 점역자 주

middle_punctuation_list = {"⠐⠆": "·", "⠐⠂": ":", "⠦⠄": "(", "⠠⠴": ")", "⠦⠂": "{", "⠐⠴": "}", "⠦⠆": "[", "⠰⠴": "]", "⠐⠦": "〈", "⠴⠂": "〉",
                           "⠤": "-", "⠤⠤": "~", "⠸⠌": "/", "⠠⠦": "'", "⠴⠄": "'", "⠠⠠⠠": "...", "⠔⠔": "*", "⠰⠆": "〃", "⠈⠺": "₩", "⠈⠙": "$"}  # "⠲": "." 은 말줄임표 위해서
# 11 Dec 2021: "⠲": ".", middle에서 뺐음. 읊다 -> 을.다 현상 때문에
# 13 Dec 2021: "⠦": "\"", "⠴": "\"" middle에서 뺐음. 많지 -> 만"지 현상 때문에

end_punctuation_list = {"⠲": ".", "⠦": "?", "⠖": "!", "⠐": ",", "⠐⠂": ":", "⠴": "\"", "⠠⠴": ")", "⠐⠴": "}",
                        "⠰⠴": "]", "⠤⠤": "~", "⠠⠠⠠": "...", "⠸⠌": "/", "⠔⠔": "*", "⠰⠆": "〃", "⠈⠺": "₩", "⠈⠙": "$", "⠠⠄": " "}
# 22 Jan 2022: "⠠⠄": 점역자 주


def translatePunc(words):
    stringWithTranslatedPunc = words

    for (index, word) in enumerate(words):
        word_arr = word
        word_arr = translateMiddlePunc(
            translateLastPunc(translateFirstPunc(word_arr)))

        stringWithTranslatedPunc[index] = word_arr

    return stringWithTranslatedPunc


def translateFirstPunc(word: str):
    resultWord = word
    resultWord = list(resultWord)

    firstWord = ""
    if len(word) == 0:
        firstWord = ""
    else:
        firstWord = word[0]

    secondWord = " "

    if len(word) > 1:
        secondWord = word[1]

    if (firstWord + secondWord) in front_punctuation_list.keys():
        punctuation = front_punctuation_list[firstWord + secondWord]
        resultWord = resultWord[1:]  # 하나를 지우고

        if front_punctuation_list[firstWord + secondWord] == " ":  # 점역자 주
            resultWord = resultWord[1:]
            resultWord = translateFirstPunc(resultWord)
        else:
            resultWord[0] = punctuation  # 하나는 변경해주고
            # resultWord = punctuation + resultWord[1:]

    elif firstWord in front_punctuation_list.keys():
        punctuation = front_punctuation_list[firstWord]
        resultWord[0] = punctuation

    return "".join(resultWord)


def translateMiddlePunc(word):
    resultWord = word
    resultWord = list(resultWord)

    for index in range(len(resultWord)):
        word_count = len(resultWord)
        if index >= word_count:
            break

        oneWord = resultWord[index]

        back_index_word = " "
        back_back_index_word = " "

        if index < word_count - 2:
            back_index_word = resultWord[index + 1]
        if index < word_count - 3:
            back_back_index_word = resultWord[index + 2]

        if (oneWord + back_index_word + back_back_index_word) in middle_punctuation_list.keys():
            resultWord[index] = "."
            resultWord[index+1] = "."
            resultWord[index+2] = "."
        elif (oneWord + back_index_word) in middle_punctuation_list.keys():
            punctuation = middle_punctuation_list[oneWord + back_index_word]
            # resultWord = resultWord[index:]  # 하나를 지우고
            resultWord[index] = punctuation
        elif oneWord in middle_punctuation_list.keys():
            punctuation = middle_punctuation_list[oneWord]
            resultWord[index] = punctuation

    return "".join(resultWord)


def translateLastPunc(word):
    resultWord = word
    resultWord = list(resultWord)
    word_count = len(word)

    if word_count == 0:
        return resultWord

    lastWord = word[word_count-1]
    front_word = " "
    front_front_word = " "

    if word_count > 1:
        front_word = word[word_count - 2]
    if word_count > 2:
        front_front_word = word[word_count - 3]

    if (front_front_word + front_word + word) in end_punctuation_list.keys():
        resultWord[word_count-1] = "."
        resultWord[word_count-2] = "."
        resultWord[word_count-3] = "."

    elif lastWord in end_punctuation_list.keys() and (end_punctuation_list[lastWord] == "\"" or end_punctuation_list[lastWord] == "'"):
        if front_word in end_punctuation_list.keys() and (end_punctuation_list[front_word] == "." or end_punctuation_list[front_word] == ","):
            punctuation_front = end_punctuation_list[front_word]
            punctuation_back = end_punctuation_list[lastWord]
            resultWord[len(resultWord)-2] = punctuation_front
            resultWord[len(resultWord)-1] = punctuation_back

    elif (front_word + lastWord) in end_punctuation_list.keys():
        punctuation = end_punctuation_list[front_word + lastWord]
        resultWord = resultWord[word_count-1:]

        if end_punctuation_list[front_word + lastWord] == " ":  # 점역자 주
            resultWord = resultWord[word_count-2:]
            resultWord = translateLastPunc(resultWord)
        else:
            resultWord[len(resultWord)-1] = punctuation
    elif lastWord in end_punctuation_list.keys():
        punctuation = end_punctuation_list[lastWord]
        # resultWord[word_count-1] = punctuation
        try:
            resultWord = resultWord[:word_count-1] + \
                list(punctuation) + resultWord[word_count]
        except:
            resultWord = resultWord[:word_count-1] + list(punctuation)

    return "".join(resultWord)
