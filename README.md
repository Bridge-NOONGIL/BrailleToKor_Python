# BrailleToKor_Python

점자 문자열을 한국어로 번역할 수 있는 BrailleToKor 파이썬 패키지입니다.

BrailleToKor Python package that translates braille string to Korean.

## Quick Start

```shell
$ pip install BrailleToKorean
```

## Usage Example
```python
from BrailleToKorean.BrailleToKor import BrailleToKor

b = BrailleToKor()
print(b.translation("⠣⠒⠉⠻⠚⠠⠝⠬⠲⠀⠨⠎⠢⠨⠀⠘⠾⠱⠁⠀⠙⠗⠋⠕⠨⠕⠕⠃⠉⠕⠊⠲"))
```
### print 결과
```python
안녕하세요. 점자 번역 패키지입니다.
```
