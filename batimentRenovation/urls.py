from django.contrib import admin
from django.urls import path, include
from . import views  # ← Importer les vues

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),  # ← Ta page d'accueil
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/batiment/", views.dashboard_batiment, name="dashboard-batiment"),
    path("dashboard/dpe/", views.dashboard_dpe, name="dashboard-dpe"),
    path("dashboard/types/", views.dashboard_types, name="dashboard-types"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("admin_page/", views.admin_page, name="admin-page"),
    path("api/", include("data.urls")),
]
