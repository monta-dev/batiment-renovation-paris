from django.urls import path
from . import views
from .views import signup_view, login_view


urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='register'),
]
