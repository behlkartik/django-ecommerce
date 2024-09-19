from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
import requests
import json
import os
from base64 import b64decode

# def create_order(order_id, amount):
#     customerDetails = CustomerDetails(customer_id="kartikbehl", customer_phone="9999999999")
#     orderMeta = OrderMeta(return_url="https://127.0.0.1/orders?order_id={order_id}", payment_methods="cc,dc,nb,upi")
#     createOrderRequest = CreateOrderRequest(order_id=f"order_{order_id}", order_amount=amount, order_currency="INR", customer_details=customerDetails, order_meta=orderMeta)
#     try:
#         api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
#         payment_session_id = api_response.data.payment_session_id
#         print(payment_session_id)
#         return payment_session_id
#     except Exception as e:
#         print(e)

class CashFreeClient:
    def __init__(self):
        self.base_url = 'https://sandbox.cashfree.com/pg'
        self.client_id = b64decode(eval(os.getenv("CASHFREE_CLIENT_ID"))).decode('utf-8')
        self.client_secret = b64decode(eval(os.getenv("CASHFREE_CLIENT_SECRET"))).decode('utf-8')
        self.api_version = "2023-08-01"
        self.default_headers = {
            "x-client-id": self.client_id,
            "x-client-secret": self.client_secret,
            "x-api-version": self.api_version,
            "accept": "application/json",
            "content-type": "application/json"
        }
    def create_order(self, order, return_url):
        url = f"{self.base_url}/orders"
        payload = {
            "order_id": f"order_{order.id}",
            "order_amount": float(order.total),
            "order_currency": "INR",
            "customer_details": {
                "customer_id": f"customer_{order.customer.id}",
                "customer_name": order.customer.username,
                "customer_phone": "9999999999" ,
            },
            "order_meta":{
                "return_url": return_url    
            }
            
        }
        response = requests.post(
            url=url,
            headers=self.default_headers,
            json=payload,
        )
        response.raise_for_status()
        print(response.json())
        return response.json(), response.status_code

    def get_order(self, order_id):
        response = requests.get(
            url=f"{self.base_url}/orders/order_{order_id}",
            headers=self.default_headers
        )
        # terminateOrder = TerminateOrderRequest(order_id=f"order_{order_id}", order_status="TERMINATED")
        # response.raise_for_status()
        if response.status_code == 404:
            return None, 404
        getOrderResponse, status = response.json(), response.status_code
        return getOrderResponse, status

    def get_payment_for_order(self, order_id):
        response = requests.get(
            url=f"{self.base_url}/orders/order_{order_id}/payments",
            headers=self.default_headers
        )
        # terminateOrder = TerminateOrderRequest(order_id=f"order_{order_id}", order_status="TERMINATED")
        response.raise_for_status()
        getOrderPaymentResponse, status = response.json(), response.status_code
        return getOrderPaymentResponse, status

    def cancel_order(self, order_id):
        response = requests.patch(
            url=f"{self.base_url}/orders/order_{order_id}",
            headers=self.default_headers,
            data=json.dumps({
                "order_status": "TERMINATED"
            })
        )
        # terminateOrder = TerminateOrderRequest(order_id=f"order_{order_id}", order_status="TERMINATED")
        response.raise_for_status()
        cancelOrderResponse, status = response.json(), response.status_code
        print("cancelOrderResponse", cancelOrderResponse)
        return cancelOrderResponse, status

cashfree_client = CashFreeClient()