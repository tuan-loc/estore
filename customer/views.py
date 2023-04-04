from tkinter.messagebox import NO
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from customer import forms
from customer import models
from store.models import Product
from store.my_module import *
from django.contrib.auth.hashers import Argon2PasswordHasher, PBKDF2PasswordHasher
from customer.forms import FormUser, FormUserProfileInfo
from customer.models import Customer
from store.my_module import read_json_internet
from cart.models import Order, OrderItem


# Create your views here.
def users(request):
    form_user = FormUser()
    form_profile = FormUserProfileInfo()
    result_register = ''

    if request.POST.get('btnDangKy'):
        form_user = FormUser(request.POST)
        form_profile = FormUserProfileInfo(request.POST, request.FILES)

        if form_user.is_valid() and form_profile.is_valid():
            if form_user.cleaned_data['password'] == form_user.cleaned_data['confirm_password']:
                # GHI VÀO CSDL
                # User
                user = form_user.save()
                user.set_password(user.password)
                user.save()

                # Profile
                profile = form_profile.save(commit=False)
                profile.user = user
                profile.save()

                result_register = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký thành viên thành công!
                </div>
                '''
            else:
                result_register = '''
                <div class="alert alert-warning" role="alert">
                    Mật khẩu và Xác nhận mật khẩu không khớp!
                </div>
                '''

    if request.POST.get('btnDangNhap'):
        # Gán biến
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('customer:users')
            
    print(request.user)

    return render(request, 'store/user.html', {
        'form_user': form_user,
        'form_profile': form_profile,
        'result_register': result_register,
    })


def logout_user(request):
    logout(request)
    return redirect('customer:users')


def login_customer_2(request):
    session_status = check_session(request, 's_khachhang')
    if session_status:
        return redirect('store:index')

    # Đọc thông tin từ API
    thong_tin = read_json_internet('http://api.laptrinhpython.net/vietnam')
    
    # Biến toàn cục xử lý Tỉnh/TP,...
    data_str_districts = []
    data_str_wards = []
    data_list_districts = []

    # Tỉnh/TP
    provinces = []
    for province in thong_tin:
        provinces.append(province['name'])

        # Quận/Huyện
        districts = []
        for district in province['districts']:
            d = district['prefix'] + ' ' + district['name']
            districts.append(d)
            data_list_districts.append(d)

            # Phường/Xã
            wards = []
            for ward in district['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                wards.append(w)
            else:
                data_str_wards.append('|'.join(wards))
        else:
            data_str_districts.append('|'.join(districts))

    # Đăng ký
    result_register = ''
    form = forms.FormDangKy2()

    if request.POST.get('btnDangKy'):
        form = forms.FormDangKy2(request.POST, models.Customer)
        if form.is_valid():
            if form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
                hasher = Argon2PasswordHasher()  # salt: 8 bytes
                # hasher = PBKDF2PasswordHasher() # salt: 1 byte
                request.POST._mutable = True
                post = form.save(commit=False)
                post.ho = form.cleaned_data['ho']
                post.ten = form.cleaned_data['ten']
                post.email = form.cleaned_data['email']
                post.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], '12345678')
                post.dien_thoai = form.cleaned_data['dien_thoai']
                post.dia_chi = form.cleaned_data['dia_chi'] + ', ' + form.cleaned_data['phuong_xa'] + ', ' + form.cleaned_data['quan_huyen'] + ', ' + form.cleaned_data['tinh_tp']
                post.save()
                result_register = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký thành viên thành công!
                </div>
                '''
            else:
                result_register = '''
                <div class="alert alert-warning" role="alert">
                    Mật khẩu và Xác nhận mật khẩu không khớp!
                </div>
                '''
        else:
            result_register = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký thành viên không thành công. Vui lòng kiểm tra lại thông tin nhập!
                </div>
                '''

    # Đăng nhập: nva@gmail.com / 123456
    result_login = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        # Đọc dữ liệu
        khach_hang = models.Customer.objects.filter(email=email, mat_khau=encoded)

        if khach_hang.count() > 0:
            request.session['s_khachhang'] = khach_hang.values()[0]
            return redirect('store:index')
        else:
            result_login = '''
            <div class="alert alert-danger" role="alert">
                Đăng nhập thất bại
            </div>
            '''

    return render(request, 'store/login-2.html', {
        'form': form,
        'result_register': result_register,
        'result_login': result_login,
        'provinces': tuple(provinces),
        'data_str_districts': tuple(data_str_districts),
        'data_str_wards': tuple(data_str_wards),
        'data_list_districts': data_list_districts,
    })




def login_customer(request):
    session_status = check_session(request, 's_khachhang')
    if session_status:
        return redirect('store:index')

    # Đăng ký
    result_register = ''
    form = forms.FormDangKy()
    if request.POST.get('btnDangKy'):
        form = forms.FormDangKy(request.POST, models.Customer)
        if form.is_valid():
            if form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
                hasher = Argon2PasswordHasher()  # salt: 8 bytes
                # hasher = PBKDF2PasswordHasher() # salt: 1 byte
                request.POST._mutable = True
                post = form.save(commit=False)
                post.ho = form.cleaned_data['ho']
                post.ten = form.cleaned_data['ten']
                post.email = form.cleaned_data['email']
                post.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], '12345678')
                post.dien_thoai = form.cleaned_data['dien_thoai']
                post.dia_chi = form.cleaned_data['dia_chi']
                post.save()
                result_register = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký thành viên thành công!
                </div>
                '''
            else:
                result_register = '''
                <div class="alert alert-warning" role="alert">
                    Mật khẩu và Xác nhận mật khẩu không khớp!
                </div>
                '''
        else:
            result_register = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký thành viên không thành công. Vui lòng kiểm tra lại thông tin nhập!
                </div>
                '''

    # Đăng nhập: nva@gmail.com / 123456
    result_login = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        # Đọc dữ liệu
        khach_hang = models.Customer.objects.filter(email=email, mat_khau=encoded)

        if khach_hang.count() > 0:
            request.session['s_khachhang'] = khach_hang.values()[0]
            return redirect('store:index')
        else:
            result_login = '''
            <div class="alert alert-danger" role="alert">
                Đăng nhập thất bại
            </div>
            '''

    return render(request, 'store/login.html', {
        'form': form,
        'result_register': result_register,
        'result_login': result_login,
    })


def logout_customer(request):
    if request.session.get('s_khachhang'):
        del request.session['s_khachhang']
    return redirect('customer:login')


def my_account(request):
    # Kiểm tra trạng thái đăng nhập trước khi cho truy cập vào trang my-account
    session_khach_hang = request.session.get('s_khachhang')
    if session_khach_hang is None:
        return redirect('customer:login')

    # Biến dùng chung (toàn cục)
    result_update = ''
    result_change_pwd = ''
    
    # Cập nhật thông tin Tài khoản của tôi
    if request.POST.get('btnCapNhat'):
        # Gán biến
        ho = request.POST.get('ho').strip()
        ten = request.POST.get('ten').strip()
        dien_thoai = request.POST.get('dien_thoai').strip()
        dia_chi = request.POST.get('dia_chi').strip()

        # Cập nhật vào CSDL
        khach_hang = Customer.objects.get(id=session_khach_hang['id'])
        khach_hang.ho = ho
        khach_hang.ten = ten
        khach_hang.dien_thoai = dien_thoai
        khach_hang.dia_chi = dia_chi
        khach_hang.save()

        # Cập nhật vào session
        session_khach_hang['ho'] = ho
        session_khach_hang['ten'] = ten
        session_khach_hang['dien_thoai'] = dien_thoai
        session_khach_hang['dia_chi'] = dia_chi
        request.session['s_khachhang'] = session_khach_hang
    
        # Thông báo kết quả
        result_update = '''
        <div class="alert alert-success" role="alert">
            Cập nhật thông tin thành công!
        </div>
        '''

    # Đổi mật khẩu
    if request.POST.get('btnDoiMatKhau'):
        # Gán biến
        mat_khau_hien_tai = request.POST.get('mat_khau_hien_tai').strip()
        mat_khau_moi = request.POST.get('mat_khau_moi').strip()
        xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau').strip()
        khach_hang = Customer.objects.get(id=session_khach_hang['id'])

        # So sánh mật khẩu hiện tại có đúng hay không?
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau_hien_tai, '12345678')
        if encoded == khach_hang.mat_khau:
            if mat_khau_moi == xac_nhan_mat_khau:
                khach_hang.mat_khau = hasher.encode(mat_khau_moi, '12345678')
                khach_hang.save()
                result_change_pwd = '''
                    <div class="alert alert-success" role="alert">
                        Cập nhật thông tin thành công!
                    </div>
                    '''
            else:
                result_change_pwd = '''
                    <div class="alert alert-danger" role="alert">
                        Mật khẩu mới và Xác nhận mật khẩu không khớp.
                    </div>
                    '''
        else:
            result_change_pwd = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu hiện tại không đúng. Vui lòng kiểm tra lại.
                </div>
                '''

    # Lịch sử mua hàng
    list_orders = Order.objects.filter(username=session_khach_hang['email']).order_by('-created')
    dict_orders = {}
    for order in list_orders:
        list_order_items = list(OrderItem.objects.filter(order_id=order.pk).values())
        for order_item in list_order_items:
            product = Product.objects.get(pk=order_item['product_id'])
            order_item['product_name'] = product.name
            order_item['product_image'] = product.image
            order_item['total_price'] = order.total
        dict_order_items = { order.pk: list_order_items }
        dict_orders.update(dict_order_items)
    print(dict_orders)

    return render(request, 'store/my-account.html', {
        'result_update': result_update,
        'result_change_pwd': result_change_pwd,
        'list_orders': list_orders,
        'dict_orders': dict_orders,
    })