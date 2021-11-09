from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

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
    return render(request, 'dashboard.html', {'section':'dashboard'})
    