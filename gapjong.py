import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3,time

def rail(trn_no):
    import time
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('./chromedriver',chrome_options=options)
    driver.implicitly_wait(5)
    response = driver.get('http://m.logis.korail.com/smartindex.do')
    driver.find_element_by_xpath('//*[@id="mbody"]/tbody/tr[3]/td[1]/a').click()
    driver.find_element_by_name('trn_no').send_keys(str(trn_no))
    driver.find_element_by_xpath('//*[@id="bottom_bar"]/div/ul/a').click()
    try:
        alert = driver.switch_to_alert()
    except:
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        pos = soup.select('tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td')
        result = []
        for x in pos:
            if x.text.strip() != '':
                result += [x.text.strip()]
        string = '열차번호 : #'+str(trn_no)+'\n'
        string += result[1]+' >> '+result[3]+'\n'
        string += '현재위치 : '+result[2]+'\n'
        string += '지연시간 : '+result[-1]
        print(string)
    return

rail(7405)