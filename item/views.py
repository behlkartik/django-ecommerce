from http import HTTPStatus
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Item
from django.urls import reverse
from .forms import ItemForm
from django.db.models import Q

# Create your views here.
def list_items(request):
    searched_item = request.GET.get("q")
    veg_nonveg_filter = request.GET.get("veg_nonveg")
    print(request.GET, searched_item, veg_nonveg_filter)
    if not searched_item:
        items = Item.objects.all()
    else:
        items = Item.objects.search(searched_item)
    if veg_nonveg_filter:
        items = items.filter(veg_nonveg__iexact=veg_nonveg_filter).all()
    return render(request, 'item/list.html', context={"items": items})

@login_required
def show_item(request, slug):
    item = Item.objects.get(slug=slug)
    return render(request, 'item/show.html', context={"item": item})

@login_required
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            # Item.objects.create(name=form.cleaned_data.get("name"), price=form.cleaned_data.get("price"), description=form.cleaned_data.get("description"))
            return redirect(reverse('list_items'))
    else:
        form = ItemForm()
    context = {
        "form": form
    }
    return render(request, 'item/create.html', context=context, status=HTTPStatus.OK)

@login_required
def edit_item(request, slug = None):
    if slug:
        item = Item.objects.get(slug__iexact=slug)
        print(item.name)
    form = ItemForm(request.POST or None, )
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect(reverse('list_items'))
    return render(request, 'item/create.html', context=context, status=HTTPStatus.OK)