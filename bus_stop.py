import time
import requests
from bs4 import BeautifulSoup
import lxml

link = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=1234567890&keyword='
for x in range(100000):
    req = requests.get(link + str(x).zfill(5))
    soup = BeautifulSoup(req.content, "lxml-xml")
    result = soup.find_all('busStationList')
    print(len(result))
    time.sleep(1)
