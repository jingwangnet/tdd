from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
        

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_stlying(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 756)

        # she notices the inputbox  is necely centered
        inputbox = self.browser.find_element(By.ID, 'id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512, 
            delta=10
        )

        # she types something into text box
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_check_text_in_the_rows('1: Buy milk')

        # There is still a centered inputbox
        inputbox = self.browser.find_element(By.ID, 'id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512, 
            delta=10
        )
