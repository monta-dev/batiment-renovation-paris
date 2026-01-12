from django.contrib import admin
from django.urls import path
from . import views  # ← Importer les vues

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),  # ← Ta page d'accueil
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('admin_page/', views.admin_page, name='admin-page'),
]