# For web request
import requests, os, time, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# For google firestore query
from firebase_admin import credentials, firestore, initialize_app
#For json dump
import json

def crawling_lib():
    # Env for web reqeust
    chrome_options = webdriver.ChromeOptions()
    try:
        # chrome_options.binary_location = "/usr/bin/brave-browser"
        driver = webdriver.Chrome('C:\\Users\\Jeongin\\Desktop\\chromedriver', options=chrome_options)
    except:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("/home/Jeongin/chromedriver", options=chrome_options)

    # Google Firestore setup
    # Change cert path by your env
    try:
        cred = credentials.Certificate('C:\\Users\\Jeongin\\Downloads\\personal-sideprojects-3e0ca032c482.json')
    except:
        cred = credentials.Certificate('/home/Jeongin/google-firebase.json')
    initialize_app(cred)
    db_client = firestore.client()
    db = db_client.collection("libinfo")

    # ERICA Campus
    request_url = "http://information.hanyang.ac.kr/#/smuf/seat/status"
    now = datetime.datetime.now()
    driver.get(request_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ikc-container.ng-scope > div.ikc-content > div > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > span:nth-child(2)")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.findAll("span", {"ng-bind": "s.name"})
        total = soup.findAll("span", {"ng-bind": "s.activeTotal"})
        active = soup.findAll("span", {"ng-bind": "s.occupied"})
        percent = soup.findAll("span", {"ng-bind": "s.rate + '%'"})
        for x in range(len(name)):
            db_doc = db.document('ERICA').collection('library_list').document(name[x].text)
            db_doc.set({
                'total': int(total[x].text),
                'active': int(active[x].text),
                'occupied': percent[x].text,
                'time' : now
            })
    finally:
        # driver.close()
        pass

    # Seoul Campus
    request_url = "http://library.hanyang.ac.kr/#/smuf/seat/status"
    driver.get(request_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ikc-content > div > div > div > div > table > tbody > tr:nth-child(1) > td.ikc-seat-name > span:nth-child(2)")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.findAll("span", {"ng-bind": "s.name"})
        total = soup.findAll("span", {"ng-bind": "s.activeTotal"})
        active = soup.findAll("span", {"ng-bind": "s.occupied"})
        percent = soup.findAll("span", {"ng-bind": "s.rate + '%'"})
        for x in range(len(name)):
            db_doc = db.document('Seoul').collection('library_list').document(name[x].text.split("[")[0])
            db_doc.set({
                'total': int(total[x].text),
                'active': int(active[x].text),
                'occupied': percent[x].text,
                'time' : now
            })
    finally:
        driver.close()
        driver.quit()
    return

crawling_lib()