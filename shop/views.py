from django.shortcuts import render,get_object_or_404
from django.http import  HttpResponse
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
# Create your views here.
from .models import Category, Product

# def about_shop(request):
#     return HttpResponse("Page about ComputerShop")

def about_shop(request):
    return render(request,"shop/about.html")

def contacts(request):
    return HttpResponse("Contacts ComputerShop")

def product_list(request, category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    if category_slug:
        # category=Category.objects.filter(slug=category_slug)
        category=get_object_or_404(Category,slug=category_slug)
        products=products.filter(category=category)
    paginator=Paginator(products, 6)
    if 'page' in request.GET:
        page_num=request.GET['page']
    else:
        page_num=1

    page=paginator.get_page(page_num)
    return render(request, 'shop/product/list.html',{
        'category':category,
        'categories':categories,
        'products':page.object_list,
        'page':page
    })

def product_detail(request,id):
    product = get_object_or_404(Product, id=id)
    cart_product_form=CartAddProductForm()
    return render(request,'shop/product/detail.html',{
        'product':product,
        'cart_product_form':cart_product_form
    })