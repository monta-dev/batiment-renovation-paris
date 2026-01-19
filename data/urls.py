from django.urls import path, re_path
from django.urls import register_converter
from . import views


urlpatterns = [
    path("energy-classes/", views.get_energy_classes),
    path("Renovation-types/", views.get_Renovation_types),
    path("Batiment_renovates/", views.get_Batiment_renovates),
]
