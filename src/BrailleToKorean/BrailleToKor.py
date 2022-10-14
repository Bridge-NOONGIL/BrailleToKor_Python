# -*- coding: utf-8 -*-
from . import PunctuationFunc
from . import NumberFunc
from .KorData import CHO, JUNG, JONG
from .BrailleData import abb_word_dict, abb_cho_jung_jong_dict, JUNG_braille, double_JUNG_braille, JONG_braille, abb_jung_jong_dict, double_JONG_braille, double_CHO_braille, abb_CHO_braille, abb_cho_dict, CHO_braille


brailles = ['⠀','⠮','⠐','⠼','⠫','⠩','⠯','⠄','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌','⠴','⠂','⠆','⠒','⠲','⠢',
        '⠖','⠶','⠦','⠔','⠱','⠰','⠣','⠿','⠜','⠹','⠈','⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚','⠅',
        '⠇','⠍','⠝','⠕','⠏','⠟','⠗','⠎','⠞','⠥','⠧','⠺','⠭','⠽','⠵','⠪','⠳','⠻','⠘','⠸']

class BrailleToKor:
    def __init__(self) -> None:
        pass

    # 점자인지 확인하는 함수
    def isBraille(self, input):
        for i in input:
            if i in brailles:
                return True
            else:
                return False
        return False



    # 초성 + 중성 (+ 종성)을 합쳐 하나의 음절을 반환
    def JamoCombination(self, c1, c2, c3):
        cho_i = 0
        jung_i = 0
        jong_i = 0

        for i in range(len(CHO)):
            if CHO[i] == c1:
                cho_i = i

        choValue = cho_i * 21 * 28

        for i in range(len(JUNG)):
            if JUNG[i] == c2:
                jung_i = i
        
        jungValue = jung_i * 28

        for i in range(len(JONG)):
            if JONG[i] == c3:
                jong_i = i

        jongValue = 0 

        if jong_i == 0:
            jongValue = 0
        else:
            jongValue += jong_i

        uniValue = choValue + jungValue + jongValue + 0xAC00

        uni = chr(uniValue)

        return uni

    # 끊은 '단어' 점자를 한글로 바꾸는 역할
    def brailleTosyllable(self, word: str):
        
        brailleWord = word # brailleWord로 번역을 함

        abb_braille = "" # 약어 점자
        abb_kor = "" # 약어

        wordResult = "" # 번역 결과

        cho = "" # 초성
        jung = "" # 중성
        jong = "" # 종성

        # 초성/중성/종성 정해졌다는 flag
        selectedCho = False
        selectedJung = False
        selectedJong = False

        # ㅖ + 받침 있을 때 flag (continue 두 번 하기 위해서)
        ye_jong = False

        # 껏의 된소리표 flag
        flag_14 = False 

        # 마지막 음절의 인덱스
        last = len(brailleWord) - 1

        # 단어 자체가 약어라면 바로 점자로 번역해서 리턴
        if word in abb_word_dict.keys():
            wordResult += abb_word_dict[word]
            return wordResult
        else: # 단어에 약어가 포함
            for (key, value) in abb_word_dict:
                if key in word:
                    abb_braille = key
                    abb_kor = value

            if abb_braille != "": # 위 Step에 의해 약어가 포함되어있는 것을 확인했다면
                # [다만] 위에 제시된 말들의 앞에 다른 음절이 붙어 쓰일 때에는 약어를 사용하여 적지 않는다.
                if word[0] != abb_braille[0]: # 종성이 가장 먼저 오는 경우 X
                    pass
                else:
                    wordResult += abb_kor
                    brailleWord = brailleWord.replace(abb_braille, "")
                    last = len(brailleWord) - 1 # 갱신

        for i in range(len(brailleWord)):
            letter_front = ""
            letter = brailleWord[i]
            letter_back = ""
            letter_back_back  = ""

            letter_isBraille = self.isBraille(letter)
            letter_back_isBraille = False
            letter_back_back_isBraille = False


            if letter_isBraille == False:
                wordResult += letter
                continue
                
            if i > 0:
                letter_front = brailleWord[i-1]

            if i < last:
                letter_back = brailleWord[i+1]
                letter_back_isBraille = self.isBraille(letter_back)

            if i < last - 1:
                letter_back_back = brailleWord[i+2]
                letter_back_back_isBraille = self.isBraille(letter_back_back)

            if letter == "⠤": # 붙임표면 pass
                cho = ""
                jung = ""
                jong = ""
                selectedCho = False
                selectedJung = False
                selectedJong = False

                continue

            if flag_14: # 껏 flag
                flag_14 = False
                continue

            # 것, 껏 처리
            if (letter == "⠠") and ((letter_back + letter_back_back) in abb_cho_jung_jong_dict.keys()): # 껏
                cho = "ㄲ"
                jung = "ㅓ"
                jong = "ㅅ"

                selectedCho = True
                selectedJung = True
                selectedJong = True

                flag_14 = True # 된소리표 Pass
                continue
            elif (selectedCho == False) and ((letter + letter_back) in abb_cho_jung_jong_dict.keys()): # 것
                cho = "ㄱ"
                jung = "ㅓ"
                jong = "ㅅ"
                selectedCho = True
                selectedJung = True
                selectedJong = True
                continue

            if ye_jong == True:
                ye_jong = False
                continue


            #초성 처리
            if selectedCho == False:
                # 초성 없이 중성이 먼저 나오는 경우
                if letter in JUNG_braille.keys(): # 초성 'ㅇ'
                    cho = "ㅇ"
                    selectedCho = True
                    selectedJung = True

                    if (letter+letter_back) in double_JUNG_braille.keys():
                        jung = double_JUNG_braille[letter+letter_back]
                        if letter_back_back not in JONG_braille.keys(): # 이중 종성 + 종성이 없는 경우
                            jong = " "
                            selectedJong = True
                        continue
                    else: # 기본 중성일 때
                        jung = JUNG_braille[letter]

                    if letter_back not in JONG_braille.keys(): # letter_back이 종성이 아닐 때
                        jong = " " # 종성이 없음
                        selectedJong = True
                    else:
                        continue

                elif letter in abb_jung_jong_dict.keys(): # 초성이 ㅇ이고 letter가 중+종 약자일 때
                    cho = "ㅇ"
                    selectedCho = True

                    jung = abb_jung_jong_dict[letter][0]
                    jong = abb_jung_jong_dict[letter][1]

                    selectedJung = True
                    selectedJong = True

                    if letter_back in JONG_braille.keys(): # letter_back이 종성일 때 => 겹받침
                        try:
                            jong = double_JONG_braille[jong + letter_back]
                        except:
                            jong = " "
                        continue
                
                # 'ㅏ' 약자일 때 - 초성 리스트에 존재하고(이 때 'ㄱ','ㄹ','ㅅ' 제외, letter_back이 초성이거나 종성일 때)
                elif (letter in abb_CHO_braille.keys()) and ((letter_back in CHO_braille.keys() or letter_back in JONG_braille.keys() or i == last or letter_back == "⠫" or letter_back == "⠇" or letter_back == "⠤") or letter_back_isBraille == False) :
                    cho = CHO_braille[letter]
                    jung = "ㅏ"
                    selectedCho = True
                    selectedJung = True

                    if letter_back == "⠌":
                        if letter_back_back in JONG_braille.keys(): # ex. 톈 case 해결 위해
                            jung = "ㅖ"
                            ye_jong = True
                            continue

                        if cho == "ㅎ":
                            jung = "ㅖ"
                            jong = " "
                        else:
                            jung = "ㅏ"
                            jong = "ㅆ"

                        selectedJong = True
                        continue
                    
                    elif letter_back == "⠤": # 초성처리에서 letter_back이 붙임표일 때 음절 완성
                        jong = " "
                        selectedJong = True

                    elif letter_back not in JONG_braille.keys():
                        jong = " "
                        selectedJong = True
                
                elif letter in abb_cho_dict.keys(): # '가', '사'
                    cho = abb_cho_dict[letter][0]
                    jung = "ㅏ"
                    selectedCho = True
                    selectedJung = True

                    if letter_back == "⠌": # 뒤에 3, 4점
                        jung = "ㅏ"
                        jong = "ㅆ"

                        selectedJong = True
                        continue

                    elif letter_back not in JONG_braille.keys(): # 뒤에 종성이 없음
                        jong = " "
                        selectedJong = True

                elif letter == "⠠": # 6점 (된소리)
                    # 'ㅏ' 약자(까, 싸 제외)
                    if letter_back in abb_CHO_braille.keys() and ((letter_back_back in CHO_braille.keys() or letter_back_back in JONG_braille.keys() or i+1 == last or letter_back_back == "⠫" or letter_back_back == "⠇") or letter_back_back_isBraille == False):
                        try:
                            cho = CHO_braille[letter + letter_back]
                        except:
                            cho = " "
                        
                        jung = "ㅏ"
                        selectedCho = True
                        selectedJung = True

                        if letter_back_back == "⠌": # 땄 같은 경우
                            jong = "ㅆ"
                            continue
                    
                        elif letter_back_back not in JONG_braille.keys(): # 종성이 없을 때. 따.
                            jong = " "
                            selectedJong = True

                        
                    elif letter_back in abb_cho_dict.keys(): # 까, 싸 - letter_back이 가, 사 일 때
                        try:
                            cho = abb_cho_dict[letter + letter_back][0]
                        except:
                            cho = " "
                        try:
                            jung = abb_cho_dict[letter + letter_back][1]
                        except:
                            jung = " " 

                        selectedCho = True
                        selectedJung = True

                        if letter_back_back == "⠌":
                            jong = "ㅆ"
                        
                        if letter_back_back not in JONG_braille.keys():
                            jong = " "
                            selectedJong = True

                    elif letter_back not in CHO_braille.keys(): # 된소리가 아니라 'ㅅ'일 때
                        try:
                            cho = CHO_braille[letter]
                        except:
                            cho = " "
                        selectedCho = True 

                    elif letter_back in CHO_braille: # 된소리 + 초성
                        try: 
                            cho = double_CHO_braille[letter + letter_back]
                        except:
                            cho = " "
                        selectedCho = True

                    continue
                
                elif letter in CHO_braille.keys():
                    cho = CHO_braille[letter]
                    selectedCho = True
                else:
                    continue
            
            # 중성 처리
            if selectedCho == True and selectedJung == False:
                
                if letter in abb_jung_jong_dict.keys(): # 중성 + 종성 약자
                    jung = abb_jung_jong_dict[letter][0]
                    jong = abb_jung_jong_dict[letter][1]

                    selectedJung = True
                    selectedJong = True

                    if (jong + letter_back) in double_JONG_braille.keys(): # 이중 종성(겹받침)
                        jong = double_JONG_braille[jong + letter_back]
                        continue
                
                elif letter in JUNG_braille.keys(): # 중성일 때
                    jung = JUNG_braille[letter]
                    selectedJung = True

                    if (letter+letter_back) in double_JUNG_braille.keys(): # 이중 중성
                        jung = double_JUNG_braille[letter+letter_back]

                        if letter_back_back not in JONG_braille.keys():
                            jong = " "
                            selectedJong = True

                        continue
                    elif letter_back not in JONG_braille.keys(): # 중성 + 종성이 없는 경우
                        jong = " "
                        selectedJong = True

                    elif letter_back in JONG_braille.keys(): # 종성이 있으면 continue
                        continue

            # 종성 처리
            if selectedCho == True and selectedJung == True and selectedJong == False:
                if letter in JONG_braille.keys():
                    jong = JONG_braille[letter]
                    selectedJong = True

                    if (jong+letter_back) in double_JONG_braille.keys(): # 이중 종성
                        jong = double_JONG_braille[jong + letter_back]
                        continue
            
            # 음절 완성
            if selectedCho == True and selectedJung == True and selectedJong == True:
                # 제 16항: '성, 썽, 정, 쩡, 청'은 'ㅅ,  ㅆ,  ㅈ,  ㅉ,  ㅊ’  다음에  'ㅕㅇ'의 약자를 적어 나타낸다.
                if (cho == "ㅅ" or cho == "ㅆ" or cho == "ㅈ" or cho == "ㅉ" or cho == "ㅊ") and jung == "ㅕ" and jong == "ㅇ":
                    jung = "ㅓ"
                
                wordResult += self.JamoCombination(cho, jung, jong)

                selectedCho = False
                selectedJung = False
                selectedJong = False

                cho = ""
                jung = ""
                jong = ""

        return wordResult


    # 전체 문장 번역
    def translation(self, input):

        result = ""

        # 숫자 번역
        input = NumberFunc.translateNumber(input)
        
        # 문장부호 번역
        
        punctuationTranslatedWords = PunctuationFunc.translatePunc((input.replace('⠀', ' ')).split())
        
        for word in punctuationTranslatedWords:
            replacedWord = word
            replace123456Flag = False # 옹옹 처리
            replace1245Flag = False # 운운 처리

            if "⠛⠛" in word:
                replacedWord = word.replace("⠛⠛", "")
                replace1245Flag = True
            if replace1245Flag:
                replacedWord = replacedWord.replace("⠛", "")
                replace1245Flag = False

            if "⠿⠿" in word:
                replacedWord = word.replace("⠿⠿", "")
                replace123456Flag = True
            if replace123456Flag:
                replacedWord = replacedWord.replace("⠿", "")
                replace123456Flag = False


            result += self.brailleTosyllable(replacedWord)
            result += " "

        return result



