from django import forms
from store.models import Contact, Product
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))", "Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!")


class FormContact(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={
        'placeholder': 'Họ tên',
        'class': 'form-control'
    }))
    phone_number = forms.CharField(max_length=20, label='Phone', validators=[phone_validator],
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Điện thoại',
                                       'class': 'form-control fh5co_contact_text_box',
                                       'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
                                       'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'
                                   }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={
        'placeholder': 'Tiêu đề',
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Nội dung',
        'class': 'form-control',
        'rows': '5'
    }))

    class Meta:
        model = Contact
        fields = '__all__'


class FormProduct(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ('name', 'price')
        exclude = ('viewed',)
        
        labels = {
            'name': 'Tên sản phẩm',
            'price': 'Giá',
        }