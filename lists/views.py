from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'index.html')

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-url/')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'view.html', {'items': items})
 
