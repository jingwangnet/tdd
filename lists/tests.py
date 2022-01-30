from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_use_index_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'index.html')

    def test_can_save_post_request(self):
        response = self.client.post('/', data={'item_text': 'A new item'})
        self.assertIn('A new item', response.content.decode())



        
