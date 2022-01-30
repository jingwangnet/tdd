from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import unittest

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

        # she types 'Buy peacock feathers' into a text box 

        # She she hits enter, the page updates, and now the page lists
        # '1: Buy peacock feathers' as an item in a to-do lists

        # There is still a text box inviting her to add another item, She
        # enters "Use peacock feathers to make a fly' 

        # The page updates again, and now shows both item on her list

if __name__ == '__main__':
    unittest.main()
