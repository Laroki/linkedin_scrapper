from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import time
from profileScrapper import ProfileScrapper

class Navigator:
    timeout = 2
    maxPageValue = 0
    peopleListToScrap: list[str] = []

    def __init__(self, driver: webdriver.Firefox, activeFilters):
        self.driver = driver
        self.activeFilters = activeFilters
        self._scrollToBottom()
        self._setMaxPageValue()
        self.peopleListToScrap = []

        if self.maxPageValue > 0:
            self._paginateAndStoreProfile()
        else:
            self._storeProfiles()

        #scrap profiles
        ProfileScrapper(self.peopleListToScrap)
        
    def _setMaxPageValue(self):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-pagination__pages"))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            self.maxPageValue = int(self.driver.find_element(by=By.CSS_SELECTOR, value="ul.artdeco-pagination__pages.artdeco-pagination__pages--number li:last-child button span").text)
            print(self.maxPageValue)
            self.currentUrl = self.driver.current_url
            print(self.currentUrl)
        except TimeoutException:
            print("No pagination")

    def _paginateAndStoreProfile(self):
        for index in range(1, self.maxPageValue + 1):
            print(self.activeFilters)
            print('current page: ' + str(index))
            if index != 1:
                # Navigate to URL
                self.driver.get(self.currentUrl + '&page=' + str(index))
                # Scroll To bottom
                self._scrollToBottom()
            # Store profile
            self._storeProfiles()

    def _findByCSSSelector(self, cssSelector):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_elements(by=By.CSS_SELECTOR, value=cssSelector)
        except TimeoutException:
            print("Timed out waiting for element")

    def _storeProfiles(self):
        peopleList = self._findByCSSSelector("ul.reusable-search__entity-result-list li div span.entity-result__title-line a")
        if peopleList is not None:
            for people in peopleList:
                link = people.get_attribute("href")
                if "/in/" in link:
                    print(link)
                    self.peopleListToScrap.append(link)
        else:
            print('NO PROFILES ON CURRENT PAGE')

    def _scrollToBottom(self):
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")