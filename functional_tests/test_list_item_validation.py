from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
from .base import FunctionalTest



class ItemVlidationTest(FunctionalTest):

    def test_cannot_and_empty_list_items(self):
        # Edith goes to the home page and accidentally trires to sumbit
        # an empty list item, She hists ENTER on the empty input box

        # The page refreshes, and there is an error message saying
        # that list item cannot be blank

        # she tries agian with some text for the item, which now works

        # perversly, she now decides to sumibt a second blank item 

        # she recives a similar wrarning on the list page

        # and she can coorect it by filling some text in the text box
        self.fail('write me')





