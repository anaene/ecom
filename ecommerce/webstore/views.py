from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
# home, account,
from webstore.forms import CustomerForm
from webstore.models import Product


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
    return render(request, 'webstore/products/product.html', {'product': product})
