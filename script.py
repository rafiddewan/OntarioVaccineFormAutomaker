import os
import sys
from csv import reader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict


def readParams(filename):
    with open(filename, newline='') as iris:
        # returning from 2nd row
        return list(reader(iris, delimiter=','))[1:]

params = readParams('Ontario Covid Vaccine - Sheet1.csv')

chromedriver_location = params[0][7]

driver = webdriver.Chrome(chromedriver_location)
driver.implicitly_wait(10000)
driver.get('https://covid19.ontariohealth.ca/app-identity?viewId=9MYRZKKV92R7')

params = readParams('Ontario Covid Vaccine - Sheet1.csv')
#Page 1
hcn_xpath = '//*[@id="hcn"]'
hcn_back_xpath = '//*[@id="scn"]'
vn_xpath = '//*[@id="vcode"]'
dob_xpath = '//*[@id="dob"]'
postal_code_xpath = '//*[@id="postal"]'
continue_button = '//*[@id="continue_button"]'
continue_to_vacine = '//*[@id="booking_button"]'

driver.find_element_by_xpath(hcn_xpath).send_keys(params[0][0])
driver.find_element_by_xpath(vn_xpath).send_keys(params[0][1])
driver.find_element_by_xpath(hcn_back_xpath).send_keys(params[0][2])
driver.find_element_by_xpath(dob_xpath).send_keys(params[0][3])
driver.find_element_by_xpath(postal_code_xpath).send_keys(params[0][4])
driver.find_element_by_xpath(continue_button).click()

#sleep(1)
#Ensures that the script does not exit during the queue wait time. 
WebDriverWait(driver,10000).until(EC.element_to_be_clickable((By.ID, "booking_button")))
driver.find_element_by_xpath(continue_to_vacine).click()

#Page 2
'''
eligible_xpath = '//*[@id="eligibility_fieldset"]/div/div[1]'
next_page_button = '//*[@id="register_button"]'
driver.implicitly_wait(10000)
driver.find_element_by_xpath(eligible_xpath).click()


driver.implicitly_wait(10000)
driver.find_element_by_xpath(next_page_button).click()
'''

#Ensures that the script does not exit during the queue wait time. 
WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.ID, "email")))

email_xpath = '//*[@id="email"]'
confirm_email_xpath = '//*[@id="emailx2"]'
mobile_phone_xpath = '//*[@id="mobile"]'
vaccination_booking_xpath = '//*[@id="schedule_button"]'
driver.find_element_by_xpath(email_xpath).send_keys(params[0][5])
driver.find_element_by_xpath(confirm_email_xpath).send_keys(params[0][5])
driver.find_element_by_xpath(mobile_phone_xpath).send_keys(params[0][6])
driver.find_element_by_xpath(vaccination_booking_xpath).click()

#Ensures that the script does not exit during the queue wait time. 
driver.implicitly_wait(10000)

#Page 3
your_location_xpath = '//*[@id="root"]/div/main/div/div[4]/button'
address_booking_xpath = '//*[@id="location-search-input"]'
driver.find_element_by_xpath(your_location_xpath).click()

driver.implicitly_wait(10000)

#Page 4
select_location_xpath = '//*[@id="root"]/div/main/div[1]/div[2]/div[1]/div[2]/button'
driver.find_element_by_xpath(select_location_xpath).click()

driver.implicitly_wait(10000)