def do():

    import requests
    from bs4 import BeautifulSoup
    import bs4.element
    import datetime
    import json

    # BeautifulSoup 객체 생성, url을 요청해서 beautifulsoup객체를 생성하는 함수, url을 input으로 받고 beautifulsoup객체를 output으로 전달, 
    def get_soup_obj(url):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'}
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text,'lxml')

        return soup


    # # 뉴스의 기본 정보 가져오기, for문의 내용을 함수화, input=section id & section -> url을 구성하고 상위 3개 뉴스에 대한 메타 정보를 만든 후에 output으로 전달, 3개 뉴스에 대한 메타 정보를 모두 보내줘야하므로 리스트 형식으로 함, 
    def get_top3_news_info(sec, sid):
        # 임시 이미지, 이미지가 없는 뉴스도 있기 때문에 설정
        default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"

        # 해당 분야 상위 뉴스 목록 주소
        sec_url = "https://news.naver.com/main/list.nhn?mode=LSD&mid=sec" \
                + "&sid1=" \
                + sid
        print("section url : ", sec_url)

        # 해당 분야 상위 뉴스 HTML 가져오기
        soup = get_soup_obj(sec_url)

        # 해당 분야 상위 뉴스 3개 가져오기
        global news_list3
        news_list3 = []
        lis3 = soup.find('ul', class_='type06_headline').find_all("li", limit=3)
        for li in lis3:
            # title : 뉴스 제목, news_url : 뉴스 URL, image_url : 이미지 URL
            news_info = {
                "title" : li.img.attrs.get('alt') if li.img else li.a.text.replace("\n", "").replace("\t","").replace("\r","") ,
                "date" : li.find(class_="date").text,
                "news_url" : li.a.attrs.get('href'),
                "image_url" : li.img.attrs.get('src') if li.img else default_img
            }
            news_list3.append(news_info)

        return news_list3

    # 뉴스 본문 가져오기, input으로는 뉴스 본문이 있는 url을 전달받아, html구조에 맞춰 뉴스 본문을 output으로 전달,
    def get_news_contents(url):
        soup = get_soup_obj(url)
        body = soup.find('div', class_="_article_body_contents")

        news_contents = ''
        for content in body:
            if type(content) is bs4.element.NavigableString and len(content) > 50:
                # content.strip() : whitepace 제거 (참고 : https://www.tutorialspoint.com/python3/string_strip.htm)
                # 뉴스 요약을 위하여 '.' 마침표 뒤에 한칸을 띄워 문장을 구분하도록 함
                news_contents += content.strip() + ' '

        return news_contents


    # '정치', '경제', '사회' 분야의 상위 3개 뉴스 크롤링, input은 없고 output은 3개의 섹션별 3개의 뉴스 정보 및 뉴스 본문을 news_dic을 output으로 전달, sod에 사용될 정보를 담고 67라인에서 반복하여 요청
    def get_naver_news_top3():
        # 뉴스 결과를 담아낼 dictionary
        news_dic = dict()

        # sections : '정치', '경제', '사회'
        sections = ["pol", "eco","soc"]
        # section_ids : URL에 사용될 뉴스 각 부문 ID
        section_ids = ["100", "101","102"]

        for sec, sid in zip(sections, section_ids):
            # 뉴스의 기본 정보 가져오기
            news_info = get_top3_news_info(sec, sid)
            # 3개의 분야의 뉴스 정보(title, news_url, date, image_url) 가 나옴
            #print(news_info)
            for news in news_info:
                # 뉴스 본문 가져오기
                news_url = news['news_url']
                news_contents = get_news_contents(news_url)

                # 뉴스 정보를 저장하는 dictionary를 구성
                news['news_contents'] = news_contents

            news_dic[sec] = news_info

        return news_dic

    # 함수 호출 - '정치', '경제', '사회' 분야의 상위 3개 뉴스 크롤링
    news_dic = get_naver_news_top3()
    # 경제의 첫번째 결과 확인하기
    news_dic


    def load_tokens(filename):
        with open(filename) as fp:
            tokens = json.load(fp)

        return tokens
        
    KAKAO_TOKEN_FILENAME = "res/kakao_message/kakao_token.json"
    ## 저장된 토큰 정보를 읽어 옴
    tokens = load_tokens(KAKAO_TOKEN_FILENAME)


    ## 텍스트 메시지 url
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization" : "Bearer " + tokens['access_token']
    }
                #token이 저장된 파일
                #KAKAO_TOKEN_FILENAME = "res/kakao_message/kakao_token.json"
                #KAKAO_APP_KEY = "<REST_API 앱키를 입력하세요>"
                #kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

    ########################
    ##리스트 템플릿으로 뉴스 목록 전송하기
    # 사용자가 선택한 카테고리를 제목에 넣기 위한 dictionary
    sections_ko = {'pol': '정치', 'eco' : '경제', 'soc' : '사회'}

    # 네이버 뉴스 URL
    navernews_url = "https://news.naver.com/main/home.nhn"

    # 추후 각 리스트에 들어갈 내용(content) 만들기
    contents = []

    # 리스트 템플릿 형식 만들기
    template = {
        "object_type" : "list",
        "header_title" : "상위 뉴스 빅3",
        "header_link" : {
            "web_url": navernews_url,
            "mobile_web_url" : navernews_url
        },
        "contents" : contents,
        "button_title" : "네이버 뉴스 바로가기"
    }
    ## 내용 만들기
    # 각 리스트에 들어갈 내용(content) 만들기
    for news_info in news_list3:
        content = {
            "title" : news_info.get('title'),
            "description" : "작성일 : " + news_info.get('date'),
            "image_url" : news_info.get('image_url'),
            "image_width" : 50, "image_height" : 50,
            "link": {
                "web_url": news_info.get('news_url'),
                "mobile_web_url": news_info.get('news_url')
            }
        }

        contents.append(content)

    data = {
        'template_object':json.dumps(template)
    }
    # 카카오톡 메시지 전송
    res = requests.post(url,data=data, headers=headers)
    if res.json().get('result_code') == 0:
        print('뉴스를 성공적으로 보냈습니다.')
    else:
        print('뉴스를 성공적으로 보내지 못했습니다. 오류메시지 : ', res.json())
