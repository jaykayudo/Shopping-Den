from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, password_validation
from .models import User, Product
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email_phone = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput, strip =False)
    def __init__(self,request = None,*args,**kwargs):
        self.request = request
        self.user = None
        super().__init__(*args,**kwargs)
    def clean(self):
        email = self.cleaned_data.get('email_phone')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user = authenticate(self.request,email=email,password=password)
            if self.user is None:
                self.user = authenticate(self.request,phone_number=email,password=password)
        if self.user is None:
            raise forms.ValidationError('Incorrect email/password')
        return self.cleaned_data
    def get_user(self):
        return self.user

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email","phone_number"]

        # def clean_phone_number(self):
        #     phone_start_number = ['081','080','090','091','070']
        #     phone_number = self.cleaned_data.get('phone_number')
        #     if phone_number[:2] not in phone_start_number:
        #         self.add_error(self.phone_number,'Enter a valid nigerian number')
        #     return phone_number
class ProductCreateForm(forms.ModelForm):
    category = forms.CharField()
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple':'muliptle'}))
    class Meta:
        model = Product
        fields = ["name","description","price","phone_number","location","negotiable"]
    def __init__(self,request = None,*args,**kwargs):
        self.request = request
        super().__init__(*args,**kwargs)
    def clean(self):
        count = Product.objects.filter(user = self.request.user).count()
        if count >= 10:
            raise ValidationError('You can only have at most 10 posts. Delete posts to inorder to add these one.')
        return self.cleaned_data

    def clean_category(self):
        category = self.cleaned_data.get('category')
        category_list = set(category.split(','))
        if len(category_list) > 5:
            self.add_error(self.category,_("Select at most 5 categories"))
        return category


