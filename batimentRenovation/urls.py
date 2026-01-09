from django.contrib import admin
from django.urls import path
from . import views  # ← Importer les vues

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='home'),  # ← Ta page d'accueil
    path('auth/', views.auth, name='login'),  
    path('graph/', views.accueil, name='dashboard'), 
    path('aquipe/', views.contact, name='contact'),
    path('admin/', views.admin, name='admin_page'),
    path('about/', views.about, name='about'),
    path('404/', views.erreur, name='404'),
   # path('admin/', admin.site.urls)
]
