from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from django.test import LiveServerTestCase
import time


MAX_TIME = 5
def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.2)
    return modified_fn


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for_check_text_in_the_rows(self, text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(
            text, 
            [row.text for row in rows] 
        )

    @wait
    def wait_for(self, func):
        return func()

    def get_inputbox(self):
        return self.browser.find_element(By.ID, 'id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.LINK_TEXT,'Log out')
                
    @wait
    def wait_to_be_logged_out(self, email):
        lambda: self.browser.find_element(By.NAME, 'email')
