from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST.get('item_text', ''))
        new_item_text = item.text
    else:
        new_item_text = ''
       
    context = {'new_item_text': new_item_text }
    return render(request, 'index.html', context)
