from hanspell import spell_checker
 
sent = "한글 맞춤법검사기 재대로작동돼는지테스트"
spelled_sent = spell_checker.check(sent)
checked_sent = spelled_sent.checked
 
print(checked_sent)

