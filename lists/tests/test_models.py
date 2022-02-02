from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
   
    def test_can_not_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text="", list=list_)
        with self.assertRaises(ValidationError):
            item.save() # Should raise ValidationError
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='bla', list=list_)
            item.full_clean()  # Should raise a Validation 

    def test_can_save_same_item_to_diffrent_lists(self):
        list1 = List.objects.create()
        Item.objects.create(text='bla', list=list1)
        list2 = List.objects.create()
        item = Item(text='bla', list=list2)
        item.full_clean()


    def test_creating_items_and_retreiving_it_later(self):
        list_ = List.objects.create()
        first_item = Item()
        first_item.text = "First item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.list = list_
        second_item.save()

        self.assertEqual(1, List.objects.count())
        self.assertEqual(2, Item.objects.count())
        saved_list = List.objects.first()
        first_saved_item, second_saved_item = saved_list.item_set.all()

        self.assertEqual(first_saved_item.text, 'First item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Second item')
        self.assertEqual(second_saved_item.list, list_)

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/1/')


    
        
