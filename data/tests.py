"""
Tests pour l'API Renovation.

Exécution: python manage.py test data.tests
"""

import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import pandas as pd

from data.services.renovation_service import RenovationDataService
from data.dto.renovation_dto import (
    StatsBatimentDTO,
    StatsDPEDTO,
    StatsTypeTravauxDTO,
    DPE_COLORS,
)


class MockDataMixin:
    """Mixin avec des données de test."""

    @staticmethod
    def get_mock_renovation_dataframe():
        """Retourne un DataFrame de rénovation de test."""
        data = {
            "annee": [2020, 2020, 2021, 2021, 2022, 2022],
            "arrondissement": [1, 2, 1, 2, 1, 2],
            "nb_logements": [100, 150, 120, 180, 90, 200],
        }
        return pd.DataFrame(data)

    @staticmethod
    def get_mock_dpe_dataframe():
        """Retourne un DataFrame DPE de test."""
        data = {
            "classe_dpe": [
                "A",
                "A",
                "B",
                "B",
                "B",
                "C",
                "C",
                "D",
                "D",
                "D",
                "E",
                "F",
                "G",
            ],
        }
        return pd.DataFrame(data)


class RenovationDTOTest(TestCase):
    """Tests des DTOs."""

    def test_stats_batiment_dto(self):
        """Test du DTO StatsBatiment."""
        dto = StatsBatimentDTO(
            name="1er",
            total=41000,
            renovated=15400,
            private_renovated=10000,
            social_renovated=5400,
        )

        result = dto.to_dict()

        self.assertEqual(result["name"], "1er")
        self.assertEqual(result["total"], 41000)
        self.assertEqual(result["renovated"], 15400)
        self.assertEqual(result["private_renovated"], 10000)
        self.assertEqual(result["social_renovated"], 5400)

    def test_stats_batiment_renovation_rate(self):
        """Test du calcul du taux de rénovation."""
        dto = StatsBatimentDTO(
            name="1er",
            total=100,
            renovated=25,
            private_renovated=15,
            social_renovated=10,
        )

        self.assertEqual(dto.renovation_rate, 25.0)

    def test_stats_dpe_dto(self):
        """Test du DTO StatsDPE."""
        dto = StatsDPEDTO(class_="A", count=1500, color="#10B981")

        result = dto.to_dict()

        # Vérifie que "class_" devient "class" dans le JSON
        self.assertEqual(result["class"], "A")
        self.assertEqual(result["count"], 1500)
        self.assertEqual(result["color"], "#10B981")

    def test_stats_types_dto(self):
        """Test du DTO StatsTypeTravaux."""
        dto = StatsTypeTravauxDTO(
            type="Isolation Thermique", count=12500, percentage=35
        )

        result = dto.to_dict()

        self.assertEqual(result["type"], "Isolation Thermique")
        self.assertEqual(result["count"], 12500)
        self.assertEqual(result["percentage"], 35)


class RenovationServiceTest(TestCase, MockDataMixin):
    """Tests du service de données."""

    def setUp(self):
        """Configuration initiale."""
        self.service = RenovationDataService.__new__(RenovationDataService)
        self.service._df_renovation = self.get_mock_renovation_dataframe()
        self.service._df_dpe = self.get_mock_dpe_dataframe()
        self.service.renovation_csv_path = None
        self.service.dpe_csv_path = None

    def test_get_stats_batiments(self):
        """Test de get_stats_batiments."""
        result = self.service.get_stats_batiments()

        self.assertEqual(len(result), 2)  # 2 arrondissements
        self.assertIsInstance(result[0], StatsBatimentDTO)

        # Vérifier les noms d'arrondissement
        names = [r.name for r in result]
        self.assertIn("1er", names)
        self.assertIn("2e", names)

        # Vérifier les totaux rénovés
        arr1 = next(r for r in result if r.name == "1er")
        self.assertEqual(arr1.renovated, 310)  # 100 + 120 + 90

    def test_get_stats_batiments_with_filter(self):
        """Test du filtrage par période."""
        result = self.service.get_stats_batiments(annee_debut=2021, annee_fin=2021)

        arr1 = next(r for r in result if r.name == "1er")
        self.assertEqual(arr1.renovated, 120)  # Seulement 2021

    def test_get_stats_dpe(self):
        """Test de get_stats_dpe."""
        result = self.service.get_stats_dpe()

        self.assertEqual(len(result), 7)  # 7 classes (A-G)

        # Vérifier l'ordre (A -> G)
        classes = [r.class_ for r in result]
        self.assertEqual(classes, ["A", "B", "C", "D", "E", "F", "G"])

        # Vérifier les couleurs
        for r in result:
            self.assertEqual(r.color, DPE_COLORS[r.class_])

    def test_get_stats_types(self):
        """Test de get_stats_types."""
        result = self.service.get_stats_types()

        self.assertEqual(len(result), 5)  # 5 types de travaux

        # Vérifier que les pourcentages totalisent 100%
        total_pct = sum(r.percentage for r in result)
        self.assertEqual(total_pct, 100)

        # Vérifier les types
        types = [r.type for r in result]
        self.assertIn("Isolation Thermique", types)
        self.assertIn("Chauffage / EnR", types)

    def test_format_arrondissement_name(self):
        """Test du formatage des noms d'arrondissement."""
        self.assertEqual(self.service._format_arrondissement_name(1), "1er")
        self.assertEqual(self.service._format_arrondissement_name(2), "2e")
        self.assertEqual(self.service._format_arrondissement_name(20), "20e")

    def test_get_filtres_disponibles(self):
        """Test des filtres disponibles."""
        result = self.service.get_filtres_disponibles()

        self.assertEqual(len(result.arrondissements), 20)
        self.assertEqual(result.arrondissements[0], "1er")
        self.assertEqual(result.classes_dpe, ["A", "B", "C", "D", "E", "F", "G"])