# if __name__ == "__main__":
#     b = BrailleToKor()
#     print(b.translation("⠒⠒⠒⠒⠒⠒⠒⠒⠲⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠼⠓⠓ ⠼⠙⠲ ⠟⠑⠯⠺ ⠑⠣⠪⠢⠮ ⠨⠕⠢⠨⠁⠚⠗⠬ ⠦⠄⠑⠣⠪⠢ ⠉⠉⠍⠈⠕⠠⠴  ⠶ ⠈⠮⠮ ⠕⠂⠁⠈⠥ ⠟⠑⠯⠺ ⠑⠣⠪⠢⠮ ⠨⠕⠢⠨⠁⠚⠗ ⠨⠠⠟⠺ ⠠⠗⠶⠫⠁⠮ ⠠⠠⠎ ⠘⠥⠃⠠⠕⠊⠲ ⠤⠒⠒⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠒⠒⠒⠤⠤⠤⠼⠓⠊ ⠠⠄⠈⠪⠐⠕⠢ ⠠⠞⠑⠻⠐⠂ ⠋⠎⠊⠐⠣⠒ ⠈⠪⠐⠕⠢⠰⠗⠁⠝ ⠊⠍ ⠱⠨⠣⠣⠕⠫ ⠟⠇⠚⠉⠵ ⠈⠪⠐⠕⠢⠕ ⠕⠌⠠⠪⠃⠉⠕⠊⠲ ⠿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠿ ⠱⠨⠣⠣⠕ ⠼⠁⠐⠂ ⠉⠎⠊⠥ ⠼⠃⠘⠒⠕⠉⠕⠦ ⠱⠨⠣⠣⠕ ⠼⠃⠐⠂ ⠉⠊⠥ ⠼⠃⠘⠒⠕⠜⠖ ⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐ ⠊⠒⠠⠨⠁ ⠨⠕⠵⠕⠧ ⠼⠃ ⠚⠁⠉⠡ ⠠⠊⠗⠊⠥ ⠫⠦⠵ ⠘⠒⠕ ⠊⠽⠎⠌⠎⠲ ⠦⠉⠎⠊⠥ ⠼⠃⠘⠒⠕⠉⠕⠦⠶ ⠤ ⠿⠶⠶⠶⠶⠶⠶⠻⠛⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠿ ⠱⠨⠣⠣⠕⠐⠂ ⠠⠗ ⠚⠁⠉⠡⠕ ⠊⠧⠗⠠⠎ ⠊⠍ ⠰⠟⠈⠍⠫ ⠫⠦⠵ ⠘⠒⠕ ⠊⠧⠗⠌⠉ ⠘⠧⠲ ⠉⠢⠨⠣⠣⠕⠐⠂ ⠉⠊⠥ ⠰⠟⠚⠒ ⠰⠟⠈⠍⠧ ⠫⠦⠕ ⠘⠒⠕ ⠊⠽⠒ ⠨⠹⠕ ⠕⠌⠎⠲⠠⠄ ⠔⠔ ⠈⠪⠐⠕⠢⠰⠗⠁ ⠠⠭ ⠊⠍ ⠣⠕⠉⠵ ⠎⠠⠊⠾ ⠑⠣⠪⠢⠕⠂⠠⠫⠬⠦  ⠑ ⠼⠓⠓      ⠼⠙⠲ ⠟⠑⠯⠺ ⠑⠣⠪⠢       ⠼⠁ "))
    