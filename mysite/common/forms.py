from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# UserForm은 forms 패키지의 UserCreationForm를 상속하고
# email 속성을 추가 했다. 기본적으로 UserCreateForm은 Username, password1, password2 등이 있는데
# Email 속성을 추가 하기 위해 상속한 UserForm을 만든것.
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")