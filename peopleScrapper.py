from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time
from gatherer import Gatherer

load_dotenv()
LI_AT = os.getenv('LI_AT')

class PeopleScrapper:
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox()
    driver.maximize_window()
    timeout = 10

    def __init__(self, data):
        self.data = data
        self.driver.get("https://www.linkedin.com/")
        self._loggin()
        self.driver.implicitly_wait(5)
        self._searchPeople()

    def _loggin(self):
        self.driver.add_cookie({"name":"li_at","value": LI_AT})
        self.driver.get("https://www.linkedin.com/search/results/people/?keywords=remi+cakir&origin=GLOBAL_SEARCH_HEADER")

    def _searchPeople(self):
        self._setLocations(self.data[0]['locations'])
        self.driver.implicitly_wait(10)
        self._setCompanies(self.data[0]['companies'])
        self.driver.implicitly_wait(10)
        self._setKeywords(self.data[0]['keywords'])

    def _setKeywords(self, keywords):
        searchBox = self._findElementByCLASS("search-global-typeahead__input")
        searchBox.send_keys()

        for keyword in keywords:
            searchBox.clear()
            time.sleep(1)
            self.driver.implicitly_wait(1)
            searchBox.send_keys(keyword)
            time.sleep(1)
            self.driver.implicitly_wait(1)
            self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.implicitly_wait(1)
            searchBox.clear()
            # EXEC GATHERER
            Gatherer(self.driver)

    def _setLocations(self, locations):
        locationBtn = self._findElementByID('searchFilter_geoUrn')
        self.driver.implicitly_wait(5)
        locationBtn.click()
        self.driver.implicitly_wait(5)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.implicitly_wait(5)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        locationSearchBox = self.driver.switch_to.active_element

        for location in locations:
            time.sleep(1)
            self.driver.implicitly_wait(1)
            locationSearchBox.send_keys(location)
            time.sleep(1)
            self.driver.implicitly_wait(1)
            locationSearchBox.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            self.driver.implicitly_wait(1)
            locationSearchBox.send_keys(Keys.ENTER)
            locationSearchBox.clear()
        
        self.driver.implicitly_wait(1)
        locationSearchBox.send_keys(Keys.TAB)
        self.driver.implicitly_wait(1)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    def _setCompanies(self, companies):
        companiesBtn = self._findElementByID('searchFilter_currentCompany')
        self.driver.implicitly_wait(1)
        companiesBtn.click()
        self.driver.implicitly_wait(5)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.implicitly_wait(5)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        companiesSearchBox = self.driver.switch_to.active_element

        for company in companies:
            time.sleep(1)
            self.driver.implicitly_wait(1)
            companiesSearchBox.send_keys(company)
            time.sleep(1)
            self.driver.implicitly_wait(1)
            companiesSearchBox.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            self.driver.implicitly_wait(1)
            companiesSearchBox.send_keys(Keys.ENTER)
            companiesSearchBox.clear()

        self.driver.implicitly_wait(1)
        companiesSearchBox.send_keys(Keys.TAB)
        self.driver.implicitly_wait(1)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    def _findFilters(self, cssSelector):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_elements(by=By.CSS_SELECTOR, value=cssSelector)
        except TimeoutException:
            print("Timed out waiting for element")

    def _findElementByID(self, id):
        try:
            element_present = EC.presence_of_element_located((By.ID, id))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_element(by=By.ID, value=id)
        except TimeoutException:
            print("Timed out waiting for element")

    def _findElementByXPATH(self, xpath):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_element(by=By.XPATH, value=xpath)
        except TimeoutException:
            print("Timed out waiting for element")

    def _findElementByCLASS(self, className):
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, className))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_element(by=By.CLASS_NAME, value=className)
        except TimeoutException:
            print("Timed out waiting for element")

    def _findElementByTAG(self, tagName):
        try:
            element_present = EC.presence_of_element_located((By.TAG_NAME, tagName))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_element(by=By.TAG_NAME, value=tagName)
        except TimeoutException:
            print("Timed out waiting for element")
        
        
        