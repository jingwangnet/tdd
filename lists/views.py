from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

# Create your views here.
def home_page(request):
    return render(request, 'index.html')

def new_list(request):
    Item.objects.create(text=request.POST.get('item_text', ''))
    return redirect('/lists/the-only-url/')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'view.html', {'items': items})
 
