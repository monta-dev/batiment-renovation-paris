# 📔 Journal de Développement - Refonte Architecture Frontend

## 📅 12 Janvier 2026 - Refactoring JS et Séparation des Responsabilités

### 🎯 Objectif
Pass d'un script "monolithique" inclus dans le HTML à une architecture modulaire et maintenable pour le Dashboard statique. Cela permet de simuler une structure professionnelle (Clean Architecture côté Frontend).

### 🛠️ Modifications Effectuées

#### 1. Création de la structure JS (`docs/templates/js/`)
Nous avons éclaté la logique en 3 fichiers distincts ayant chacun une responsabilité unique (Single Responsibility Principle) :

- **`apiFetch.js`** (La couche Service) :
    - Responsable uniquement de la récupération des données.
    - Gère les appels réseaux (`fetch`) vers les fichiers JSON.
    - Utilise `Promise.all` pour optimiser le chargement parallèle des 3 sources de données (`batiments`, `types`, `dpe`).
    - Ne connait rien de l'affichage ou des graphiques.

- **`configChart.js`** (La couche Configuration) :
    - Contient toute la configuration visuelle des graphiques ApexCharts.
    - Stocke la palette de couleurs (`donutColors`).
    - Expose des fonctions helpers (`getBarOptions`, `getDonutOptions`) pour générer les objets de configuration proprement.

- **`controller.js`** (Le Chef d'Orchestre) :
    - Importe `apiFetch` et `configChart`.
    - Initialise l'application (`initDashboard`).
    - Transforme les données brutes (DTOs) en format compatible graphiques.
    - Gère le rendu du DOM (`renderBuildingStats`, `renderList`).
    - Gère les interactions utilisateur (Accordéons du menu).

#### 2. Mise à jour de `dashboard.html`
- Suppression de tout le code JavaScript inline (~150 lignes).
- Remplacement par une seule ligne d'import module :
  ```html
  <script type="module" src="js/controller.js"></script>
  ```

### 🚀 Bénéfices
1. **Lisibilité** : Chaque fichier fait moins de 100 lignes et est très focalisé.
2. **Maintenabilité** : Si on veut changer la couleur des graphiques, on va uniquement dans `configChart.js`. Si on veut changer l'URL de l'API, on va dans `apiFetch.js`.
3. **Réutilisabilité** : `configChart.js` pourrait être réutilisé par d'autres pages sans dupliquer le code.

## 📅 12 Janvier 2026 (Suite) - Architecture "SPA-Like" et Optimisations

### 🔄 Évolution de l'Architecture
Nous sommes passés d'un simple découpage fonctionnel à une véritable architecture MVC (Modèle-Vue-Contrôleur) côté client, orchestrée par un **Front Controller**.

#### 1. Architecture des Contrôleurs (`js/controllers/`)
Le fichier unique `controller.js` a été divisé pour respecter le principe de responsabilité unique (SRP) :
- **`mainController.js` (Front Controller)** :
    - Point d'entrée unique de l'application.
    - Gère le **Routing** (détection de la page via `data-page`).
    - Gère la **Sécurité** (vérification via `AuthService`).
    - Dispatch la logique vers les sous-contrôleurs spécialisés.
- **`buildingController.js`** : Gère spécifiquement le tableau de bord "Bâtiments".
- **`typesController.js`** : Gère l'affichage des "Types de Rénovation".
- **`dpeController.js`** : Gère l'affichage des "Classes DPE".

#### 2. Services Transverses (`js/services/` & `js/utils/`)
- **`authService.js`** :
    - Simule une couche d'authentification (Login/Logout).
    - Permet de protéger l'accès au dashboard (Guard).
- **`ui.js`** :
    - Regroupe les fonctions de manipulation du DOM partagées (titres, sidebar, listes, interactions).

---

### ⚡ Performance & Caching (`apiFetch.js`)
Mise en place d'une stratégie de **Cache LocalStorage** :
- **Principe** : Les données JSON ne sont chargées depuis le réseau que si le cache local est vide ou expiré (+2h).
- **Préchauffage** : Un script invisible sur `home.html` lance le chargement des données en arrière-plan dès l'arrivée sur le site.
- **Résultat** : Affichage instantané lors de la navigation vers les dashboards.

---

### 🎨 Amélioration de l'Expérience Utilisateur (UX)
- **Sidebar Contextuelle** : La barre latérale s'adapte automatiquement à la page courante (masque les sections inutiles).
- **Admin Portal** : Création d'une page d'administration dédiée (`admin_page.html`) avec un design Neumorphic spécifique (`css/admin_page.css`).
- **Navigation Unifiée** : Le lien supérieur "Dashboard" redirige désormais intelligemment vers l'accueil (`home.html`).

## 📅 12 Janvier 2026 (Session Finale) - Standardisation et Passage en SPA

### 🎯 Standardisation Visuelle (Design System)
- **Unification des Headers** : Les pages `about.html` et `contact.html` partagent désormais un header rigoureusement identique.
- **Centralisation CSS** : Les styles globaux (header, menus, body de base) ont été déplacés de `contact.css` vers `style.css` pour être accessibles à toutes les pages.
- **Synchronisation des Polices** : Utilisation uniforme de `Poppins` (titres) et `Inter` (corps) avec les mêmes graisses (400-800) sur tout le site.

### 🧩 Evolution Single Page Application (SPA)
Le Dashboard a été transformé en une véritable **SPA** pour une expérience fluide et professionnelle :
- **Fichier Unique** : `dashboard.html` contient désormais toutes les sections (Bâtiments, Types, DPE).
- **Navigation sans rechargement** : Le `mainController.js` intercepte les clics de la sidebar pour afficher/masquer les sections dynamiquement.
- **Vue "Vue d'ensemble"** : Permet de voir l'intégralité des 8 graphiques sur une seule page (idéal pour une vision globale administrative).
- **Maintien des Filtres** : Réintégration des menus accordéons (`Années`, `Types de travaux`, `Classes DPE`) directement dans la sidebar de la SPA, permettant de filtrer les données sans changer de page.

### 🛠️ Corrections Techniques
- **Resize Trigger** : Ajout d'un événement de redimensionnement forcé lors du changement de vue pour garantir que les graphiques `ApexCharts` recalculent leurs dimensions correctement dans les conteneurs nouvellement visibles.
- **Nettoyage des Chemins** : Correction des liens relatifs dans les nouveaux fichiers HTML statiques.
