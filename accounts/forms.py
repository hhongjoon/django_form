from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserCustomChangeForm(UserChangeForm):
    class Meta: # 정보가 들어가야함
        model = User
        fields = ['username','email','first_name','last_name']