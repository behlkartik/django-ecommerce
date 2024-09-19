from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages

from order.models import Order, OrderStatus
from .utils import cashfree_client
# Create your views here.

def make_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_response, status = cashfree_client.get_order(order_id)
    if not order_response:
        order_response, status = cashfree_client.create_order(order, f"http://localhost:8000/payment/{order_id}/status")
    payment_session_id = order_response["payment_session_id"]
    return_url = order_response["order_meta"]["return_url"]
    return render(request, 'payment/payment.html', context={"payment_session_id": payment_session_id, "order": order, "customer": request.user, "return_url": return_url})

def retry_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    get_order_response, status = cashfree_client.get_order(order_id)
    payment_session_id = get_order_response["payment_session_id"]
    return_url = get_order_response["order_meta"]["return_url"]
    return render(request, 'payment/payment.html', context={"payment_session_id": payment_session_id, "order": order, "customer": request.user, "return_url": return_url})

def cancel_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    cancelled_order_details, status = cashfree_client.cancel_order(order.id)
    print(cancelled_order_details, status)
    if 200 <= status <= 209:
        messages.success(
            request=request,
            message=f"Order #{order_id} was cancelled"
        )
        return redirect(reverse('cancel_order', kwargs={"order_id": order_id}))
    raise Http404

def payment_status(request, order_id):
    order_payment_response, status = cashfree_client.get_payment_for_order(order_id)
    print(order_payment_response)
    order_status = order_payment_response[0]["payment_status"]
    order = Order.objects.get(id=int(order_id))
    
    if order_status == "SUCCESS":
        order.status = OrderStatus.PAID.value
    elif order_status == "CANCELLED":
        order.status = OrderStatus.CANCELLED.value
    elif order_status == "FAILED":
        order.status = OrderStatus.PAYMENT_FAILED.value
    elif order_status in ["PENDING", "USER_DROPPED"]:
        order.status = OrderStatus.PENDING.value
    else:
        raise Http404()
    order.save()
    return redirect(reverse('list_orders'))
    

# def cancel_payment(request, order_id):
#     order = get_object_or_404(Order, id=order_id, customer=request.user)
#     cancelled_order_details, status = cancel_order(order.id)
#     print(cancelled_order_details, status)
#     if 200 <= status <= 209:
#         return redirect(reverse('cancel_order', kwargs={"order_id": order_id}))
#     return Http404