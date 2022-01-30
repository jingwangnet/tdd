from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_use_index_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'index.html')



        
