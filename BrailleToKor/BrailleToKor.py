from KorData import CHO, JUNG, JONG

class BrailleToKor:
    # 전체 문장 번역
    def translation(input: str):
        return ""


    # 점자인지 확인하는 함수
    def isBraille(input: str):
        return False

    # 끊은 '단어' 점자를 한글로 바꾸는 역할
    def brailleTosyllable(word: str):
        return ""


    # 초성 + 중성 (+ 종성)을 합쳐 하나의 음절을 반환
    def JamoCombination(c1, c2, c3):
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

print(BrailleToKor.JamoCombination('ㅇ', 'ㅏ', 'ㄴ'))

    