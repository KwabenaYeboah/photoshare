from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError("The two passwords mismatch")
            return cd['password2']

class UserUpdateForm(forms.ModelForm):
        class Meta:
            model = get_user_model()
            fields = ('email', 'first_name', 'last_name')
            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dob', 'image')
        
        
    

