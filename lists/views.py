from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
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
    except ValidationError:
        list_.delete()
        error="You can't have an empty item"
        return render(request, 'index.html', {'error': error})
    return redirect(f'/lists/{list_.pk}/')

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    error = None
    if request.method == 'POST':
        item = Item(text=request.POST['item_text'], list=list_)
        try:
           item.full_clean()
           item.save()
           return redirect(f'/lists/{list_.pk}/')
        except ValidationError:
            error="You can't have an empty item"
    return render(request, 'view.html', {'list': list_, 'error': error})
 
