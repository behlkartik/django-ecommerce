from http import HTTPStatus
from time import sleep
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Item
from django.urls import reverse
from .forms import ItemForm

# Create your views here.

@login_required
def list_items(request):
    searched_item = request.GET.get("q")
    if searched_item:
        item = Item.objects.get(name__icontains=searched_item)
        return render(request, 'item/show.html', context={"item": item})
    items = Item.objects.all()
    return render(request, 'item/list.html', context={"items": items})

@login_required
def show_item(request, name):
    item = Item.objects.get(name__contains=name)
    return render(request, 'item/show.html', context={"item": item})

@login_required
def create_item(request):
    form = ItemForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        # Item.objects.create(name=form.cleaned_data.get("name"), price=form.cleaned_data.get("price"), description=form.cleaned_data.get("description"))
        return redirect(reverse('list_items'))
    return render(request, 'item/create.html', context=context, status=HTTPStatus.OK)