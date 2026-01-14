from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    #path('register/', register, name='register'),
    path('login/', views.login, name='login'),
    #path('logout/', logout_view, name='logout'),
]