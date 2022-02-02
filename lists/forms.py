from django import forms


class ItemForm(forms.Form):
    text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': "Enter a item list",
            'class': 'input',
        }
    ))
