from django import forms
from .models import Item
from django.core.exceptions import ValidationError


EMPTY_ITEM_ERROR = "You can't have an empty item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.ModelForm):

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
    
    class Meta:
        model = Item
        fields = ['text',]
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'input'
                }
            ),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }



class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.ModelForm.save(self)

