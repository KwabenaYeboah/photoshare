from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserSignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Login Successful')
                return HttpResponse('Your account is disabled') #return this if user is inactive
            return HttpResponse('Invalid login details') # return this for wrong login details
    form = LoginForm()
    return render(request, 'login.html', {'form':form})  
    
@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'section':'dashboard'})

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Create User object without saving it yet
            user.set_password(form.cleaned_data['password']) 
            user.save()
            Profile.objects.create(user=user)
            return render(request, 'accounts/signup_complete.html', {'user':user})
    
    form = UserSignUpForm()
    return render(request, 'accounts/signup.html', {'form':form})

@login_required
def user_profile_update_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileUpdateForm(instance=request.user.profile,
                                         data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Successfully updated')
        else:
            messages.error(request, 'Error updating profile')
    
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/user_profile_update.html', 
                  {'user_form': user_form, 'profile_form':profile_form})
            
            


    