#haspell test code
from hanspell import spell_checker
text = "아버지가방에들어가신다나는오늘코딩을했다"

hanspell_sent = spell_checker.check(text)
print(hanspell_sent.checked)

#Mecab test code
# from konlpy.tag import Mecab
# mecab = Mecab()
# text = u"""잘 설치 되었는지 테스트"""
# nouns = mecab.nouns(text)
# print(nouns)