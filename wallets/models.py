from django.contrib.auth.models import User
from django.db import models
from django import forms

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed
    bio = models.TextField(blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return self.user.username
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'wallet_balance','user']