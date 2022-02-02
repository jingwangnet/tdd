from django.test import TestCase
from lists.forms import ItemForm
from lists.models import Item, List

class ItemFormTest(TestCase):
    
    def test_ItemForm_has_placeholder_and_classes(self):
        form = ItemForm()
        self.assertIn('placeholder', form.as_p())
        self.assertIn('class="input"', form.as_p())

    def test_ItemForm_validation_for_empty_input(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ["You can't have an empty item"])

    def test_ItemForm_can_save_item(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'test'})
        form.save(for_list=list_)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(List.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'test')
        self.assertEqual(item.list, list_)

        
        
