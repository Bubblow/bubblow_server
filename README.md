# 🚀 버블로우 서버 초기 세팅

파이썬 프레임워크 **FastAPI**를 사용, 각 실행 환경에 맞는 가상환경(`venv`)을 사용

#### 1. 바탕 화면에 '버블로우 서버' 폴더 만들기

#### 2. git clone 하기
```bash
git clone https://github.com/Bubblow/bubblow_server.git
```

#### 3. Python 설치 확인
```bash
python3 -V
```

#### 4. 가상환경 생성
Bash에서 다음 명령어 실행:
```bash
python -m venv venv
```

#### 5. 가상환경 활성화
- 맥:
```bash
source venv/bin/activate
```
- 윈도우:
```bash
source venv/Scripts/activate
```

#### 6. 신뢰도 알고리즘에 필요한 라이브러리 설치
#### 6.1 py-hanspell (파이썬 맞춤법 검사 라이브러리)
```bash
git clone https://github.com/ssut/py-hanspell.git
cd py-hanspell
```

#### 6.1.1 `py-hanspell` 폴더 안에 > `hanspell` 폴더 안에 > `spell_checker.py` 파일 수정
아래 코드로 def check 함수 수정
```python
# -*- coding: utf-8 -*-
"""
Python용 한글 맞춤법 검사 모듈
"""
def check(text):
    """
    매개변수로 입력받은 한글 문장의 맞춤법을 체크합니다.
    """
    if isinstance(text, list):
        result = []
        for item in text:
            checked = check(item)
            result.append(checked)
        return result

    # 최대 500자까지 가능.
    if len(text) > 500:
        return Checked(result=False)

    payload = { 'passportKey': 'f727f097f7d41da7ac664ae6041bb00afd3d5af5'
    , '_callback': 'jQuery1124010479246828164901_1709258162093'
    , 'q': text, 'color_blindness': '0' }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer': 'https://search.naver.com/',
    }

    start_time = time.time()
    r = _agent.get(base_url, params=payload, headers=headers)
    passed_time = time.time() - start_time

    json_data = re.search(r'\((.*)\)', r.text).group(1)
    data = json.loads(json_data)
    html = data['message']['result']['html']
    result = {
        'result': True,
        'original': text,
        'checked': _remove_tags(html),
        'errors': data['message']['result']['errata_count'],
        'time': passed_time,
        'words': OrderedDict(),
    }
    # 코드의 나머지 부분...
```
#### 6.1.2 py-hanspell 설치
```bash
python setup.py install
```

#### 6.2 형태소 분석기 Mecab 설치
```bash
cd .. 
git clone https://github.com/SOMJANG/Mecab-ko-for-Google-Colab.git
cd Mecab-ko-for-Google-Colab
bash install_mecab-ko_on_colab_light_220429.sh
```

#### 7. 그 외에 필요한 패키지 설치
```bash
cd ..
pip install -r requirements.txt
```


#### 8. fastapi 실행
```bash
cd projects/bubblow
uvicorn main:app --reload
```

끝‼️

(참고) 라이브러리 테스트 코드
```python
#haspell test code
from hanspell import spell_checker
text = "아버지가방에들어가신다나는오늘코딩을했다"

hanspell_sent = spell_checker.check(text)
print(hanspell_sent.checked)

#Mecab test code
from konlpy.tag import Mecab
mecab = Mecab()
text = u"""잘 설치 되었는지 테스트"""
nouns = mecab.nouns(text)
print(nouns)
```

