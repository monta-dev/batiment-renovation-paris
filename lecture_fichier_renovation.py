#-----------------------------------------------------------------------------------
#lecture fichier csv renovation
import pandas as pd
import numpy as np
df = pd.read_csv("renovation.csv", sep = ';', header = 0)
print(df)
print(df.head())
print(df.iloc[0:5, 0:3])
print(df.iloc[0:5, 1:3])
print(df.iloc[0:5, 1:])

#lecture fichier csv renovation
#-----------------------------------------------------------------------------------



#nombre de logemets renovés par arrondissement
import pandas as pd

df = pd.read_csv("renovation.csv", sep=';')

logements_par_arr = (
    df.groupby("Arrondissement")["Nombre de logts avec vote travaux"]
      .sum()
)

print(logements_par_arr)

#nombre de logemets renovés par arrondissement



#-----------------------------------------------------------------------------------
#nombre de logemets renovés par arrondissement et par année
import pandas as pd

# Chargement
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal=".",
)

df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# Conversion des types
# Arrondissement : entier (en supprimant le .0)
df["Arrondissement"] = df["Arrondissement"].astype(int)

# Nombre de logements : entier
df["Nb_logements"] = df["Nb_logements"].astype(int)

# Annee : entier (au cas où)
df["Annee"] = df["Annee"].astype(int)

# 1) Nombre de logements par arrondissement
logements_par_arrondissement = (
    df.groupby("Arrondissement")["Nb_logements"].sum().reset_index()
)

print("Nombre de logements par arrondissement :")
print(logements_par_arrondissement)

# 2) Nombre de logements par année
logements_par_annee = df.groupby("Annee")["Nb_logements"].sum().reset_index()

print("\nNombre de logements par année :")
print(logements_par_annee)

#nombre de logemets renovés par arrondissement et par année
#-----------------------------------------------------------------------------------













#-----------------------------------------------------------------------------------
# nombre de logements rénovés par année et nombre de logements rénovés par arrondissement

import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# Renommage des colonnes
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# Conversion des types
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# 1) Histogramme du nombre de logements par ANNÉE
# ======================================================
logements_par_annee = (
    df.groupby("Annee")["Nb_logements"]
      .sum()
      .reset_index()
)

logements_par_annee.hist(
    column="Nb_logements",
    bins=10,
    grid=True,
    figsize=(8, 5)
)

plt.xlabel("Année")
plt.ylabel("Nombre de logements rénovés")
plt.title("Histogramme du nombre de logements rénovés par année")
plt.show()

# ======================================================
# 2) Histogramme du nombre de logements par ARRONDISSEMENT
# ======================================================
logements_par_arrondissement = (
    df.groupby("Arrondissement")["Nb_logements"]
      .sum()
      .reset_index()
)

logements_par_arrondissement.hist(
    column="Nb_logements",
    bins=10,
    grid=True,
    figsize=(8, 5)
)

plt.xlabel("Arrondissement")
plt.ylabel("Nombre de logements rénovés")
plt.title("Histogramme du nombre de logements rénovés par arrondissement")
plt.show()

# nombre de logements rénovés par année et nombre de logements rénovés par arrondissement
#-----------------------------------------------------------------------------------






#-----------------------------------------------------------------------------------
# ======================================================
# Nombre de logements rénovés par année
# et par arrondissement + tableau croisé
# ======================================================

