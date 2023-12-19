from django import forms

from orders.enums import OrderStatus
from orders.models import Order


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=OrderStatus.get_choices()),
        }
