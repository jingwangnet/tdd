from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm

# Create your views here.
def home_page(request):
    form = ItemForm()
    return render(request, 'index.html', {'form': form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'index.html', {'form': form})

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'view.html', {'list': list_, 'form': form})
