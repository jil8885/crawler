from datetime import datetime
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3,time

def rail(trn_no):
    now = datetime.now().strftime('%Y%m%d')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(5)
    link = 'https://zermoth.net/railroad/logis/Default.aspx?train='+str(trn_no)+'&date='+now+'#!'
    response = driver.get(link)
    try:
        alert = driver.switch_to_alert()
    except:
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        string = '열차번호 : '+str(trn_no)+'\n'
        pos = soup.select('b > span > a')
        string += pos[1].text + ' >> ' + pos[0].text+'\n'
        pos = soup.select('#spDrive > b > span > a')
        status = soup.select('#spDrive > span')
        if '종료' in status[0].text:
            string += status[0].text
        else:
            string += '현재위치 : '+pos[0].text +' - ' + pos[1].text +' 간 운행중'
    print(string)
    return
rail(1212)
