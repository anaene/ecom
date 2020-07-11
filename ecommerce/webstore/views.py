from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

# Create your views here.
# home, account,
from webstore.forms import CustomerForm, QuantityForm
from webstore.models import Product, Order, OrderProduct


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


def add_to_cart(request, product_id):
    quantity_form = QuantityForm(request.POST)
    quantity = quantity_form['quantity'].value()
    product = get_object_or_404(Product, pk=product_id)
    order = get_order(request)
    update_order(order, product, quantity)
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


def update_order(order, product, quantity):
    try:
        order_product = get_object_or_404(OrderProduct, order=order, product=product)
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
