from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'index.html')

def new_list(request):
    list_ = List.objects.create()
    item=Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except:
        list_.delete()
        error="You can't have an empty item"
        return render(request, 'index.html', {'error': error})
    return redirect(f'/lists/{list_.pk}/')

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    return render(request, 'view.html', {'list': list_})
 
def add_item(request, pk):
    list_ = List.objects.get(pk=pk)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.pk}/')
