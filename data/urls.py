"""
URLs de l'application renovation.

Endpoints principaux (format JSON direct pour le frontend):
    /api/renovation/stats-batiments/  → Statistiques par arrondissement
    /api/renovation/stats-dpe/        → Répartition par classe DPE
    /api/renovation/stats-types/      → Types de travaux

Endpoints utilitaires:
    /api/renovation/dashboard/        → Toutes les données en un appel
    /api/renovation/summary/          → Résumé statistique
    /api/renovation/filtres/          → Filtres disponibles
"""

from django.urls import path
from data.views import (
    StatsBatimentsView,
    StatsDPEView,
    StatsTypesView,
    DashboardView,
    StatsSummaryView,
    FiltresView,
)

app_name = "renovation"

urlpatterns = [
    # ==========================================================================
    # Endpoints principaux (données pour graphiques)
    # ==========================================================================
    
    # Statistiques par arrondissement
    # GET /api/renovation/stats-batiments/
    # GET /api/renovation/stats-batiments/?annee_debut=2020&annee_fin=2024
    path(
        "stats-batiments/",
        StatsBatimentsView.as_view(),
        name="stats-batiments"
    ),
    
    # Répartition par classe DPE
    # GET /api/renovation/stats-dpe/
    path(
        "stats-dpe/",
        StatsDPEView.as_view(),
        name="stats-dpe"
    ),
    
    # Types de travaux
    # GET /api/renovation/stats-types/
    # GET /api/renovation/stats-types/?annee_debut=2020&annee_fin=2024
    path(
        "stats-types/",
        StatsTypesView.as_view(),
        name="stats-types"
    ),
    
    # ==========================================================================
    # Endpoints utilitaires
    # ==========================================================================
    
    # Dashboard complet (toutes les données en un appel)
    # GET /api/renovation/dashboard/
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard"
    ),
    
    # Résumé statistique
    # GET /api/renovation/summary/
    path(
        "summary/",
        StatsSummaryView.as_view(),
        name="summary"
    ),
    
    # Filtres disponibles
    # GET /api/renovation/filtres/
    path(
        "filtres/",
        FiltresView.as_view(),
        name="filtres"
    ),
]