import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# Chargement des données
# ======================================================
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# ======================================================
# Renommage des colonnes
# ======================================================
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# ======================================================
# Conversion des types
# ======================================================
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# 1) Histogramme du nombre de logements par ANNÉE
# ======================================================
logements_par_annee = (
    df.groupby("Annee")["Nb_logements"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.hist(logements_par_annee["Nb_logements"], bins=10)
plt.xlabel("Année")
plt.ylabel("Nombre de logements rénovés")
plt.title("Histogramme du nombre de logements rénovés par année")
plt.grid(True)
plt.show()

# ======================================================
# 2) Histogramme du nombre de logements par ARRONDISSEMENT
# ======================================================
logements_par_arrondissement = (
    df.groupby("Arrondissement")["Nb_logements"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.hist(logements_par_arrondissement["Nb_logements"], bins=10)
plt.xlabel("Arrondissement")
plt.ylabel("Nombre de logements rénovés")
plt.title("Histogramme du nombre de logements rénovés par arrondissement")
plt.grid(True)
plt.show()

# ======================================================
# 3) Tableau : logements par ARRONDISSEMENT et par ANNÉE
# ======================================================
tableau_arrondissement_annee = pd.pivot_table(
    df,
    values="Nb_logements",
    index="Arrondissement",
    columns="Annee",
    aggfunc="sum",
    fill_value=0
)

print("\nNombre de logements rénovés par arrondissement et par année :\n")
print(tableau_arrondissement_annee)

# ======================================================
# (Optionnel) Sauvegarde du tableau en CSV
# ======================================================
tableau_arrondissement_annee.to_csv(
    "logements_par_arrondissement_et_par_annee.csv",
    sep=";"
)
#-----------------------------------------------------------------------------------







#-----------------------------------------------------------------------------------
# ======================================================
# Total des logements rénovés par ARRONDISSEMENT
# entre 2014 et 2024
# ======================================================

import pandas as pd

# ======================================================
# Chargement des données
# ======================================================
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# ======================================================
# Renommage des colonnes
# ======================================================
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# ======================================================
# Conversion des types
# ======================================================
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# Filtrage des années 2014 à 2024 inclus
# ======================================================
df_filtre = df[(df["Annee"] >= 2014) & (df["Annee"] <= 2024)]

# ======================================================
# Total des logements rénovés par arrondissement
# ======================================================
total_par_arrondissement = (
    df_filtre
        .groupby("Arrondissement")["Nb_logements"]
        .sum()
        .reset_index()
        .rename(columns={"Nb_logements": "Total_logements_2014_2024"})
)

print("\nTotal de logements rénovés par arrondissement (2014–2024) :\n")
print(total_par_arrondissement)

# ======================================================
# Sauvegarde en CSV
# ======================================================
total_par_arrondissement.to_csv(
    "total_logements_par_arrondissement_2014_2024.csv",
    sep=";",
    index=False
)
#-----------------------------------------------------------------------------------








#-----------------------------------------------------------------------------------
# ======================================================
# Tableau du nombre de logements rénovés
# par ARRONDISSEMENT pour les années 2023 et 2024
# ======================================================

import pandas as pd

# ======================================================
# Chargement des données
# ======================================================
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# ======================================================
# Renommage des colonnes
# ======================================================
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# ======================================================
# Conversion des types
# ======================================================
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# Filtrage sur les années 2023 et 2024
# ======================================================
df_filtre = df[df["Annee"].isin([2023, 2024])]

# ======================================================
# Tableau croisé : logements par arrondissement et par année
# ======================================================
tableau_arrondissement_annee = pd.pivot_table(
    df_filtre,
    values="Nb_logements",
    index="Arrondissement",
    columns="Annee",
    aggfunc="sum",
    fill_value=0
)

print("\nNombre de logements rénovés par arrondissement (2023–2024) :\n")
print(tableau_arrondissement_annee)

# ======================================================
# Sauvegarde du tableau en CSV
# ======================================================
tableau_arrondissement_annee.to_csv(
    "logements_par_arrondissement_2023_2024.csv",
    sep=";"
)
#-----------------------------------------------------------------------------------



















#-----------------------------------------------------------------------------------
# ======================================================
# Total des logements rénovés par ARRONDISSEMENT
# pour les années 2023 et 2024
# ======================================================

import pandas as pd

# ======================================================
# Chargement des données
# ======================================================
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# ======================================================
# Renommage des colonnes
# ======================================================
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# ======================================================
# Conversion des types
# ======================================================
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# Filtrage sur les années 2023 et 2024
# ======================================================
df_filtre = df[df["Annee"].isin([2023, 2024])]

# ======================================================
# Total des logements par arrondissement (2023 + 2024)
# ======================================================
total_par_arrondissement = (
    df_filtre
        .groupby("Arrondissement")["Nb_logements"]
        .sum()
        .reset_index()
        .rename(columns={"Nb_logements": "Total_logements_2023_2024"})
)

print("\nTotal de logements rénovés par arrondissement (2023–2024) :\n")
print(total_par_arrondissement)

# ======================================================
# Sauvegarde du résultat en CSV
# ======================================================
total_par_arrondissement.to_csv(
    "total_logements_par_arrondissement_2023_2024.csv",
    sep=";",
    index=False
)
#-----------------------------------------------------------------------------------
















#-----------------------------------------------------------------------------------
#(1)
# ======================================================
# Analyse des logements rénovés
# - Par année
# - Par arrondissement
# - Tableau croisé
# - Total par arrondissement (2014–2024)
# ======================================================

import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# Chargement des données
# ======================================================
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# ======================================================
# Renommage des colonnes
# ======================================================
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# ======================================================
# Conversion des types
# ======================================================
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# 1) Histogramme : logements rénovés par ANNÉE
# ======================================================
logements_par_annee = (
    df.groupby("Annee")["Nb_logements"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(logements_par_annee["Annee"], logements_par_annee["Nb_logements"])
plt.xlabel("Année")
plt.ylabel("Nombre de logements rénovés")
plt.title("Nombre de logements rénovés par année")
plt.grid(True)
plt.show()

# ======================================================
# 2) Histogramme : logements rénovés par ARRONDISSEMENT
# ======================================================
logements_par_arrondissement = (
    df.groupby("Arrondissement")["Nb_logements"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    logements_par_arrondissement["Arrondissement"],
    logements_par_arrondissement["Nb_logements"]
)
plt.xlabel("Arrondissement")
plt.ylabel("Nombre de logements rénovés")
plt.title("Nombre de logements rénovés par arrondissement")
plt.grid(True)
plt.show()

# ======================================================
# 3) Tableau croisé : ARRONDISSEMENT x ANNÉE
# ======================================================
tableau_arrondissement_annee = pd.pivot_table(
    df,
    values="Nb_logements",
    index="Arrondissement",
    columns="Annee",
    aggfunc="sum",
    fill_value=0
)

print("\nNombre de logements rénovés par arrondissement et par année :\n")
print(tableau_arrondissement_annee)

tableau_arrondissement_annee.to_csv(
    "logements_par_arrondissement_et_par_annee.csv",
    sep=";"
)

# ======================================================
# 4) Total des logements rénovés par ARRONDISSEMENT
#    entre 2014 et 2024
# ======================================================
df_2014_2024 = df[(df["Annee"] >= 2014) & (df["Annee"] <= 2024)]

total_par_arrondissement = (
    df_2014_2024
        .groupby("Arrondissement")["Nb_logements"]
        .sum()
        .reset_index()
        .rename(columns={"Nb_logements": "Total_logements_2014_2024"})
)

print("\nTotal de logements rénovés par arrondissement (2014–2024) :\n")
print(total_par_arrondissement)

total_par_arrondissement.to_csv(
    "total_logements_par_arrondissement_2014_2024.csv",
    sep=";",
    index=False
)
#-----------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------
# ======================================================
# 4) Total ET POURCENTAGE des logements rénovés
#    par ARRONDISSEMENT entre 2014 et 2024
# ======================================================
df_2014_2024 = df[(df["Annee"] >= 2014) & (df["Annee"] <= 2024)]

# Total par arrondissement
total_par_arrondissement = (
    df_2014_2024
        .groupby("Arrondissement")["Nb_logements"]
        .sum()
        .reset_index()
        .rename(columns={"Nb_logements": "Total_logements_2014_2024"})
)

# Total général (tous arrondissements)
total_general = total_par_arrondissement["Total_logements_2014_2024"].sum()

# Calcul du pourcentage
total_par_arrondissement["Pourcentage"] = (
    total_par_arrondissement["Total_logements_2014_2024"] / total_general * 100
).round(2)

print("\nTotal et pourcentage de logements rénovés par arrondissement (2014–2024) :\n")
print(total_par_arrondissement)

# Export CSV
total_par_arrondissement.to_csv(
    "total_et_pourcentage_logements_par_arrondissement_2014_2024.csv",
    sep=";",
    index=False
)
#-----------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------
#(1)
# ======================================================
# Analyse des logements rénovés
# - Par année
# - Par arrondissement
# - Tableau croisé
# - Total par arrondissement (2014–2024)
# - Total GLOBAL tous arrondissements (2014–2024)
# ======================================================

import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# Chargement des données
# ======================================================
df = pd.read_csv(
    "renovation.csv",
    sep=";",
    decimal="."
)

# ======================================================
# Renommage des colonnes
# ======================================================
df = df.rename(
    columns={
        "Année de vote des travaux": "Annee",
        "Arrondissement": "Arrondissement",
        "Nombre de logts avec vote travaux": "Nb_logements",
    }
)

# ======================================================
# Conversion des types
# ======================================================
df["Annee"] = df["Annee"].astype(int)
df["Arrondissement"] = df["Arrondissement"].astype(int)
df["Nb_logements"] = df["Nb_logements"].astype(int)

# ======================================================
# 1) Histogramme : logements rénovés par ANNÉE
# ======================================================
logements_par_annee = (
    df.groupby("Annee")["Nb_logements"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(logements_par_annee["Annee"], logements_par_annee["Nb_logements"])
plt.xlabel("Année")
plt.ylabel("Nombre de logements rénovés")
plt.title("Nombre de logements rénovés par année")
plt.grid(True)
plt.show()

# ======================================================
# 2) Histogramme : logements rénovés par ARRONDISSEMENT
# ======================================================
logements_par_arrondissement = (
    df.groupby("Arrondissement")["Nb_logements"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    logements_par_arrondissement["Arrondissement"],
    logements_par_arrondissement["Nb_logements"]
)
plt.xlabel("Arrondissement")
plt.ylabel("Nombre de logements rénovés")
plt.title("Nombre de logements rénovés par arrondissement")
plt.grid(True)
plt.show()

# ======================================================
# 3) Tableau croisé : ARRONDISSEMENT x ANNÉE
# ======================================================
tableau_arrondissement_annee = pd.pivot_table(
    df,
    values="Nb_logements",
    index="Arrondissement",
    columns="Annee",
    aggfunc="sum",
    fill_value=0
)

print("\nNombre de logements rénovés par arrondissement et par année :\n")
print(tableau_arrondissement_annee)

tableau_arrondissement_annee.to_csv(
    "logements_par_arrondissement_et_par_annee.csv",
    sep=";"
)

# ======================================================
# 4) Total des logements rénovés par ARRONDISSEMENT
#    entre 2014 et 2024
# ======================================================
df_2014_2024 = df[(df["Annee"] >= 2014) & (df["Annee"] <= 2024)]

total_par_arrondissement = (
    df_2014_2024
        .groupby("Arrondissement")["Nb_logements"]
        .sum()
        .reset_index()
        .rename(columns={"Nb_logements": "Total_logements_2014_2024"})
)

print("\nTotal de logements rénovés par arrondissement (2014–2024) :\n")
print(total_par_arrondissement)

total_par_arrondissement.to_csv(
    "total_logements_par_arrondissement_2014_2024.csv",
    sep=";",
    index=False
)

# ======================================================
# 5) Total GLOBAL des logements rénovés
#    tous arrondissements confondus (2014–2024)
# ======================================================
total_global_logements = df_2014_2024["Nb_logements"].sum()

print("\n==============================================")
print("TOTAL GLOBAL des logements rénovés (2014–2024)")
print("Tous arrondissements confondus :")
print(total_global_logements)
print("==============================================")

pd.DataFrame({
    "Periode": ["2014-2024"],
    "Total_logements_tous_arrondissements": [total_global_logements]
}).to_csv(
    "total_global_logements_2014_2024.csv",
    sep=";",
    index=False
)

#-----------------------------------------------------------------------------------







#-----------------------------------------------------------------------------------
#(3)
#-----------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# 1) Chargement des données (Fichier DPE-75)
# ======================================================
# Note : Le fichier utilise des virgules comme séparateur
df = pd.read_csv("dpe-75.csv", sep=",")

# ======================================================
# 2) Préparation des données pour le graphique
# ======================================================
# On compte le nombre d'occurrences pour chaque classe énergétique
# On filtre les valeurs "N" ou manquantes si nécessaire
df_clean = df[df["classe_consommation_energie"].isin(['A', 'B', 'C', 'D', 'E', 'F', 'G'])]

stats_energie = (
    df_clean.groupby("classe_consommation_energie")
    .size()
    .reset_index(name="Nb_logements")
)

# On s'assure que les classes sont dans l'ordre alphabétique (A -> G)
stats_energie = stats_energie.sort_values("classe_consommation_energie")

# ======================================================
# 3) Tracé de la courbe
# ======================================================
plt.figure(figsize=(10, 6))
plt.plot(
    stats_energie["classe_consommation_energie"], 
    stats_energie["Nb_logements"], 
    marker='o', 
    linestyle='-', 
    color='b',
    linewidth=2
)

# Ajout des labels et du titre
plt.xlabel("Classe de consommation énergétique")
plt.ylabel("Nombre de logements")
plt.title("Répartition des logements par classe énergétique (DPE Paris)")
plt.grid(True, linestyle='--', alpha=0.7)

# Optionnel : Colorer les points pour rappeler les étiquettes DPE
for i, txt in enumerate(stats_energie["Nb_logements"]):
    plt.annotate(txt, (stats_energie["classe_consommation_energie"].iloc[i], stats_energie["Nb_logements"].iloc[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center')

plt.show()

# ======================================================
# 4) Affichage du récapitulatif dans la console
# ======================================================
print("\nRépartition par classe énergétique :")
print(stats_energie.to_string(index=False))
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# 1) Chargement des données
# ======================================================
df = pd.read_csv("dpe-75(3).csv", sep=",")

# ======================================================
# 2) Nettoyage et préparation des données
# ======================================================
# On garde uniquement les valeurs non nulles
df_clean = df.dropna(subset=["tr002_type_batiment_libelle"])

# Comptage du nombre de bâtiments par type
stats_batiment = (
    df_clean.groupby("tr002_type_batiment_libelle")
    .size()
    .reset_index(name="Nb_batiments")
)

# ======================================================
# 3) Affichage graphique
# ======================================================
plt.figure(figsize=(8, 5))
plt.bar(
    stats_batiment["tr002_type_batiment_libelle"],
    stats_batiment["Nb_batiments"]
)

plt.xlabel("Type de bâtiment")
plt.ylabel("Nombre")
plt.title("Nombre de logements et de maisons (DPE Paris)")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Affichage des valeurs au-dessus des barres
for i, value in enumerate(stats_batiment["Nb_batiments"]):
    plt.text(i, value, str(value), ha="center", va="bottom")

plt.show()

# ======================================================
# 4) Affichage du résultat dans la console
# ======================================================
print("\nNombre de logements / maisons :")
print(stats_batiment.to_string(index=False))

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
