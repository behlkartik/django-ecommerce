from http import HTTPStatus
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms.models import modelformset_factory #model form for queryset

from cart.models import Cart
import item
from order.forms import OrderForm, OrderItemForm
from .models import Order, OrderItem, OrderStatus
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Create your views here.

@login_required
def list_orders(request):
    query = request.GET.get("q")
    if not query:
        orders = Order.objects.filter(customer=request.user)
    else:
        orders = Order.objects.search(query=query).filter(customer=request.user)
    context = {
        "orders": orders.order_by('-created_at')
    }
    return render(request, 'orders/list.html', context=context, status=HTTPStatus.OK)

@login_required
def show_order(request, order_id):
    order = Order.get_by_id(order_id=order_id)
    context = {
        "order": order
    }
    return render(request, 'orders/show.html', context=context, status=HTTPStatus.OK)


@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    form = OrderForm(request.POST or None, instance=order)
    # OrderItemFormset = modelformset_factory(OrderItem, form=OrderItemForm, extra=0)
    # qs = order.orderitem_set.all()
    # formset = OrderItemFormset(request.POST or None, queryset=qs) # take the querset and turn it into OrderItemForm
    context = {
        "form": form,
        "order": order
    }
    if request.method == "POST":
        if all([form.is_valid()]):
            order = form.save(commit=False)
            order.save()
            context["message"] = "Data saved!!!"
            return redirect(reverse("show_order", kwargs={"order_id": order_id}))
        else:
            context["error"] = "Internal Server Error!!"
    if order.orderitem_set.all().count() == 0:
        return redirect(reverse('cancel_order', kwargs={"order_id": order_id}))
    return render(request, 'orders/create_update.html', context=context, status=HTTPStatus.OK)

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, customer=request.user)
    order = Order.objects.create(
        customer=request.user
    )
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, item=cart_item.item, quantity=cart_item.quantity)
    cart.cartitem_set.all().delete()
    cart.total = 0.0
    cart.save()
    messages.info(
            request=request,
            message=f"Order created",
            extra_tags=str(order.id),
    )
    return redirect(reverse('show_cart'))


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect(reverse('list_orders'))

@login_required
def update_orderitem(request, order_id, orderitem_id):
    _orderItem = get_object_or_404(OrderItem, order__id=order_id, id=orderitem_id)
    
    form = OrderItemForm(request.POST or None, instance=_orderItem)
    context = {
        "form": form
    }
    if form.is_valid():
        orderItem = form.save(commit=False)
        orderItem.order = _orderItem.order
        orderItem.item = _orderItem.item
        orderItem.save()
        return redirect(reverse('update_order', kwargs={"order_id": order_id}))
    return render(request, 'orders/orderitems/create_update.html', context=context, status=HTTPStatus.OK)

@login_required
def cancel_orderitem(request, order_id, orderitem_id):
    orderItem = get_object_or_404(OrderItem, id=orderitem_id, order_id=order_id)
    orderItem.delete()
    return redirect(reverse('update_order', kwargs={"order_id": order_id}))
