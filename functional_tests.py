from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_start_a_list_for_one_user(self):
        # Edith has heard about a cool new oneline to-do app, She goes
        # to check out its homepage
        try:
            self.browser.get('http://127.0.0.1:8000')
        except WebDriverException:
            pass

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

        time.sleep(2)

        # She she hits enter, the page updates, and now the page lists
        # '1: Buy peacock feathers' as an item in a to-do lists
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(
            '1: BUy peacock feathers',
            [row.text for row in rows] 
        )

        # There is still a text box inviting her to add another item, She
        # enters "Use peacock feathers to make a fly' 

        # The page updates again, and now shows both item on her list

if __name__ == '__main__':
    unittest.main()
