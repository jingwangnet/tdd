from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import home_page
from .models import Item

# Create your tests here.
class HomePageTest(TestCase):

    def test_use_index_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'index.html')


class NewListTest(TestCase):

    def test_can_save_post_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new item'})
     
        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')

    def test_redirect_afeter_post_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-url/')


class ViewListTest(TestCase):

    def test_displays_all_items(self):
        Item.objects.create(text="item1")
        Item.objects.create(text="item2")

        response = self.client.get('/lists/the-only-url/')
        self.assertContains(response, "item1")
        self.assertContains(response, "item2")

    def test_use_view_template(self):
        response = self.client.get('/lists/the-only-url/')

        self.assertTemplateUsed(response, 'view.html')

class ItemModelTest(TestCase):
   
    def test_creating_items_and_retreiving_it_later(self):
        first_item = Item()
        first_item.text = "First item"
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.save()

        self.assertEqual(2, Item.objects.count())
        first_saved_item, second_saved_item = Item.objects.all()

        self.assertEqual(first_saved_item.text, 'First item')
        self.assertEqual(second_saved_item.text, 'Second item')



        
