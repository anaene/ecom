from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

# Create your views here.
# home, account,
from webstore.forms import CustomerForm, QuantityForm, AddressForm
from webstore.models import Product, Order, OrderProduct, Customer


def index(request):
    products_list = Product.sort_by_name()
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 12)
    limited_items = Product.limited_items(4)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'webstore/index.html', {'products': products, 'limited_products': limited_items})


def account(request):
    return render(request, 'webstore/account.html')


def register(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user_form.save()

            return redirect('login')
    else:
        customer_form = CustomerForm()
        user_form = UserCreationForm()

    context = {'user': user_form, 'customer': customer_form}
    return render(request, 'webstore/registration/register.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity_form = QuantityForm()

    context = {'product': product, 'quantity_form': quantity_form}
    return render(request, 'webstore/products/product.html', context)


# add to cart functions
def add_to_cart(request, product_id):
    quantity_form = QuantityForm(request.POST)
    quantity = quantity_form['quantity'].value()
    product = get_object_or_404(Product, pk=product_id)
    order = get_order(request)
    add_to_order(order, product, quantity)
    request.session['cart_total'] = update_cart_total(order).__str__()
    return redirect(index)


def get_order(request):
    # check cart total exists for session else create new order assign order number and total to session variables
    if 'cart_order' in request.session:
        order = get_object_or_404(Order, pk=request.session['cart_order'])
    else:
        order = Order()
        order.save()
        request.session['cart_order'] = order.id

    return order


def add_to_order(order, product, quantity):
    try:
        order_product = get_object_or_404(OrderProduct, order=order, product=product)
        if order_product.quantity < 5 and order_product.quantity + quantity <= 5:
            order_product.quantity += int(quantity)

    except Http404:
        order_product = OrderProduct(order=order, product=product, quantity=int(quantity))

    order_product.save()


def update_cart_total(order):
    products = get_list_or_404(OrderProduct, order=order)
    cart_total = 0
    for product in products:
        cart_total += product.quantity

    return cart_total


# checkout functions
def checkout(request):
    if 'cart_order' not in request:
        get_order(request)
    try:
        pk = request.session['cart_order']
        order = get_object_or_404(Order, pk=pk)
        order_products = get_list_or_404(OrderProduct, order=order)
        context = {'order_products': order_products, 'range': range(1, 6), 'order': order}

    except Http404:
        context = {'no_items': 'No Items in Cart'}
    return render(request, 'webstore/checkout/checkout.html', context)


def update_order_product(request):
    order_product = get_object_or_404(OrderProduct, pk=request.GET.get('orderProductId'))
    order_product.quantity = request.GET.get('quantity')
    order_product.save()
    order_product.refresh_from_db()
    data = {'subtotal': order_product.subtotal, 'total': order_product.order.get_total()}
    return JsonResponse(data)


def remove_cart_product(request, product_id):
    order_product = get_object_or_404(OrderProduct, pk=product_id)
    order_product.delete()
    return redirect(checkout)


@login_required(redirect_field_name='next')
def process_checkout(request):
    try:
        order = get_object_or_404(Order, pk=request.session['cart_order'])
        customer = get_object_or_404(Customer, user=request.user)
        order.customer = customer
        order.save()
        order.refresh_from_db()
        order_products = get_list_or_404(OrderProduct, order=order)
        address_form = AddressForm()
        context = {'order': order, 'address_form': address_form, 'order_products': order_products, 'range': range(1, 6)}
    except Http404:
        context = {}

    return render(request, 'webstore/checkout/confirmation.html', context)


def get_customer_address(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        street = customer.primary_address.street
        city = customer.primary_address.city
        postcode = customer.primary_address.postcode
        data = {'street': street, 'postcode': postcode, 'city': city}
    else:
        data = {}

    return JsonResponse(data)
