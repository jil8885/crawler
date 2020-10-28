import json, requests

dest_list = []

def main():
    stn_name = input()
    print(search(stn_name))


def dest(total_cnt) -> bool:
    global dest_list
    cnt = 0
    for x in dest_list:
        if x == cnt:
            cnt += 1
    return cnt == total_cnt

# 역별로 이름 받아서 찾아주는 함수
def search(name):
    global dest_list
    link = f'http://swopenapi.seoul.go.kr/api/subway/sample/json/realtimeStationArrival/0/5/{name}'
    # 역명을 주소 뒤에 이어서 서버에 요청 보냄
    response = requests.get(link)
    try:
        soup = json.loads(response.content)
    except:
        print("503 Error")
        return 
    arrival_list = soup['realtimeArrivalList']
    # 503 에러거나 도착 정보가 없을 때
    if len(arrival_list) == 0:
        print("API 서버상의 에러거나 도착 예정인 전철이 없습니다.")
        return
    # 노선 별로 수신 정보 분리
    arrival_list_by_route = {}
    for arrival_info in arrival_list:
        route = arrival_info['subwayId']
        if route in arrival_list_by_route.keys():
            arrival_list_by_route[route].append(arrival_info)
        else:
            arrival_list_by_route[route] = [arrival_info]
    # 목적지 별로 분리
    string = ''
    for route in arrival_list_by_route.keys():
        for arrival_info in arrival_list_by_route[route]:
            # 2호선이 아닐 때는 종착역으로 분리
            if arrival_info['subwayId'] != '1002':
                # 이미 출력 문자열에 들어간 목적지일 때는,
                if dest(arrival_info['trainLineNm'], 2):
                    continue
                else:
                    dest_list.append(arrival_info['trainLineNm'])
                    string += arrival_info['bstatnNm'] + ' 방면 ' + arrival_info['arvlMsg2'] + '\n'
            # 2호선일 때는 내외선으로 분리
            else:
                # 이미 출력 문자열에 들어간 목적지일 때는,
                if dest(arrival_info['updnLine'], 2):
                    continue
                else:
                    dest_list.append(arrival_info['updnLine'])
                    string += arrival_info['updnLine'] + ' 방면 ' + arrival_info['arvlMsg2'] + '\n'
    return string


main()
