"""
DTOs (Data Transfer Objects) pour l'API batimentRenovation.

Ces classes définissent la structure exacte des données JSON
attendues par le frontend pour les graphiques.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


# =============================================================================
# DTO 1: Statistiques par arrondissement (stats_batiments.json)
# =============================================================================

@dataclass
class StatsBatimentDTO:
    """
    Statistiques de rénovation par arrondissement.
    
    Format JSON:
    {
        "name": "1er",
        "total": 41000,
        "renovated": 15400,
        "private_renovated": 10000,
        "social_renovated": 5400
    }
    """
    name: str                    # "1er", "2e", "3e", etc.
    total: int                   # Total de logements
    renovated: int               # Logements rénovés
    private_renovated: int       # Rénovations privées
    social_renovated: int        # Rénovations sociales
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @property
    def renovation_rate(self) -> float:
        """Taux de rénovation en pourcentage."""
        if self.total == 0:
            return 0.0
        return round((self.renovated / self.total) * 100, 2)


# =============================================================================
# DTO 2: Répartition par classe DPE (stats_dpe.json)
# =============================================================================

@dataclass
class StatsDPEDTO:
    """
    Répartition des logements par classe énergétique DPE.
    
    Format JSON:
    {
        "class": "A",
        "count": 1500,
        "color": "#10B981"
    }
    """
    class_: str      # Classe DPE: A, B, C, D, E, F, G (renommé car 'class' est réservé)
    count: int       # Nombre de logements
    color: str       # Couleur pour le graphique
    
    def to_dict(self) -> dict:
        return {
            "class": self.class_,
            "count": self.count,
            "color": self.color
        }


# Couleurs standard DPE
DPE_COLORS = {
    "A": "#10B981",  # Vert foncé
    "B": "#34D399",  # Vert
    "C": "#A7F3D0",  # Vert clair
    "D": "#FCD34D",  # Jaune
    "E": "#F59E0B",  # Orange
    "F": "#EF4444",  # Rouge
    "G": "#7F1D1D",  # Rouge foncé
}


# =============================================================================
# DTO 3: Types de travaux (stats_types.json)
# =============================================================================

@dataclass
class StatsTypeTravauxDTO:
    """
    Statistiques par type de travaux de rénovation.
    
    Format JSON:
    {
        "type": "Isolation Thermique",
        "count": 12500,
        "percentage": 35
    }
    """
    type: str           # Type de travaux
    count: int          # Nombre de logements concernés
    percentage: float   # Pourcentage du total
    
    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# DTOs pour les réponses API
# =============================================================================

@dataclass
class MetaDTO:
    """Métadonnées de la réponse."""
    total_records: int
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    source: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {
            "total_records": self.total_records,
            "generated_at": self.generated_at
        }
        if self.source:
            result["source"] = self.source
        return result


@dataclass
class APIResponseDTO:
    """
    Réponse API standardisée.
    
    Format:
    {
        "success": true,
        "data": [...],
        "meta": {...}
    }
    """
    success: bool
    data: list | dict
    meta: Optional[MetaDTO] = None
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {
            "success": self.success,
            "data": self.data
        }
        if self.meta:
            result["meta"] = self.meta.to_dict()
        if self.error:
            result["error"] = self.error
        return result


# =============================================================================
# DTOs combinés pour dashboard complet
# =============================================================================

@dataclass
class DashboardDataDTO:
    """
    Toutes les données du dashboard en une seule réponse.
    
    Utile pour charger toutes les données en un seul appel API.
    """
    stats_batiments: list[StatsBatimentDTO]
    stats_dpe: list[StatsDPEDTO]
    stats_types: list[StatsTypeTravauxDTO]
    
    def to_dict(self) -> dict:
        return {
            "stats_batiments": [s.to_dict() for s in self.stats_batiments],
            "stats_dpe": [s.to_dict() for s in self.stats_dpe],
            "stats_types": [s.to_dict() for s in self.stats_types]
        }


# =============================================================================
# DTOs pour filtres et paramètres
# =============================================================================

@dataclass
class FiltresDisponiblesDTO:
    """Filtres disponibles pour le frontend."""
    arrondissements: list[str]
    classes_dpe: list[str]
    types_travaux: list[str]
    
    def to_dict(self) -> dict:
        return asdict(self)