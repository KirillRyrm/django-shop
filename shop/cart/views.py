from django.shortcuts import render, redirect, \
    get_object_or_404
from django.views.decorators.http import require_POST

from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, **cd)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['updated_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override_quantity': True
        })
    return render(request, 'cart/cart_detail.html', context={'cart': cart})

