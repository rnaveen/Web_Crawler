# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 17:53:25 2017

@author: 5558
"""
import pandas as pd
import urllib3 as ul
from bs4 import BeautifulSoup
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver

link = 'http://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx'
http = ul.PoolManager()

page = http.request('GET', link)

soup = BeautifulSoup(page.data)
# years = soup.find_all('select', id='cphBody_cboYear')
cust_years = ['2020', '2019']
cust_months = [] #['January', 'June', 'December']
cust_states = ['Telangana']
cust_commodities = ['15']
file_name = 'AgMarket' + cust_states[0] + cust_commodities[0] + '.csv'

dowait = True
# write header to the csv file
data = []  # ['','','','','','','']
agMarktbl = pd.DataFrame(data,
                         columns=['Index', 'Market', 'Arrival Date', 'Arrivals (Tonnes)', 'Variety', 'Minimum Price',
                                  'Maximum Price', 'Modal Price'])
agMarktbl.to_csv(file_name, index=0)

# path for the chromedriver
driver = webdriver.Chrome("/Users/../SWPlayArea/Web_Crawler/chromedriver")
driver.get(link)

path = '//select[@id="cphBody_cboYear"]'
year_element = driver.find_element_by_xpath(path)
year_select = Select(year_element)

year_values = ['%s' % o.get_attribute('value') for o in year_select.options[1:]]
#year_values = ['2020', '2019']


def get_year_select():
    path = '//select[@id="cphBody_cboYear"]'
    year_select_elem = driver.find_element_by_xpath(path)
    year_select = Select(year_select_elem)
    return year_select


def get_month_select():
    path = '//select[@id="cphBody_cboMonth"]'
    month_select_elem = driver.find_element_by_xpath(path)
    month_select = Select(month_select_elem)
    return month_select


def get_state_select():
    path = '//select[@id="cphBody_cboState"]'
    state_select_elem = driver.find_element_by_xpath(path)
    state_select = Select(state_select_elem)
    return state_select


def get_commodity_select():
    path = '//select[@id="cphBody_cboCommodity"]'
    commodity_select_elem = driver.find_element_by_xpath(path)
    commodity_select = Select(commodity_select_elem)
    return commodity_select


def select_year_option(value, dowait=True):
    '''
    Select state value from dropdown. Wait until district dropdown
    has loaded before returning.
    '''
    path = '//select[@id="cphBody_cboMonth"]'
    month_select_elem = driver.find_element_by_xpath(path)

    def month_select_updated(driver):
        try:
            month_select_elem.text
        except StaleElementReferenceException:
            return True
        except:
            pass

        return False

    year_select = get_year_select()
    year_select.select_by_value(value)

    if dowait:
        wait = WebDriverWait(driver, 20)
        wait.until(month_select_updated)

    return get_month_select()


def select_month_option(value, dowait=True):
    '''
    Select state value from dropdown. Wait until district dropdown
    has loaded before returning.
    '''

    def state_select_updated(driver):
        try:
            state_select_elem.text
        except StaleElementReferenceException:
            return True
        except:
            pass

        return False

    month_select = get_month_select()
    month_select.select_by_value(value)

    wait = WebDriverWait(driver, 30)
    visible_element = wait.until(ec.visibility_of_element_located((By.ID, "cphBody_cboState")))
    """
    if dowait:
        path = '//select[@id="cphBody_cboState"]'
        #time.sleep(20)
        #state_select_elem = driver.find_element_by_xpath(path)
        wait = WebDriverWait(driver, 30)
        #time.sleep(10)
        # wait.until(state_select_updated)
        print('before')
        #fast = wait.until(ec.visibility_of_element_located((By.XPATH,path)));
       # fastrack = WebDriverWait(driver, 50).until(
        #    ec.visibility_of_element_located((By.XPATH, "//select[@id='cphBody_cboState']")))
        print('after')
        # wait = WebDriverWait(driver, 100)
        visible_element = wait.until(ec.visibility_of_element_located((By.ID, "cphBody_cboState")))
        # wait.until(state_select_updated)
    """
    return get_state_select()


def select_state_option(value, dowait=True):
    '''
    Select state value from dropdown. Wait until commodity dropdown
    has loaded before returning.
    '''

    def commodity_select_updated(driver):
        try:
            commodity_select_elem.text
        except StaleElementReferenceException:
            return True
        except:
            pass

        return False

    state_select = get_state_select()
    state_select.select_by_value(value)
    wait = WebDriverWait(driver, 30)
    visible_element = wait.until(ec.visibility_of_element_located((By.ID, "cphBody_cboCommodity")))

    """
    if dowait:
        time.sleep(10)
        path = '//select[@id="cphBody_cboCommodity"]'
        commodity_select_elem = driver.find_element_by_xpath(path)
        wait = WebDriverWait(driver, 20)
        time.sleep(10)
        #wait.until(commodity_select_updated)
    """
    return get_commodity_select()


def select_commodity_option(value, dowait=True):
    commodity_element = get_commodity_select()
    commodity_element.select_by_value(value)


def rename(commodity, year, month):
    os.rename('/Users/../Downloads/Agmarknet_Commodity___Cotton_State___Telangana.xls',
              '/Users/../Downloads/%s_%s_%s.xlsx' % (commodity, year, month))


def submit_download(values, month, state, commodity):
    select_commodity_option(commodity)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait = WebDriverWait(driver, 30)
    visible_element = wait.until(ec.visibility_of_element_located((By.ID, "cphBody_btnSubmit")))
    driver.find_element_by_id("cphBody_btnSubmit").click()
    time.sleep(5)
    # driver.find_element_by_id("cphBody_Button1").click()
    # time.sleep(5)
    # rename(commodity,values,month)
    # driver.find_element_by_id("cphBody_btnBack").click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    agMarkgrid = soup.find('table', {'id': 'cphBody_gridRecords'})
    tbody = agMarkgrid.find('tbody')
    data = []
    row = ''
    district = ''
    for tr in tbody.find_all('tr'):
        row = [td.text for td in tr.find_all('td')]

        data.append(row)

    agMarktbl = pd.DataFrame(data)
    agMarktbl.to_csv(file_name, mode='a', header=False)
# get custom year values from the top
if cust_years:  year_values = cust_years

for values in year_values:

    k = 1
    months = select_year_option(values)
    month_values = ['%s' % o.get_attribute('value') for o in months.options[1:]]
    # month_values = ['January', 'June']
    if cust_months:  month_values = cust_months
    for month in month_values:
        curr_month = pd.Timestamp('today').month_name()
        curr_year = pd.Timestamp('today').year

        if (values == str(curr_year)) and (month == curr_month) : break
        j = 0
        if k != 1:
            select_year_option(values)
        states = select_month_option(month)
        state_values = ['%s' % o.get_attribute('value') for o in states.options[1:]]
        if cust_states :  state_values = cust_states
        for state in state_values:
            commodities = select_state_option(state)
            commodity_values = ['%s' % o.get_attribute('value') for o in commodities.options[1:]]
            if cust_commodities: commodity_values = cust_commodities
            for commodity in commodity_values:
                select_commodity_option(commodity)
                submit_download(values, month, state, commodity)

                driver.close()
                k = k + 1
                # path for the chromedriver
                driver = webdriver.Chrome("/Users/../SWPlayArea/Web_Crawler/chromedriver")
                driver.get(link)

                path = '//select[@id="cphBody_cboYear"]'
                year_element = driver.find_element_by_xpath(path)
                year_select = Select(year_element)
