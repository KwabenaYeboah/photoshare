from typing import Container
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from decorators.decorators import ajax_required
from .forms import LoginForm, UserSignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Follow

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
    # if user is already signed in, return user to dashboard page
    if request.user.is_authenticated:
        return redirect('dashboard')
        
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
            return redirect('dashboard') # return user to dashboard after profile update.
        else:
            messages.error(request, 'Error updating profile')
    
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/user_profile_update.html', 
                  {'user_form': user_form, 'profile_form':profile_form})


@login_required
def user_list_view(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'accounts/user_list.html', {'users':users, 'section':'people'})

@login_required
def user_detail_view(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'accounts/user_detail.html', {'user':user, 'section': 'people'})
           
@ajax_required
@require_POST
@login_required
def follow_user_view(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Follow.objects.get_or_create(this_user=request.user, that_user=user)
            else:
                Follow.objects.filter(this_user=request.user, that_user=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})