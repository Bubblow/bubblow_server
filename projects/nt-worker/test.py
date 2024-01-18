import json
from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisTitle import AnalysisTitle
from Analysis.AnalysisScore import AnalysisScore
from feature import Feature


news_link = "https://n.news.naver.com/mnews/article/016/0002248617?sid=101"

news_data = Feature(news_link)

# 결과 출력
print(json.dumps(news_data, ensure_ascii=False, indent=4))
print(news_data[0]['title'])

newsBuffer = Feature(news_link)
# for targetIndex in range(len(newsBuffer)):

at = AnalysisTitle(newsBuffer[0]['title'])
at.PrintMyValue()
ac = AnalysisContent(newsBuffer[0]['content'], newsBuffer[0]['provider'], newsBuffer[0]['fix_category'])
ac.PrintMyValue()
myAs = AnalysisScore(at, ac)
myAs.PrintMyValue()