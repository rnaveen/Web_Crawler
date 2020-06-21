"""
Scrape
http://tsmarketing.in/DailyArrivalsnPricesBetweenDates.aspx

"""

import urllib3 as ul
from bs4 import BeautifulSoup
import time
import pandas as pd
import lxml

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from_date = "01-08-2019"
to_date = "31-03-2020"
commodity = ['25','1']

link = "http://tsmarketing.in/DailyArrivalsnPricesBetweenDates.aspx"
http = ul.PoolManager()

page = http.request("GET",link)

soup = BeautifulSoup(page.data)

driver = webdriver.Chrome("/Users/swapna/SWPlayArea/Web_Crawler/chromedriver")
driver.get(link)

from_date_id = '//input[@id="ContentPlaceHolder1_txtDate1"]'
from_date_element = driver.find_element_by_xpath(from_date_id)
from_date_element.clear()
from_date_element.send_keys(from_date)

to_date_id = '//input[@id="ContentPlaceHolder1_txtDate2"]'
to_date_element = driver.find_element_by_xpath(to_date_id)
to_date_element.clear()
to_date_element.send_keys(to_date)

commodity_id = '//select[@id="ContentPlaceHolder1_ddlCommodity"]'
commodity_element = driver.find_element_by_xpath(commodity_id)
commodity_select = Select(commodity_element)
commodity_select.select_by_value(commodity[1])
#commodity_values =  [ '%s' % o.get_attribute('value') for o in commodity_select.options[1:] ]

"""
for values in commodity_values:
    commodity_select.select_by_value(values)
    time.sleep(5)
"""
time.sleep(5)
#showbtn_id = '//input[@id="ContentPlaceHolder1_btnShow"]'
#showbtn_element = driver.find_element_by_xpath(showbtn_id)
# showbtn_element.click()

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
tsMarktbl = soup.find('table',{'id':'ContentPlaceHolder1_GridView1'})

tbody = tsMarktbl.find('tbody')

data = []
rows = tbody.find_all('tr')
columns = [cols.text for cols in rows[0].find_all('th')]
print(columns)

tsMark_df = pd.DataFrame(columns=columns)

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')
    if len(tds) == 7:
        values = '' , tds[0].text , tds[1].text, tds[2].text , tds[3].text , tds[4].text , tds[5].text , tds[6].text
    else:
        values = [td.text for td in tds]

    tsMark_df = tsMark_df.append(pd.Series(values, index=columns), ignore_index=True)
"""
for tr in tbody.find_all('tr'):
    row_head = [th.text for th in tr.find_all('th')]
    row = [td.text for td in tr.find_all('td')]
"""


#tsMark_df = pd.DataFrame(tsMark_df)
tsMark_df.to_csv('TSMarketdata6.csv', mode='a')