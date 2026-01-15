/* 
Syntax: JavaScript ES6.
Role: Contrôleur spécialisé dans la présentation des différentes catégories de travaux de rénovation effectués.
Workflow: Analyse les volumes par type de travaux, calcule les ratios et met à jour dynamiquement les graphiques en barres et circulaires.
*/

import { getBarOptions, getDonutOptions, donutColors } from '../configChart.js'; // S: Imports nommés | R: Accès config et couleurs | W: Fournit les outils nécessaires pour le rendu graphique des travaux.
import { renderList, updatePageTitle, setActiveMenu } from '../utils/ui.js'; // S: Imports nommés | R: Utilitaires UI | W: Gère la mise à jour des éléments textuels et de navigation du DOM.

export const TypesController = {
  // S: Objet exporté | R: Namespace "Types" | W: Centralise la logique liée aux catégories de travaux.
  /**
   * Initializes the Types Dashboard view.
   * @param {Object} data
   */
  init(data, config = {}) {
    // S: Méthode d'init | R: Boot de la page Types | W: Configure l'interface detaillee ou globale et lance le calcul des stats.
    console.log('🛠️ [TypesController] Initializing...'); // S: Log console | R: Trace de démarrage | W: Permet de suivre l'exécution du code dans l'inspecteur.

    if (!config.isOverview) {
      // S: Condition if | R: Vérifie le mode d'affichage | W: Applique les réglages de titre et de menu si on n'est pas sur l'aperçu global.
      updatePageTitle('Types de Rénovation'); // S: Appel utilitaire | R: Titre principal | W: Modifie le texte du header pour l'utilisateur.
      setActiveMenu(1); // S: Appel utilitaire | R: Navigation sidebar | W: Surligne le menu "Types" (index 1) dans la barre latérale.
      this.adjustLayout(); // S: Appel méthode interne | R: Optimisation mise en page | W: Réorganise les conteneurs pour une vue focalisée sur les types.
    } // S: Fin du bloc conditionnel

    this.renderStats(data.types, config); // S: Appel de rendu | R: Production visuelle | W: Passe les données de types à la fonction de génération de graphiques.
  }, // S: Fin de init

  adjustLayout() {
    // S: Méthode utilitaire | R: Modification structurelle DOM | W: Masque les zones dédiées aux bâtiments pour ne laisser que les conteneurs réutilisés pour les types.
    // Modify UI Structure for singular chart view
    const socialChart = document.getElementById('socialChart'); // S: Sélection ID | R: Cible graphique social | W: Identifie l'élément à retirer du flux visuel.
    if (socialChart) socialChart.parentElement.style.display = 'none'; // S: Manipulation CSS | R: Masquage | W: Cache le bloc parent pour aérer l'interface.

    const socialDonut = document.getElementById('socialDonut'); // S: Sélection ID | R: Cible donut social | W: Recherche l'élément inutile.
    if (socialDonut) socialDonut.parentElement.parentElement.parentElement.style.display = 'none'; // S: Navigation DOM | R: Masquage complet | W: Retire tout le bloc complexe correspondant.
  }, // S: Fin de adjustLayout

  renderStats(data, config = {}) {
    // S: Méthode de rendu statistique | R: Génère graphiques et listes | W: Transforme les données, calcule les parts et instancie les instances ApexCharts.
    const ids = {
      // S: Mapping d'IDs | R: Identification des conteneurs | W: Détermine où injecter les graphiques selon le contexte d'appel.
      bar: config.bar || 'privateChart', // S: Fallback ID | R: ID but barres | W: Cible 'privateChart' par défaut s'il n'est pas spécifié.
      donut: config.donut || 'privateDonut', // S: Fallback ID | R: ID but donut | W: Cible 'privateDonut' par défaut.
      list: config.list || 'privateListContainer' // S: Fallback ID | R: ID but légende | W: Cible 'privateListContainer'.
    }; // S: Fin de l'objet ids

    // Process Data
    const typeItems = data.map((d, i) => ({
      // S: Méthode Array.map | R: Transformation métier -> graphique | W: Crée une liste d'objets compatibles avec les donuts et les listes.
      name: d.type, // S: Propriété | R: Nom du type de travaux | W: Ex: "Isolation", "Chauffage", etc.
      value: d.count, // S: Propriété | R: Volume de travaux | W: Valeur brute pour le graphique.
      percent: -1, // S: Init | R: Pourcentage par défaut | W: Calculé dynamiquement juste après.
      color: donutColors[i % donutColors.length] // S: Accès tableau avec modulo | R: Couleur segment | W: Attribue une couleur unique à chaque type de travaux.
    })); // S: Fin du map typeItems

    const total = typeItems.reduce((acc, curr) => acc + curr.value, 0); // S: Array.reduce | R: Calcul somme totale | W: Additionne tous les travaux pour la base de calcul du %.
    typeItems.forEach((item) => (item.percent = Math.round((item.value / total) * 100 * 10) / 10)); // S: Array.forEach | R: Calcul pourcentage | W: Met à jour chaque élément avec son ratio sur 100 (1 décimale).

    // Render Main Bar Chart - Reusing privateChart container
    const barData = typeItems.map((d) => ({ name: d.name, total: d.value, renovated: d.value })); // S: Transformation intermédiaire | R: Format barres | W: Adapte les données pour getBarOptions.

    if (document.querySelector(`#${ids.bar}`)) {
      // S: Sélecteur DOM | R: Test d'existence | W: Évite de lancer le rendu si le conteneur est absent.
      new ApexCharts( // S: Instanciation ApexCharts | R: Création objet graphique | W: Définit un graphique en barres pour les volumes de travaux.
        document.querySelector(`#${ids.bar}`), // S: Cible | R: Container | W: Identifie le lieu de rendu.
        getBarOptions(barData, 'Types de Rénovation (Volume)') // S: Helper config | R: Style barres | W: Applique la configuration visuelle.
      ).render(); // S: render() | R: Dessin graphique | W: Affiche physiquement les barres dans la page.
    } // S: Fin du bloc bar

    // Render Donut
    if (document.querySelector(`#${ids.donut}`)) {
      // S: Sélection DOM | R: Test | W: Sécurité de rendu.
      new ApexCharts( // S: Instanciation | R: Graphique circulaire | W: Permet de voir la répartition relative des travaux.
        document.querySelector(`#${ids.donut}`), // S: Cible | R: Container | W: Lieu de rendu.
        getDonutOptions(typeItems, 'TYPES') // S: Helper config | R: Style donut | W: Configure le cercle avec les données traitées.
      ).render(); // S: render() | R: Dessin | W: Affiche le donut dans le navigateur.
    } // S: Fin du bloc donut

    // Render List
    renderList(ids.list, typeItems); // S: Appel utilitaire | R: Génération légende | W: Construit le tableau HTML récapitulatif sous les graphiques.
  } // S: Fin de renderStats
}; // S: Fin de TypesController
