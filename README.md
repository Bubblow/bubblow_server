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
cd bubblow_server/
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
    payload = { 'passportKey': '0103527cc78df4354dae796239716c5bd2417cd6'
    , '_callback': 'jQuery112406967053878796103_1710292798358'
    , 'q': text, 'color_blindness': '0' }
```
#### 6.1.2 py-hanspell 설치
```bash
pip install setuptools
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
cd projects/bubblow
pip install -r requirements.txt
```

#### 9. DB migration 하기

```bash
alembic init migrations
(... 생략 ...)
```

projects > bubblow > alembic.ini 파일 안에서 > sqlalchemy.url  = 노션 보고 변경
</br>
migrations > env.py 아래와 같이 수정 및 추가

```bash
import models
target_metadata = models.Base.metadata
(... 생략 ...)
```
터미널에 마저 실행
```bash
alembic revision --autogenerate
alembic upgrade head
(... 생략 ...)
```

#### 10. .env 파일 생성하기
projects랑 동일한 위치에 .env파일 만들기
자세한 코드는 노션 참고

#### 11. 로컬 위치 수정
projects > bubblow > domain > question > question_crud.py에서 아래 코드를 로컬에 맞춰서 수정한다
```bash
sys.path.append('/Users/hansol/desktop (2)/Bubblow/nt-worker')
# '/Users/hansol/desktop (2)/Bubblow/nt-worker'은 내 로컬에서 nt-worker가 현재 위치한 path이다
```

#### 12. fastapi 실행
```bash
uvicorn main:app --reload
# http://127.0.0.1:8000/docs에 접속하면 api 테스트 가능
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

