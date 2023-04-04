from django import forms
from customer import models
from django.contrib.auth.models import User
from customer.models import UserProfileInfo


class FormDangKy(forms.ModelForm):
    ho = forms.CharField(max_length=250, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Họ"
    }))
    ten = forms.CharField(max_length=250, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Tên"
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    mat_khau = forms.CharField(max_length=100, label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Mật khẩu"
    }))
    xac_nhan_mat_khau = forms.CharField(max_length=100, label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Xác nhận Mật khẩu"
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Điện thoại"
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Địa chỉ",
        "rows": 4,
    }))

    class Meta:
        model = models.Customer
        # fields = '__all__'
        fields = ['ho', 'ten', 'email', 'mat_khau', 'dien_thoai', 'dia_chi']

    
class FormDangKy2(forms.ModelForm):
    ho = forms.CharField(max_length=250, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Họ"
    }))
    ten = forms.CharField(max_length=250, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Tên"
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    mat_khau = forms.CharField(max_length=100, label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Mật khẩu"
    }))
    xac_nhan_mat_khau = forms.CharField(max_length=100, label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Xác nhận Mật khẩu"
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Điện thoại"
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Địa chỉ",
        "rows": 4,
    }))
    tinh_tp = forms.CharField(label='Tỉnh/TP', widget=forms.Select(attrs={
        "class": "form-control",
    }))
    quan_huyen = forms.CharField(label='Quận/Huyện', widget=forms.Select(attrs={
        "class": "form-control",
    }))
    phuong_xa = forms.CharField(label='Phường/Xã', widget=forms.Select(attrs={
        "class": "form-control",
    }))

    class Meta:
        model = models.Customer
        # fields = '__all__'
        fields = ['ho', 'ten', 'email', 'mat_khau', 'dien_thoai', 'dia_chi']


class FormUser(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    confirm_password = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password"
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FormUserProfileInfo(forms.ModelForm):
    portfolio = forms.URLField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Portfolio"
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control-file",
    }))

    class Meta:
        model = UserProfileInfo
        exclude = ('user',)
