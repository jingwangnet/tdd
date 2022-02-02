from django.test import TestCase
from lists.views import home_page
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import (
    ItemForm,
    ExistingListItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR
)

# Create your tests here.
class HomePageTest(TestCase):

    def test_uses_index_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'index.html')

    def test_uses_ItemForm(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)



class NewListTest(TestCase):

    def test_can_save_post_request(self):
        self.client.post('/lists/new', data={'text': 'A new item'})
     
        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')

    def test_redirect_afeter_post_request(self):
        response = self.client.post('/lists/new', data={'text': 'A new item'})

        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.pk}/')

    def test_for_invalid_input_renders_index_template(self):
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})

        expect_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expect_error)

    def test_do_not_save_invalid_list_item(self):
        self.client.post('/lists/new', data={'text': ''})
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

    def test_uses_ItemForm(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')

        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_passes_list_instance(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')

        self.assertEqual(response.context['list'], list_)

    def test_can_save_post_request_for_existing_list(self):
        list_ = List.objects.create()
        self.client.post(f'/lists/{list_.pk}/', data={'text': 'A new item'})
     
        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')
        self.assertEqual(item.list, list_)

    def test_redirect_afeter_post_request(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.pk}/', data={'text': 'A new item'})

        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.pk}/')

    def post_invalid_request(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.pk}/',
            data={'text': ''}
        )

    def test_for_invalid_input_noting_saved_to_db_(self):
        self.post_invalid_request()

        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_temlate(self):
        response = self.post_invalid_request()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_request()

        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_showsL_error_on_page(self):
        response = self.post_invalid_request()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
        expect_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expect_error)


    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'view.html')
        self.assertEqual(Item.objects.all().count(), 1)


