from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm






class UserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = User
		fields = ('username',)


class UserChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('email', 'username')