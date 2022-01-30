from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from django.test import LiveServerTestCase

import time


MAX_TIME = 5


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def wait_for_check_text_in_the_rows(self, text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(
                    text, 
                    [row.text for row in rows] 
                )
                return 
            except (AssertionError, WebDrivertException) as e:
                if time.time() - start_time > MAX_TIME:
                    raise e
                time.sleep(0.2)
                

    def test_start_a_list_for_one_user(self):
        # Edith has heard about a cool new oneline to-do app, She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do lists', self.browser.title)

        # she is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter a to-do item"
        )

        # she types 'Buy peacock feathers' into a text box 
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # She she hits enter, the page updates, and now the page lists
        # '1: Buy peacock feathers' as an item in a to-do lists
        self.wait_for_check_text_in_the_rows('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item, She
        # enters "Use peacock feathers to make a fly' 
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both item on her list
        self.wait_for_check_text_in_the_rows('2: Use peacock feathers to make a fly')
        self.wait_for_check_text_in_the_rows('1: Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_diffrent_url(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_check_text_in_the_rows('1: Buy peacock feathers')

        # She notices that her list has a unique url
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, '/lists/.+/')

        # Now a new user, Francis, comes along to the site
        self.browser.quit()
        self.setUp()

        # Francis visits the home page, there is no sign of Edith's list
        self.browser.get(self.live_server_url)

        html_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assrtNotIn('Buy peacock feathers', html_page)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_check_text_in_the_rows('1: Buy milk')

        # Francis gets his own unique URL
        francis_url = self.browser.current_url 
        self.assertRegex(francis_url, '/lists/.+/')
        self.assertNotEqual(francis_url, edith_url)

        # Agian, there is no strace of Edith's list
        html_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assrtNotIn('Buy peacock feathers', html_page)

        
        