class RenovationAPITest(TestCase, MockDataMixin):
    """Tests des endpoints API."""

    def setUp(self):
        """Configuration initiale."""
        self.client = Client()

        # Mock du service
        self.mock_service = MagicMock(spec=RenovationDataService)

        self.patcher = patch(
            "data.views.get_renovation_service", return_value=self.mock_service
        )
        self.patcher.start()

    def tearDown(self):
        """Nettoyage."""
        self.patcher.stop()

    def test_stats_batiments_endpoint_list_format(self):
        """Test de /stats-batiments/ format liste."""
        self.mock_service.get_stats_batiments.return_value = [
            StatsBatimentDTO("1er", 41000, 15400, 10000, 5400),
            StatsBatimentDTO("2e", 49000, 19500, 12000, 7500),
        ]

        response = self.client.get(reverse("renovation:stats-batiments"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # Doit être une liste directe
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "1er")
        self.assertEqual(data[0]["total"], 41000)

    def test_stats_batiments_endpoint_api_format(self):
        """Test de /stats-batiments/?format=api."""
        self.mock_service.get_stats_batiments.return_value = [
            StatsBatimentDTO("1er", 41000, 15400, 10000, 5400),
        ]

        response = self.client.get(
            reverse("renovation:stats-batiments"), {"format": "api"}
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # Doit être un objet avec success/data/meta
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("meta", data)

    def test_stats_dpe_endpoint(self):
        """Test de /stats-dpe/."""
        self.mock_service.get_stats_dpe.return_value = [
            StatsDPEDTO("A", 1500, "#10B981"),
            StatsDPEDTO("B", 3200, "#34D399"),
        ]

        response = self.client.get(reverse("renovation:stats-dpe"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["class"], "A")
        self.assertEqual(data[0]["color"], "#10B981")

    def test_stats_types_endpoint(self):
        """Test de /stats-types/."""
        self.mock_service.get_stats_types.return_value = [
            StatsTypeTravauxDTO("Isolation Thermique", 12500, 35),
            StatsTypeTravauxDTO("Chauffage / EnR", 8900, 25),
        ]

        response = self.client.get(reverse("renovation:stats-types"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["type"], "Isolation Thermique")
        self.assertEqual(data[0]["percentage"], 35)

    def test_dashboard_endpoint(self):
        """Test de /dashboard/."""
        from data.dto.renovation_dto import DashboardDataDTO

        self.mock_service.get_dashboard_data.return_value = DashboardDataDTO(
            stats_batiments=[StatsBatimentDTO("1er", 41000, 15400, 10000, 5400)],
            stats_dpe=[StatsDPEDTO("A", 1500, "#10B981")],
            stats_types=[StatsTypeTravauxDTO("Isolation", 12500, 35)],
        )

        response = self.client.get(reverse("renovation:dashboard"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertIn("stats_batiments", data)
        self.assertIn("stats_dpe", data)
        self.assertIn("stats_types", data)

    def test_filtres_endpoint(self):
        """Test de /filtres/."""
        from data.dto.renovation_dto import FiltresDisponiblesDTO

        self.mock_service.get_filtres_disponibles.return_value = FiltresDisponiblesDTO(
            arrondissements=["1er", "2e"],
            classes_dpe=["A", "B", "C"],
            types_travaux=["Isolation"],
        )

        response = self.client.get(reverse("renovation:filtres"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertIn("arrondissements", data)
        self.assertIn("classes_dpe", data)
        self.assertIn("types_travaux", data)

    def test_error_handling(self):
        """Test de la gestion des erreurs."""
        self.mock_service.get_stats_batiments.side_effect = Exception("Erreur test")

        response = self.client.get(reverse("renovation:stats-batiments"))

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)

        self.assertFalse(data["success"])
        self.assertIn("error", data)


class JSONFormatComplianceTest(TestCase):
    """Tests de conformité avec les formats JSON attendus."""

    def test_stats_batiments_json_format(self):
        """Vérifie que le format correspond à stats_batiments.json."""
        dto = StatsBatimentDTO(
            name="1er",
            total=41000,
            renovated=15400,
            private_renovated=10000,
            social_renovated=5400,
        )

        result = dto.to_dict()

        # Vérifier toutes les clés attendues
        expected_keys = {
            "name",
            "total",
            "renovated",
            "private_renovated",
            "social_renovated",
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_stats_dpe_json_format(self):
        """Vérifie que le format correspond à stats_dpe.json."""
        dto = StatsDPEDTO(class_="A", count=1500, color="#10B981")

        result = dto.to_dict()

        # Vérifier toutes les clés attendues
        expected_keys = {"class", "count", "color"}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_stats_types_json_format(self):
        """Vérifie que le format correspond à stats_types.json."""
        dto = StatsTypeTravauxDTO(
            type="Isolation Thermique", count=12500, percentage=35
        )

        result = dto.to_dict()

        # Vérifier toutes les clés attendues
        expected_keys = {"type", "count", "percentage"}
        self.assertEqual(set(result.keys()), expected_keys)
