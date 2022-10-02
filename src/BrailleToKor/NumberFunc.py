number_braille = "⠼"

number_braille_dict = {"⠚": "0", "⠁": "1", "⠃": "2", "⠉": "3", "⠙": "4", "⠑": "5", "⠋": "6", "⠛": "7", "⠓": "8", "⠊": "9"}

number_punctuation_invalid = ["~", " ", "⠀"] # 수표 효력 무효
number_punctuation_valid = [":", "-", ".", "·", "⠲", "⠐","⠤"] # 수표 효력 유효

def changeToNumber(c):

    return number_braille_dict[c]

def translateNumber(text: str):
    result = ""
    isdigit = False
    for i in range(len(text)):
        if text[i] == number_braille: # 수표 만나면
            isdigit = True
            continue
        elif text[i] in number_punctuation_valid and isdigit: # 수표 O & 효력 유
            if text[i] == "⠲":
                result += "."
            elif text[i] == "⠐":
                result +=  ","
            else:
                result += text[i]
            isdigit = True
            continue
        elif text[i] in number_punctuation_invalid: # 수표 O & 효력 무효 만남
            result += text[i]
            isdigit = False
            continue
        elif text[i] in number_braille_dict.keys() and isdigit: # 수표 O && 숫자
            result += changeToNumber(text[i])
            isdigit = True
            continue
        else: # 기타 점자
            isdigit = False
            result += text[i]
            continue
            
    return result

