from django.test import TestCase
from lists.forms import (
   ItemForm,
   ExistingListItemForm,
   EMPTY_ITEM_ERROR,
   DUPLICATE_ITEM_ERROR
)
from lists.models import Item, List

class ItemFormTest(TestCase):
    
    def test_ItemForm_has_placeholder_and_classes(self):
        form = ItemForm()
        self.assertIn('placeholder', form.as_p())
        self.assertIn('class="input"', form.as_p())

    def test_ItemForm_validation_for_empty_input(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_ItemForm_can_save_item(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'test'})
        form.save(for_list=list_)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(List.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'test')
        self.assertEqual(item.list, list_)


class ExistingListItemFormTest(TestCase):

    def test_ExistingListItemForm_has_placeholder_and_classes(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder', form.as_p())
        self.assertIn('class="input"', form.as_p())

    def test_ExistingLIstItemForm_validation_for_empty_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(data={'text': ''}, for_list=list_)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)

        form = ExistingListItemForm(data={'text': 'bla'}, for_list=list_)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
        
    def test_ExistingListItemForm_can_save_item(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(data={'text': 'test'}, for_list=list_)

        form.save()
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(List.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'test')
        self.assertEqual(item.list, list_)

        
