from django.test import TestCase
from lists.forms import ItemForm

class ItemFormTest(TestCase):
    
    def test_ItemForm_has_placeholder_and_classes(self):
        form = ItemForm()
        self.assertIn('placeholder', form.as_p())
        self.assertIn('class="input"', form.as_p())
        
