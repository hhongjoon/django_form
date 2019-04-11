from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','password1','password2',]

class UserCustomChangeForm(UserChangeForm):
    class Meta: # 정보가 들어가야함
        model = get_user_model()
        fields = ['email','first_name','last_name']