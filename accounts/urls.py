from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login_view, dashboard_view

urlpatterns = [
   # path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
