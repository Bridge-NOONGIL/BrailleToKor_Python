from ast import And
from KorData import CHO, JUNG, JONG
from BrailleData import abb_word_dict, abb_cho_jung_jong_dict

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
        last = brailleWord.count - 1

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
                    last = brailleWord.count - 1 # 갱신

        for i in range(brailleWord.count):
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
                continue #205
        

        return ""


    # 전체 문장 번역
    def translation(self, input):

        result = ""

        # 숫자 번역
        # 문장부호 번역

        for word in input:
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


            result += BrailleToKor.brailleTosyllable(replacedWord)
            result += ""

        return result



if __name__ == "__main__":
    b = BrailleToKor()
