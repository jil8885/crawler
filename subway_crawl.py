import lxml, requests
from bs4 import BeautifulSoup


def main():
    stn_name = input()
    search(stn_name)


def search(name):
    link = 'http://swopenapi.seoul.go.kr/api/subway/sample/xml/realtimeStationArrival/0/5/'
    link += name
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'lxml-xml')
    arrival_list = soup.findAll('row')
    if len(arrival_list) == 0:
        print("API 서버상의 에러거나 도착 예정인 전철이 없습니다.")
        return
    arrival_list_by_route = {}
    for arrival_info in arrival_list:
        route = arrival_info.find('subwayId').string
        if route in arrival_list_by_route.keys():
            arrival_list_by_route[route].append(arrival_info)
        else:
            arrival_list_by_route[route] = [arrival_info]
    dest_list = []
    string = ''
    for route in arrival_list_by_route.keys():
        for arrival_info in arrival_list_by_route[route]:
            if arrival_info.find('subwayId').string != '1002':
                if arrival_info.find('trainLineNm').string in dest_list:
                    continue
                else:
                    dest_list.append(arrival_info.find('trainLineNm').string)
                    string += arrival_info.find('bstatnNm').string + ' 방면 ' + arrival_info.find('arvlMsg2').string + '\n'
            else:
                if arrival_info.find('updnLine').string in dest_list:
                    continue
                else:
                    dest_list.append(arrival_info.find('updnLine').string)
                    string += arrival_info.find('updnLine').string + ' 방면 ' + arrival_info.find('arvlMsg2').string + '\n'
    print(string)


main()