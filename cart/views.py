import datetime
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from cart.models import Cart, CartItem
from item.models import Item

# Create your views here.
def add_to_cart(request, item_id):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse("login"))
    cart, created = Cart.objects.get_or_create(customer=user)
    print("cart created!!!", cart, created)
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)
        # print(item)
        # print(cart)
        cartItem, cartItem_created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not cartItem_created:
            cartItem.quantity += 1
            print("updated quantity", cartItem.quantity)
            cartItem.save()
        messages.success(
            request=request,
            message=f"Quantity {cartItem.quantity} of {cartItem.item.name} added",
            extra_tags={"created_at": str(datetime.datetime.now())},
        )
        return redirect(reverse("list_items"))
    return render(request, 'car/show.html', context={"cart": cart})
        
    
@login_required
def show_cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    return render(request, 'cart/show.html', context={"cart": cart})

@login_required
def update_cart(request, item_id: int):
    action = request.POST.get("action")
    quantity = int(request.POST.get("quantity"))
    print(request.POST, action)
    cart = get_object_or_404(Cart, customer=request.user)
    try:
        cartItem = get_object_or_404(CartItem, id=item_id, cart__id=cart.id)
    except Http404:
        messages.error(
            request,
            message="Item is not in your cart anymore."
        )
        return redirect(reverse('show_cart'))
    if action == "remove":
        cartItem.delete()
    elif action == "increase" or action == "decrease":
        if quantity == 0:
            cartItem.delete()
            messages.success(
                request=request,
                message=f"{cartItem.item.name} removed!!!",
                extra_tags="cartitem_removed",
            )
        else:
            prev_quantity = cartItem.quantity
            cartItem.quantity = quantity
            cartItem.save()
            messages.success(
                request=request,
                message=f"{cartItem.item.name} quantity updated from {prev_quantity} to {quantity}",
                extra_tags="cartitem_updated",
            )
    cart = get_object_or_404(Cart, customer=request.user)
    return render(request, 'cart/show.html', context={"cart": cart})
