from django.contrib import admin
from store.models import *
from datetime import date
from django.utils.html import format_html
from store.forms import FormProduct


def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=date.today())

change_public_day.short_description = 'Thay đổi thời gian cho các sản phẩm chọn'


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    form = FormProduct

    # Tắt field trong insert/update
    exclude = ('viewed',)

    # Hiển thị nhiều field cho model trên trang liệt kê danh sách
    # list_display = ('name', 'price', 'public_day', 'viewed', 'subcategory')
    list_display = ('e_name', 'e_price', 'e_public_day', 'e_viewed', 'e_subcategory', 'e_image')

    # Lọc theo public_day
    list_filter = ('public_day',)

    # Tìm kiếm theo cột chỉ định
    search_fields = ('name', 'content')

    # Action
    actions = [change_public_day]

    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    @admin.display(description='Tên sản phẩm')
    def e_name(self, obj):
        return '%s' % obj.name

    @admin.display(description='Giá')
    def e_price(self, obj):
        return '%s' % obj.price

    @admin.display(description='Ngày xuất bản')
    def e_public_day(self, obj):
        return '%s' % obj.public_day
    
    @admin.display(description='Số lượt xem')
    def e_viewed(self, obj):
        return '%s' % obj.viewed

    @admin.display(description='Danh mục')
    def e_subcategory(self, obj):
        return '%s' % obj.subcategory

    @admin.display(description='Hình ảnh')
    def e_image(self, obj):
        return format_html('<img src="{}" width="45">'.format(obj.image.url))


admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)

# Thay đổi tiêu đề
admin.site.site_header = 'EStore Admin'

