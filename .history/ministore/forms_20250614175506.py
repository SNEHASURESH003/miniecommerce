from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'