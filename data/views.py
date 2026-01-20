"""
Views API pour les données de rénovation.

Endpoints:
- GET /api/renovation/stats-batiments/  → stats_batiments.json
- GET /api/renovation/stats-dpe/        → stats_dpe.json
- GET /api/renovation/stats-types/      → stats_types.json
- GET /api/renovation/dashboard/        → Toutes les données
"""

from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from typing import Optional

from data.services.renovation_service import get_renovation_service
from data.dto.renovation_dto import APIResponseDTO, MetaDTO


class BaseRenovationView(View):
    """Classe de base pour toutes les views de rénovation."""
    
    def get_int_param(self, request, name: str, default: Optional[int] = None) -> Optional[int]:
        """Extrait un paramètre entier de la requête."""
        value = request.GET.get(name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default
    
    def json_response(self, data, status: int = 200) -> JsonResponse:
        """
        Crée une réponse JSON.
        
        Si data est une liste, retourne directement la liste (format attendu par le frontend).
        Si data est un dict avec 'success', retourne le format API standard.
        """
        return JsonResponse(
            data,
            status=status,
            safe=False,  # Permet de retourner une liste directement
            json_dumps_params={"ensure_ascii": False}
        )
    
    def error_response(self, message: str, status: int = 400) -> JsonResponse:
        """Crée une réponse d'erreur."""
        return JsonResponse(
            {"success": False, "error": message, "data": []},
            status=status,
            json_dumps_params={"ensure_ascii": False}
        )


# =============================================================================
# 1. STATS BATIMENTS
# =============================================================================

@method_decorator(require_GET, name='dispatch')
class StatsBatimentsView(BaseRenovationView):
    """
    GET /api/renovation/stats-batiments/
    
    Paramètres optionnels:
        - annee_debut: int
        - annee_fin: int
        - format: "list" (défaut) ou "api"
    
    Retourne les statistiques par arrondissement.
    
    Format "list" (défaut) - Compatible avec le frontend:
    [
        {"name": "1er", "total": 41000, "renovated": 15400, ...},
        {"name": "2e", "total": 49000, "renovated": 19500, ...},
        ...
    ]
    
    Format "api" - Avec métadonnées:
    {
        "success": true,
        "data": [...],
        "meta": {"total_records": 20}
    }
    """
    
    def get(self, request):
        service = get_renovation_service()
        
        annee_debut = self.get_int_param(request, "annee_debut")
        annee_fin = self.get_int_param(request, "annee_fin")
        response_format = request.GET.get("format", "list")
        
        try:
            data = service.get_stats_batiments(annee_debut, annee_fin)
            data_list = [d.to_dict() for d in data]
            
            if response_format == "api":
                response = APIResponseDTO(
                    success=True,
                    data=data_list,
                    meta=MetaDTO(
                        total_records=len(data),
                        source="renovation.csv"
                    )
                )
                return self.json_response(response.to_dict())
            
            # Format liste directe (par défaut)
            return self.json_response(data_list)
            
        except FileNotFoundError as e:
            return self.error_response(f"Fichier de données non trouvé: {e}", status=404)
        except Exception as e:
            return self.error_response(str(e), status=500)


# =============================================================================
# 2. STATS DPE
# =============================================================================

@method_decorator(require_GET, name='dispatch')
class StatsDPEView(BaseRenovationView):
    """
    GET /api/renovation/stats-dpe/
    
    Paramètres optionnels:
        - format: "list" (défaut) ou "api"
    
    Retourne la répartition par classe énergétique DPE.
    
    Format "list" (défaut):
    [
        {"class": "A", "count": 1500, "color": "#10B981"},
        {"class": "B", "count": 3200, "color": "#34D399"},
        ...
    ]
    """
    
    def get(self, request):
        service = get_renovation_service()
        response_format = request.GET.get("format", "list")
        
        try:
            data = service.get_stats_dpe()
            data_list = [d.to_dict() for d in data]
            
            if response_format == "api":
                response = APIResponseDTO(
                    success=True,
                    data=data_list,
                    meta=MetaDTO(
                        total_records=len(data),
                        source="dpe-75.csv"
                    )
                )
                return self.json_response(response.to_dict())
            
            return self.json_response(data_list)
            
        except FileNotFoundError as e:
            return self.error_response(f"Fichier DPE non trouvé: {e}", status=404)
        except Exception as e:
            return self.error_response(str(e), status=500)


# =============================================================================
# 3. STATS TYPES DE TRAVAUX
# =============================================================================

@method_decorator(require_GET, name='dispatch')
class StatsTypesView(BaseRenovationView):
    """
    GET /api/renovation/stats-types/
    
    Paramètres optionnels:
        - annee_debut: int
        - annee_fin: int
        - format: "list" (défaut) ou "api"
    
    Retourne les statistiques par type de travaux.
    
    Format "list" (défaut):
    [
        {"type": "Isolation Thermique", "count": 12500, "percentage": 35},
        {"type": "Chauffage / EnR", "count": 8900, "percentage": 25},
        ...
    ]
    """
    
    def get(self, request):
        service = get_renovation_service()
        
        annee_debut = self.get_int_param(request, "annee_debut")
        annee_fin = self.get_int_param(request, "annee_fin")
        response_format = request.GET.get("format", "list")
        
        try:
            data = service.get_stats_types(annee_debut, annee_fin)
            data_list = [d.to_dict() for d in data]
            
            if response_format == "api":
                response = APIResponseDTO(
                    success=True,
                    data=data_list,
                    meta=MetaDTO(
                        total_records=len(data),
                        source="renovation.csv"
                    )
                )
                return self.json_response(response.to_dict())
            
            return self.json_response(data_list)
            
        except Exception as e:
            return self.error_response(str(e), status=500)


# =============================================================================
# 4. DASHBOARD COMPLET
# =============================================================================

@method_decorator(require_GET, name='dispatch')
class DashboardView(BaseRenovationView):
    """
    GET /api/renovation/dashboard/
    
    Paramètres optionnels:
        - annee_debut: int
        - annee_fin: int
    
    Retourne toutes les données du dashboard en un seul appel.
    
    Format:
    {
        "stats_batiments": [...],
        "stats_dpe": [...],
        "stats_types": [...]
    }
    """
    
    def get(self, request):
        service = get_renovation_service()
        
        annee_debut = self.get_int_param(request, "annee_debut")
        annee_fin = self.get_int_param(request, "annee_fin")
        
        try:
            dashboard_data = service.get_dashboard_data(annee_debut, annee_fin)
            return self.json_response(dashboard_data.to_dict())
            
        except Exception as e:
            return self.error_response(str(e), status=500)


# =============================================================================
# 5. RÉSUMÉ STATISTIQUES
# =============================================================================

@method_decorator(require_GET, name='dispatch')
class StatsSummaryView(BaseRenovationView):
    """
    GET /api/renovation/summary/
    
    Retourne un résumé des statistiques globales.
    
    Format:
    {
        "total_logements": 750000,
        "total_renoves": 280000,
        "taux_renovation": 37.3,
        "total_dpe_diagnostiques": 33000,
        "passoires_thermiques": 6300,
        "taux_passoires": 19.1
    }
    """
    
    def get(self, request):
        service = get_renovation_service()
        
        try:
            summary = service.get_stats_summary()
            return self.json_response(summary)
            
        except Exception as e:
            return self.error_response(str(e), status=500)


# =============================================================================
# 6. FILTRES DISPONIBLES
# =============================================================================

@method_decorator(require_GET, name='dispatch')
class FiltresView(BaseRenovationView):
    """
    GET /api/renovation/filtres/
    
    Retourne les filtres disponibles pour le frontend.
    
    Format:
    {
        "arrondissements": ["1er", "2e", ...],
        "classes_dpe": ["A", "B", "C", "D", "E", "F", "G"],
        "types_travaux": ["Isolation Thermique", ...]
    }
    """
    
    def get(self, request):
        service = get_renovation_service()
        
        try:
            filtres = service.get_filtres_disponibles()
            return self.json_response(filtres.to_dict())
            
        except Exception as e:
            return self.error_response(str(e), status=500)