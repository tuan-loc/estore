from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST
from cart.models import Order, OrderItem


# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    list_coupon_code = ['LNTRI', 'TTTH', 'CSC']

    # Mã giảm giá
    coupon_code = ''
    if request.POST.get('btnMaGiamGia'):
        coupon_code = request.POST.get('coupon').strip()
        if coupon_code in list_coupon_code:
            cart_new = {}
            for c in cart:
                product_cart = {
                    str(c['product'].id): {
                        'quantity': c['quantity'], 
                        'price': str(c['product'].price), 
                        'coupon': '0.9'
                    }
                }
                cart_new.update(product_cart)
                c['coupon'] = 0.9
            request.session['cart'] = cart_new
        else:
            cart_new = {}
            for c in cart:
                product_cart = {
                    str(c['product'].id): {
                        'quantity': c['quantity'], 
                        'price': str(c['product'].price), 
                        'coupon': '1'
                    }
                }
                cart_new.update(product_cart)
                c['coupon'] = 1
            request.session['cart'] = cart_new

    # Cập nhập số lượng sản phẩm trên giỏ hàng
    if request.POST.get('btnCapNhatGioHang'):
        cart_new = {}
        for c in cart:
            quantity_new = int(request.POST.get('quantity1' + str(c['product'].id)))
            if quantity_new != 0:
                product_cart = {
                    str(c['product'].id): {
                        'quantity': quantity_new, 
                        'price': str(c['product'].price), 
                        'coupon': str(c['coupon'])
                    }
                }
                cart_new.update(product_cart)
            else:
                cart.remove(c['product'])
            c['quantity'] = quantity_new

        request.session['cart'] = cart_new

    # print(request.session.get('cart'))
    return render(request, 'store/cart.html', {
        'cart': cart,
        'coupon_code': coupon_code,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product=product, quantity=int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def remove_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def checkout(request):
    # Kiểm tra trạng thái đăng nhập trước khi cho truy cập vào trang checkout
    session_khach_hang = request.session.get('s_khachhang')
    if session_khach_hang is None:
        return redirect('cart:cart_detail')

    cart = Cart(request)

    # Xử lý đặt hàng
    if request.POST.get('btnDatHang'):
        order = Order()
        order.username = session_khach_hang['email']
        order.first_name = session_khach_hang['ten']
        order.last_name = session_khach_hang['ho']
        order.phone = session_khach_hang['dien_thoai']
        order.address = session_khach_hang['dia_chi']
        order.total = cart.get_final_total_price()
        order.save()

        for c in cart:
            OrderItem.objects.create(order=order, product=c['product'], price=c['price'], quantity=c['quantity'])

        # Gửi mail

        # Xóa giỏ hàng sau khi đặt hàng thành công
        cart.clear()

        return render(request, 'store/result.html')

    return render(request, 'store/checkout.html', {
        'cart': cart,
    })