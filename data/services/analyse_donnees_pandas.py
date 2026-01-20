from pathlib import Path
import pandas as pd
from django.conf import settings


class analyse_data_renovationParis:
    def __init__(self, data_source_dir: str = None):
        """
        Initialise la classe avec les DataFrames pré-chargés

        Args:
            data_source_dir: chemin relatif optionnel vers data_sources/
                           (par défaut: data/static/data_sources/)
        """
        if data_source_dir is None:
            base_path = Path(settings.BASE_DIR) / "data" / "static" / "data_sources"
        else:
            base_path = Path(settings.BASE_DIR) / data_source_dir

        # Chargement des 3 fichiers CSV
        self.df_renovation = self._load_renovation(base_path)
        self.df_dpe = self._load_dpe(base_path)
        self.df_dpe_types = self._load_dpe_types(base_path)

    def _load_renovation(self, base_path):
        """Charge et prépare renovation.csv"""
        csv_path = base_path / "renovation.csv"
        df = pd.read_csv(csv_path, sep=";", decimal=".")
        df = df.rename(
            columns={
                "Année de vote des travaux": "Annee",
                "Arrondissement": "Arrondissement",
                "Nombre de logts avec vote travaux": "Nb_logements",
            }
        )
        df["Annee"] = df["Annee"].astype(int)
        df["Arrondissement"] = df["Arrondissement"].astype(int)
        df["Nb_logements"] = df["Nb_logements"].astype(int)
        return df

    def _load_dpe(self, base_path):
        """Charge dpe-75.csv"""
        csv_path = base_path / "dpe-75.csv"
        return pd.read_csv(csv_path, sep=";")

    def _load_dpe_types(self, base_path):
        """Charge dpe-75(3).csv (ou dpe-75.csv si pas trouvé)"""
        csv_path = base_path / "dpe-75(3).csv"
        if csv_path.exists():
            return pd.read_csv(csv_path, sep=";")
        else:
            # Fallback sur dpe-75.csv
            return self._load_dpe(base_path)

    # -------------------------------------------------
    # 1) Bâtiments - get_data_Batiment_renovates()
    # {"name": "1er", "total": ..., "renovated": ..., "private_renovated": ..., "social_renovated": ...}
    # -------------------------------------------------
    def get_data_Batiment_renovates(self):
        df = self.df_renovation

        agg = (
            df.groupby("Arrondissement")["Nb_logements"]
            .sum()
            .reset_index()
            .rename(columns={"Nb_logements": "renovated"})
        )

        agg["total"] = agg["renovated"]
        agg["private_renovated"] = 0  # À adapter avec vraies colonnes
        agg["social_renovated"] = 0  # À adapter avec vraies colonnes

        results = []
        for _, row in agg.iterrows():
            arr = int(row["Arrondissement"]) % 100  # 75001 → 1, 75002 → 2
            if arr == 1:
                name = "1er"
            else:
                name = f"{arr}e"

            results.append(
                {
                    "name": name,
                    "total": int(row["total"]),
                    "renovated": int(row["renovated"]),
                    "private_renovated": int(row["private_renovated"]),
                    "social_renovated": int(row["social_renovated"]),
                }
            )

        return results

    # -------------------------------------------------
    # 2) DPE - get_data_energy_classes()
    # {"class": "A", "count": 1500}
    # -------------------------------------------------
    def get_data_energy_classes(self):
        df = self._clean_dpe_energy(self.df_dpe)

        stats_energie = (
            df.groupby("classe_consommation_energie")
            .size()
            .reset_index(name="count")
            .sort_values("classe_consommation_energie")
        )

        results = []
        for _, row in stats_energie.iterrows():
            results.append(
                {
                    "class": str(row["classe_consommation_energie"]),
                    "count": int(row["count"]),
                }
            )

        return results

    def _clean_dpe_energy(self, df):
        """Nettoie les données DPE pour les classes A-G"""
        return df[
            df["classe_consommation_energie"].isin(["A", "B", "C", "D", "E", "F", "G"])
        ]

    # -------------------------------------------------
    # 3) Types - get_data_Renovation_types()
    # {"type": "...", "count": ..., "percentage": ...}
    # -------------------------------------------------
    def get_data_Renovation_types(self):
        df = self.df_dpe_types.dropna(subset=["tr002_type_batiment_libelle"])

        stats_batiment = (
            df.groupby("tr002_type_batiment_libelle").size().reset_index(name="count")
        )

        total_global = stats_batiment["count"].sum()

        results = []
        for _, row in stats_batiment.iterrows():
            count = int(row["count"])
            percentage = (
                round(count / total_global * 100, 2) if total_global > 0 else 0.0
            )

            results.append(
                {
                    "type": str(row["tr002_type_batiment_libelle"]),
                    "count": count,
                    "percentage": percentage,
                }
            )

        return results
