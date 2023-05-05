import time
import json
import requests
from bs4 import BeautifulSoup
import js2py
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


CHROME_DRIVER_PATH = "D:\Development\chromedriver.exe"
FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSd_OV7cM7ASC0-YOd504Fz0oqZPfLF-FIvReaBF2ISUiIql5w/viewform?usp=sf_link'
ZILLOW_URL = 'https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A37.94091233943231%2C%22east%22%3A-122.18476382617187%2C%22south%22%3A37.60929971309133%2C%22west%22%3A-122.68189517382812%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
page = '/san-francisco-ca/rentals/2_p'
search_query = f'https://www.zillow.com/san-francisco-ca/rentals/{page}_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.85814866321172%2C%22east%22%3A-122.30904666308594%2C%22south%22%3A37.69234228071924%2C%22west%22%3A-122.55761233691406%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
zillow ='https://www.zillow.com'

def fill_form(a, b, c):
    service = Service(CHROME_DRIVER_PATH)
    option = webdriver.ChromeOptions()
    option.add_argument("user-agent=Request")
    driver = webdriver.Chrome(service=service, options=option)
    driver.get(FORM_LINK)
    list = [a, b, c]
    time.sleep(3)
    inputs = driver.find_elements('xpath', "//input[contains(@class,'whsOnd zHQkBf')]")

    for i in inputs:
        idx = inputs.index(i)
        i.send_keys(list[idx])

    send = driver.find_element('xpath',"//div[contains(@jsname,'M2UYVd')]")
    send.click()
    time.sleep(2)


header = {
    'User-Agent': 'Requests',
    'Content-Type': 'application/json'
}

response = requests.get(url=ZILLOW_URL, headers=header)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

nr_of_pages = int(soup.select_one('.blgxcD').getText().split()[-1])

addresses = []
prices = []
links = []

for page in range(1, nr_of_pages+1):
    if page == 1:
        url = ZILLOW_URL
    else:
        url = f'https://www.zillow.com/san-francisco-ca/rentals/{page}_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A{page}%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.85814866321172%2C%22east%22%3A-122.30904666308594%2C%22south%22%3A37.69234228071924%2C%22west%22%3A-122.55761233691406%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'

    response = requests.get(url=url, headers=header)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    all = soup.select_one("script[data-zrr-shared-data-key]").getText().strip('<!--').strip('-->')
    all = json.loads(all)
    page_results = all['cat1']['searchResults']['listResults']

    for result in page_results:
        address = result['address']
        if zillow not in result['detailUrl']:
            link = f"{zillow}{result['detailUrl']}"
        else:
            link = result['detailUrl']
        try:
            price = result['units'][0]['price']
        except KeyError:
            price = result['price']
        addresses.append(address)
        prices.append(price)
        links.append(link)
        fill_form(address, price, link)

