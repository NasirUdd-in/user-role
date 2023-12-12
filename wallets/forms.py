from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile
from django.contrib.auth.models import Group, Permission

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'wallet_balance']
        exclude = ['user']

class CustomUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        # widget=forms.SelectMultiple,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label='Select Role',
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'groups']  


from django import forms
from django.contrib.auth.models import Group, Permission

class GroupPermissionForm(forms.Form):
    group_name = forms.CharField(label='Role', max_length=50)
    permissions = forms.ModelMultipleChoiceField(
        # queryset=Permission.objects.all(),
        queryset=Permission.objects.filter(content_type__app_label='wallets'),
        widget=forms.CheckboxSelectMultiple,
        label='Role Permissions'
    )

    def save(self):
        group = Group.objects.create(name=self.cleaned_data['group_name'])
        group.permissions.set(self.cleaned_data['permissions'])
        return group
