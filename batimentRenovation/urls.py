from django.contrib import admin
from django.urls import path, include
from . import views  # ← Importer les vues


urlpatterns = [
    path('', views.index, name='home'),  # ← Ta page d'accueil
    #path('auth/', views.auth, name='login'),  
    path('graph/', views.accueil, name='dashboard'), 
   #path('aquipe/', views.contact, name='contact'),
    path('admin1/', views.admin1, name='admin_page'),
    path('about/', views.about, name='about'),
    path('404/', views.erreur, name='404'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Ajouter cette ligne
    
]



    

