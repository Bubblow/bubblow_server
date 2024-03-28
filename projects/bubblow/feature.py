from bs4 import BeautifulSoup
import requests
import re

def Feature(news_link):

    response = requests.get(news_link)
    html_content = response.text

    #뉴스 크롤러 실행
    soup = BeautifulSoup(html_content,"html.parser")
    news_titles = []
    news_contents =[]

    # 뉴스 제목 가져오기
    title_element = soup.select_one('h2.media_end_head_headline')
    if title_element:
        title = title_element.get_text(strip=True)
    else:
        title_element = soup.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        title = title_element.get_text(strip=True) if title_element else None


    #이미지 URL 가져오기
    image_container = soup.select_one("span.end_photo_org")
    if image_container:
        image_element = image_container.find('img', class_='_LAZY_LOADING')
        if image_element and 'data-src' in image_element.attrs:
            image_url = image_element['data-src']
        else:
            image_url = None  # 이미지가 없거나 data-src 속성이 없는 경우

    # 뉴스 본문 가져오기
    content = soup.select("article#dic_area")
    if content == []:
        content = soup.select("#articeBody")

    # 기사 텍스트만 가져오기
    # list합치기
    content = ''.join(str(content))

    # html태그제거 및 텍스트 다듬기
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1, repl='', string=str(title))
    content = re.sub(pattern=pattern1, repl='', string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2, '')

    news_titles.append(title)
    news_contents.append(content)

    # 날짜
    published_at = soup.find('div', {'class': 'media_end_head_info_datestamp'}).find('span', {'class': 'media_end_head_info_datestamp_time'}).text.strip()

    # 기자 이름
    byline = soup.find('span', {'class': 'byline_s'}).text.strip()
    
    # 카테고리
    category=soup.find('em', {'class': 'media_end_categorize_item'}).text.strip()

    # 언론사
    provider = soup.find('p', {'class': 'c_text'})
    if provider:
      full_text = provider.get_text()

      # 'ⓒ'와 '.' 사이의 텍스트 추출
      match = re.search(r'ⓒ(.*?)\.', full_text)
      if match:
          copyright_text = match.group(1).strip()
      else:
          print("언론사를 찾을 수 없습니다.")


    # JSON 데이터로 변환
    news_data = {
        "title": news_titles[0] if news_titles else "",
        "image_url": image_url if 'image_url' in locals() else "",
        "content": news_contents[0].strip("[]")+ f"{byline}",
        "published_at": published_at,
        "provider": copyright_text if 'copyright_text' in locals() else "",
        "byline": byline if 'byline' in locals() else "",
        "fix_category": category if 'category' in locals() else ""
    }

    return [news_data]