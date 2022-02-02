from django.test import TestCase
from lists.views import home_page
from lists.models import Item, List

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

        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.pk}/')

    def test_validation_error_sent_back_on_index_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        expect_error = "You can't have an empty item"
        self.assertContains(response, expect_error)

    def test_do_not_save_invalid_list_item(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(0, Item.objects.count())
        self.assertEqual(0, List.objects.count())


class ViewListTest(TestCase):

    def test_displays_all_items_for_that_list(self):
        other_list = List.objects.create()
        Item.objects.create(text="other item1", list=other_list)
        Item.objects.create(text="other item2", list=other_list)
        correct_list = List.objects.create()
        Item.objects.create(text="correct item1", list=correct_list)
        Item.objects.create(text="correct item2", list=correct_list)

        response = self.client.get(f'/lists/{correct_list.pk}/')
        self.assertContains(response, "correct item1")
        self.assertContains(response, "correct item2")
        self.assertNotContains(response, "other item1")
        self.assertNotContains(response, "other item2")

    def test_use_view_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')

        self.assertTemplateUsed(response, 'view.html')

    def test_passes_list_instance(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')

        self.assertEqual(response.context['list'], list_)

    def test_can_save_post_request_for_existing_list(self):
        list_ = List.objects.create()
        self.client.post(f'/lists/{list_.pk}/', data={'item_text': 'A new item'})
     
        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')
        self.assertEqual(item.list, list_)

    def test_redirect_afeter_post_request(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.pk}/', data={'item_text': 'A new item'})

        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.pk}/')

    def test_validation_error_end_on_view_template(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.pk}/', data={'item_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')
        expect_error = "You can't have an empty item"
        self.assertContains(response, expect_error)


