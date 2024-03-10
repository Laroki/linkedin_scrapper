from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import os
from dotenv import load_dotenv

load_dotenv()
LI_AT = os.getenv('LI_AT')

class ProfileScrapper:
    driver = webdriver.Firefox()
    driver.maximize_window()
    timeout = 10
    profile = {}
    profiles = []
    

    def __init__(self, peopleListToScrap):
        self.driver.get("https://www.linkedin.com/")
        self.driver.add_cookie({"name":"li_at","value": LI_AT})

        for peopleURL in peopleListToScrap:
            self.driver.implicitly_wait(5)
            self.driver.get(peopleURL)
            self._scrollToBottom()
            self._setFullName()
            self._setCurrentJob()
            print(self.profile)
            self.profiles.append(self.profile)
            self.profile = {}

        self._listToCSV(self.profiles)
        self.profile = {}
        self.profiles = []
        print('EXIT')

    def _setFullName(self):
        self.profile['fullName'] = self._findByCSSSelector('main section h1').text
    
    def _setCurrentJob(self):
        experienceSection: WebElement = self._findByCSSSelector('div#experience').parent

        try:
            element = experienceSection.find_element(by=By.CSS_SELECTOR, value='div.pvs-list__outer-container > ul.pvs-list > li:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
            self.profile['job'] = element.text
        except NoSuchElementException:
            self.profile['job'] = 'N/A'

        try:
            element = experienceSection.find_element(by=By.CSS_SELECTOR, value='div.pvs-list__outer-container > ul.pvs-list > li:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > span:nth-child(1)')
            self.profile['company'] = element.text
        except NoSuchElementException:
            self.profile['company'] = 'N/A'

    def _findByCSSSelector(self, cssSelector):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_element(by=By.CSS_SELECTOR, value=cssSelector)
        except TimeoutException:
            print("Timed out waiting for element")

    def _scrollToBottom(self):
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def _listToCSV(self, list):
        with open('dataset.csv', 'a', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=list[0].keys())
            # fc.writeheader()
            fc.writerows(list)