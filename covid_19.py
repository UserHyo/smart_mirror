#def do():

import requests
import xmltodict
import json
import datetime

service_KEY = "DEaTeAeMY+/ZCys9LTGzBk/MnsJg8VJSGr7h5yrG94i8/FSzVyxUgMsVAM1E3B4XEmYhiTRt5a/fxW+ODvMJ6w=="

service_url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson"

Now_str = datetime.date.today().strftime('%Y%m%d')
Now = int(Now_str)
Now_2=(Now-2)
Now_2_str=str(Now_2)

    #Now_7 = int(Now_7_str)

    #print(type(Now))


    #print(resp.content)

params = {
    "ServiceKey":service_KEY,
    "pageNo":"1",
    "numOfRows":"2",
    "startCreateDt":Now_2_str,
    "endCreateDt":Now_str
}

resp = requests.get(service_url, params=params)

parsed_content = xmltodict.parse(resp.content)
json_string=json.loads(json.dumps(parsed_content))
    #daily_cnt: 일별 확진자수, stateDt: 기준일, decideCnt: 누적 확진자수
daily_cnt = []
stateDt = []
decideCnt = []
    #response 안에 body 안에 items 안에 item
items = json_string['response']['body']['items']['item']
    #items을 추출
for i in items:
    stateDt.append(int(i['stateDt'][4:])) #연도는 제외하고 월,일 만 가져옴
    decideCnt.append(int(i['decideCnt']))
    #일일 확진자 수 구하기 -> 첫날 이전의 확진자 수를 알 수 없어서 1일 빼서 첫날을 제외시키는 거임
for i in range(len(stateDt)-1):
    daily_cnt.append(decideCnt[i]-decideCnt[i+1])

    #데이터 일치 및 순서 변경, openapi에서는 최신날짜가 먼저 나오므로 최신 날짜가 뒤에 나오도록 하기
stateDt.pop()
decideCnt.pop()
#    stateDt.reverse()
#    decideCnt.reverse()
#    daily_cnt.reverse()
 
print(type(daily_cnt[0]))
print(daily_cnt)
print(type(decideCnt[0]))
print(decideCnt[0])
print ("오늘 확진자 수는 %d명 이고 누적 확진자 수는 %d명입니다." %daily_cnt[0],decideCnt[0])
    #print ("누적 확진자 수는 %d명 입니다." %decideCnt[5])
    

