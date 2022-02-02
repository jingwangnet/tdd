from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    
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
            'text': {'required': "You can't have an empty item"}
        }



