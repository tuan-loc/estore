from django.shortcuts import render, redirect, reverse
from urllib.parse import urlencode
from store import serializers
from store.models import Category, SubCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.forms import *
from cart.cart import Cart
from EStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage
import feedparser

# API
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer

# Rules
import pandas as pd
import os
import re
from django.conf import settings


# Create your views here.
def index(request):
    # Giỏ hàng
    cart = Cart(request)

    # Đọc danh sách sản phẩm
    # Thiết bị gia đình
    subcategory_tbgd = SubCategory.objects.filter(category=1).values_list('id')
    list_subcategoryid_tbgd = []
    for item in subcategory_tbgd:
        list_subcategoryid_tbgd.append(item[0])
    list_product_tbgd = Product.objects.filter(subcategory__in=list_subcategoryid_tbgd).order_by('-public_day')[:20]

    # Đồ dùng nhà bếp
    subcategory_ddnb = SubCategory.objects.filter(category=2).values_list('id')
    list_subcategoryid_ddnb = []
    for item in subcategory_ddnb:
        list_subcategoryid_ddnb.append(item[0])
    list_product_ddnb = Product.objects.filter(subcategory__in=list_subcategoryid_ddnb).order_by('-public_day')[:20]

    return render(request, 'store/index.html', {
        'list_product_ddnb': list_product_ddnb,
        'list_product_tbgd': list_product_tbgd,
        'cart': cart,
    })


def contact(request):
    form = FormContact()
    result = ''
    if request.POST.get('btnSendMessage'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            # Lưu CSDL
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.phone_number = form.cleaned_data['phone_number']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            # Gửi mail
            # Gửi mail không có html
            # send_mail(post.subject, post.message, EMAIL_HOST_USER, [post.email, 'lntri@csc.hcmus.edu.vn'])

            # Gửi mail có lồng html
            content = '<p>Chào bạn <b>' + post.name + '</b>,</p>'
            content += '<p>Chúng tôi đã nhận được thông tin góp từ của bạn thông qua Website EStore với nội dung như sau:</p>'
            content += '<p>' + post.message + '</p>'
            content += '<p>Chúng tôi sẽ liên hệ lại bạn trong thời gian sớm nhất</p>'
            content += '<p>Trân trọng.</p>'

            msg = EmailMessage(post.subject, content, EMAIL_HOST_USER, [post.email, 'lntri@csc.hcmus.edu.vn'])
            msg.content_subtype = 'html'
            msg.send()

            # Thông báo KQ
            result = '''
            <div class="alert alert-success" role="alert">
                Gửi thông tin thành công
            </div>
            '''
        else:
            result = '''
            <div class="alert alert-danger" role="alert">
                Gửi thông tin thất bại.
            </div>'''


    return render(request, 'store/contact.html', {
        'form': form,
        'result': result,
    })


def subcategory(request, pk):
    # Danh sách danh mục
    subcategories = SubCategory.objects.order_by('name')

    # Đọc danh sách sản phẩm theo danh mục (subcategory)
    if pk == 0:
        # Đọc tất cả
        products = Product.objects.order_by('-public_day')

        # Hiển thị tên danh mục (subcategory)
        subcategory_name = 'Tất cả sản phẩm (' + str(products.count()) + ')'
    else:
        # Đọc theo danh mục
        products = Product.objects.filter(subcategory=pk).order_by('-public_day')

        # Hiển thị tên danh mục (subcategory)
        subcategory = SubCategory.objects.get(id=pk)
        subcategory_name = str(subcategory) + ' (' + str(products.count()) + ')'

    # Lọc theo giá
    from_price = ''
    to_price = ''
    product_name = ''
    if request.GET.get('from_price'):
        # Gán biến
        from_price = float(request.GET.get('from_price'))
        to_price = float(request.GET.get('to_price'))
        product_name = request.GET.get('product_name')

        if product_name != '':
            products = Product.objects.filter(name__contains=product_name).order_by('-public_day')

        # Xử lý lọc theo khoảng giá
        products = [product for product in products if from_price <= product.price <= to_price]  # List Comprehension
        subcategory_name = 'Tìm thấy ' + str(len(products)) + ' sản phẩm'

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    
    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        products_pager = paginator.page(1)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)

    return render(request, 'store/product-list.html', {
        'subcategories': subcategories,
        'products': products_pager,
        'product_slide': products_pager[:10],
        'subcategory_name': subcategory_name,
        'from_price': from_price,
        'to_price': to_price,
        'keyword': product_name,
    })


def search(request):
    # Danh sách danh mục
    subcategories = SubCategory.objects.order_by('name')

    products = []
    title = ''
    tu_khoa = ''
    if request.GET.get('product_name'):
        # Gán biến
        tu_khoa = request.GET.get('product_name').strip()
        products = Product.objects.filter(name__contains=tu_khoa).order_by('-public_day')

        # Hiển thị tiêu đề tìm kiếm
        title = 'Tìm thấy ' + str(products.count()) + ' sản phẩm với từ khóa "' + tu_khoa + '"'

    if request.GET.get('from_price'):
        # Gán biến
        from_price = float(request.GET.get('from_price'))
        to_price = float(request.GET.get('to_price'))
        product_name = request.GET.get('product_name')

        base_url = reverse('store:subcategory', kwargs={'pk': 0})
        query_string = urlencode({'from_price': round(from_price), 'to_price': round(to_price),
                                  'product_name': product_name})
        url = '{}?{}'.format(base_url, query_string)

        return redirect(url)

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    
    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        products_pager = paginator.page(1)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)

    return render(request, 'store/product-list.html', {
        'subcategories': subcategories,
        'products': products_pager,
        'subcategory_name': title,
        'product_slide': products_pager,
        'keyword': tu_khoa,
    })


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)

    # Đọc Rules
    rules = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'store/rules.csv'), squeeze=True, index_col=0)
    lst = rules.values.tolist()

    list_rules = []
    for item in lst:
        if str(pk) in re.findall('\d+[, \d+]*', item[0])[0].split(','):
            list_rules = re.findall('\d+[, \d+]*', item[1])[0].split(',')

    list_asc_products = []
    for i in list_rules:
        list_asc_products.append(Product.objects.get(pk=int(i)))

    return render(request, 'store/product-detail.html', {
        'product': product,
        'list_asc_products': list_asc_products,
    })


def read_rss(request):
    newsfeed = feedparser.parse('http://feeds.feedburner.com/bedtimeshortstories/LYCF')
    entry = newsfeed.entries[0]
    print(entry.keys())
    return render(request, 'store/read_rss.html', {
        'newsfeed': newsfeed,
    })


def products_service(request):
    products = Product.objects.order_by('-public_day')
    result = list(products.values())
    return JsonResponse(result, safe=False)


def product_service(request, pk):
    products = Product.objects.filter(pk=pk)
    # result = list(products.values('id', 'name'))[0]
    result = list(products.values())[0]
    return JsonResponse(result, safe=False)


# https://www.django-rest-framework.org/
# https://testdriven.io/blog/built-in-permission-classes-drf/
# https://restfulapi.net/http-status-codes/
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-public_day')
    serializer_class = ProductSerializer
    # permission_class = [permissions.IsAuthenticatedOrReadOnly] # Chỉ đọc
    permission_class = [permissions.IsAdminUser]  # Đọc / Ghi 
    