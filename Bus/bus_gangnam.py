import requests, lxml, time
from bs4 import BeautifulSoup
from datetime import datetime

# routeId
No_3100 = '216000026'
No_3101 = '216000043'
No_3102 = '216000061'

# stnId
guesthouse_forseoul = '216000379'
guesthouse_foransan = '216000378'
maingate_forseoul = '216000719'
maingate_foransan = '216000048'
gangnam = '121000974'

plateNo_3100 = ''
plateNo_3101 = ''
plateNo_3102 = ''
plateNo_3102_seoul = ''
plateNo_3102_ansan = ''
def main():
    global plateNo_3100, plateNo_3101, plateNo_3102, plateNo_3102_seoul, plateNo_3102_ansan
    while True:
        # 현재시간 확인
        now = datetime.now()
        print(now.hour, "시", now.minute, "분", now.second, "초")
        # 3102 게스트하우스 > 서울
        link = make_link(guesthouse_forseoul, No_3102)
        response = requests.get(link)
        soup = BeautifulSoup(response.content,'lxml-xml')
        arrival_result = soup.find('busArrivalItem')
        try:
            plateno = arrival_result.find('plateNo1').string
            minute = arrival_result.find('predictTime1').string
            print("안산 출발:", plateno, "차량", minute, "분 후 도착")
        except:
            plateno = ''
            print("도착 예정 X")
        if arrival_result:
            if plateNo_3102 == '' or plateNo_3102 != plateno:
                if plateNo_3102 != '':
                    pass
                plateNo_3102 = plateno
            else:
                pass
        else:
            pass
        # 3102 강남 > 안산
        link = make_link(gangnam, No_3102)
        response = requests.get(link)
        soup = BeautifulSoup(response.content,'lxml-xml')
        arrival_result = soup.find('busArrivalItem')
        try:
            plateno = arrival_result.find('plateNo1').string
            minute = arrival_result.find('predictTime1').string
            print("강남 도착:", plateno, "차량", minute, "분 후 도착")
        except:
            plateno = ''
            print("도착 예정 X")
        if arrival_result:
            if plateNo_3102_seoul == '' or plateNo_3102_seoul != plateno:
                pass
        else:
            pass
        # 3102 안산 도착
        link = make_link(guesthouse_foransan, No_3102)
        response = requests.get(link)
        soup = BeautifulSoup(response.content,'lxml-xml')
        arrival_result = soup.find('busArrivalItem')
        try:
            plateno = arrival_result.find('plateNo1').string
            minute = arrival_result.find('predictTime1').string
            print("안산 도착:", plateno, "차량", minute, "분 후 도착")
        except:
            plateno = ''
            print("도착 예정 X")
        if arrival_result:
            if plateNo_3102_ansan == '' or plateNo_3102_ansan != plateno:
                if plateNo_3102_ansan != '':
                    pass
                plateNo_3102_ansan = plateno
            else:
                pass
        else:
            pass
        time.sleep(30)


def make_link(stn, route):
    link = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey=1234567890&routeId=' + route + '&stationId=' + stn
    return link




main()
