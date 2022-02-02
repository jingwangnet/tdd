from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
from .base import FunctionalTest



class ItemVlidationTest(FunctionalTest):

    def test_cannot_and_empty_list_items(self):
        # Edith goes to the home page and accidentally trires to sumbit
        # an empty list item, She hists ENTER on the empty input box
        self.browser.get(self.live_server_url)
        inputbox = self.get_inputbox()
        inputbox.send_keys(Keys.ENTER)

        # The page refreshes, and there is an error message saying
        # that list item cannot be blank
        self.wait_for(lambda: self.assertTrue(
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        ))

        # she tries agian with some text for the item, which now works
        inputbox = self.get_inputbox()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_check_text_in_the_rows('1: Buy milk')

        # perversly, she now decides to sumibt a second blank item 
        inputbox = self.get_inputbox()
        inputbox.send_keys(Keys.ENTER)
        # she recives a similar wrarning on the list page
        self.wait_for(lambda: self.assertTrue(
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        ))

        # and she can coorect it by filling some text in the text box
        inputbox = self.get_inputbox()
        inputbox.send_keys('Buy vegetables')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_check_text_in_the_rows('2: Buy vegetables')
        self.wait_for_check_text_in_the_rows('1: Buy milk')




