import speech_recognition as sr
import requests
import json
import keyword
import news_kakao
import covid_19

def get_speech():
    #마이크에서 음성을 추출하는 객체
    recognizer = sr.Recognizer()
        #마이크 설정
    microphone = sr.Microphone(sample_rate=16000)
        
        #마이크 소음 수치 반영 _ 보류
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    #    print("소음 수치를 반영하여 음성을 청취합니다.{}".format(recognizer.energy_threshold)) - 빼도 되는듯
        #음성수집
    with microphone as source:
        print("say something!")
        audio_data = recognizer.listen(source)
    audio = audio_data.get_raw_data()

#audio = get_speech()
#text = kakao_stt(KAKAO_APP_KEY, "stream", audio)
#print("음성 인식 결과 : " + text)

    kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    headers = {
        "Content-Type": "application/octet-stream",
        "X-DSS-Service": "DICTATION",
        "Authorization": "KakaoAK " + "793b6c9257acd09a4d5c279601b21f40",}

    res = requests.post(kakao_speech_url, headers=headers, data=audio)
    #print(res.text) -> 없어도 된다
    result = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    global text 
    text = json.loads(result).get('value')
    print(text)

get_speech()

#추가 프로젝트 -> 날씨?
KEYWORD_NEWS = "뉴스"
KEYWord_COVID= "코로나"


if text:
    print("무엇을 도와드릴까요?")
    get_speech()
    if KEYWORD_NEWS in text:
        print("뉴스 프로젝트 실행")
        news_kakao.do()
    if KEYWord_COVID in text:
        print("코로나 프로젝트 실행")
        covid_19.do()
        
else:
    print("다시한번 말해주세요")
    get_speech()

#KEYWORD_SEARCH = "찾아줘"
#if KEYWORD_SEARCH in text:
#    print("검색 프로젝트 실행")

