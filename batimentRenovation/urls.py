from django.contrib import admin
from django.urls import path, include
from . import views  # ← Importer les vues


urlpatterns = [
    path('', views.index, name='home'),  # ← Ta page d'accueil
    #path('auth/', views.auth, name='login'),  
    path('Accueil/', views.Accueil, name='dashboard'), 
    path('dashboard_bat/', views.dash_bat, name='dashboard_batiment'), 
    path('dashboard_dpe/', views.dash_dpe, name='dashboard_dpe'),
    path('dashboard_types/', views.dash_types, name='dashboard_types'),  
   #path('aquipe/', views.contact, name='contact'),
    path('admin1/', views.admin1, name='admin_page'),
    path('about/', views.about, name='about'),
    path('404/', views.erreur, name='404'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Ajouter cette ligne
    
]



    

