
from . import views
from django.contrib.auth.views import LoginView

from django.urls import path

urlpatterns = [path('home_page', views.home, name='home'),
               path('login', views.login_view, name='login'),
               path('register', views.sign_up, name='register')
               ]