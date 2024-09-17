from django.forms import ModelForm

from order.models import Order, OrderItem

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["customer"].disabled = True
        self.fields["status"].disabled = True
        self.fields["total"].disabled = True
        
class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields["order"].disabled = True
        self.fields["item"].disabled = True