from django.http.response import HttpResponse
from django.shortcuts import render
from store.models import Product
from django.db.models import Count
from datetime import datetime
from django.template.loader import render_to_string
import pdfkit
import os


# Create your views here.
def html_to_pdf_view(request):
    products = Product.objects.values('subcategory', 'subcategory__name').annotate(total=Count('subcategory')).order_by('subcategory')
    current_day = datetime.now().strftime('%d-%m-%Y')

    # Xử lý cho chart
    # Cách 1
    # ds_ten_subcategory = []
    # for product in products:
    #     ds_ten_subcategory.append(product['subcategory__name'])

    # cách 2: https://www.geeksforgeeks.org/comprehensions-in-python/
    ds_ten_subcategory = [product['subcategory__name'] for product in products]

    ds_so_luong_san_pham_subcategory = [product['total'] * 10 for product in products]

    html_string = render_to_string('storereport/easyreport.html', {
        'products': products,
        'current_day': current_day,
        'ds_ten_subcategory': ds_ten_subcategory,
        'ds_so_luong_san_pham_subcategory': ds_so_luong_san_pham_subcategory,
    })

    return HttpResponse(html_string)

    # Download report (PDF)
    # config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    # file_name = 'report_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
    # pdfkit.from_string(html_string, os.path.join(
    #     os.path.expanduser('~'), 'Documents', file_name), configuration=config)

    # html = '<div class="text-center">' + html_string + \
    #        '<h5>Thống kê đã được lưu vào tập tin ' + file_name + \
    #        ' trong thư mục Documents.</h5></div>'
    # return HttpResponse(html)
