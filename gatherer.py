from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class Gatherer:
    timeout = 5
    maxPageValue = 0

    def __init__(self, driver: webdriver.Firefox):
        self.driver = driver
        self.getPageMax()

    def getPageMax(self):
        time.sleep(2)
        self.driver.implicitly_wait(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-pagination__pages"))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            maxPageValue = self.driver.find_element(by=By.CSS_SELECTOR, value="ul.artdeco-pagination__pages.artdeco-pagination__pages--number li:last-child button span").text
            print(maxPageValue)
        except TimeoutException:
            print("No pagination")
        