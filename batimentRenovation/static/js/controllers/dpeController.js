/* 
Syntax: JavaScript ES6.
Role: Contrôleur dédié à la visualisation de la performance énergétique (DPE) des bâtiments parisiens.
Workflow: Cartographie les données DPE, applique les codes couleurs officiels (A à G) et génère les graphiques de répartition correspondants.
*/

import { getBarOptions, getDonutOptions } from '../configChart.js'; // S: Imports nommés | R: Accès aux helpers ApexCharts | W: Assure la cohérence des styles graphiques avec le reste de l'app.
import { renderList, updatePageTitle, setActiveMenu } from '../utils/ui.js'; // S: Imports nommés | R: Utilitaires DOM | W: Permet de modifier le titre et le menu de navigation.

export const DpeController = {
  // S: Objet exporté | R: Namespace DPE | W: Encapsule toute la logique de traitement énergétique.
  /**
   * Initializes the DPE Dashboard view.
   * @param {Object} data
   */
  init(data, config = {}) {
    // S: Méthode d'initialisation | R: Prépare l'affichage DPE | W: Configure l'interface spécifique et lance le rendu des statistiques.
    console.log('📊 [DpeController] Initializing...'); // S: Log console | R: Trace de démarrage | W: Informe le développeur de l'activation du contrôleur.

    if (!config.isOverview) {
      // S: Condition if | R: Vérification du contexte | W: Si on est en vue détaillée, on ajuste l'en-tête et les menus.
      updatePageTitle('Classe DPE'); // S: Appel utilitaire | R: Titre de page | W: Affiche "Classe DPE" dans le header.
      setActiveMenu(2); // S: Appel avec entier | R: Navigation sidebar | W: Active l'élément DPE (index 2) dans le menu.
      this.adjustLayout(); // S: Appel méthode interne | R: Nettoyage UI | W: Cache les éléments inutiles (ex: sections sociales) pour cette vue.
    } // S: Fin du bloc conditionnel

    this.renderStats(data.dpe, config); // S: Appel méthode de rendu | R: Affiche les données | W: Transmet les statistiques DPE au moteur de rendu graphique.
  }, // S: Fin de init

  adjustLayout() {
    // S: Méthode de nettoyage | R: Adapte le DOM | W: Masque les conteneurs de graphiques sociaux qui ne sont pas pertinents pour le DPE.
    const socialChart = document.getElementById('socialChart'); // S: Sélection ID | R: Cible graphique social | W: Permet de manipuler sa visibilité.
    if (socialChart) socialChart.parentElement.style.display = 'none'; // S: Manipulation style | R: Cache le bloc parent | W: Libère de l'espace visuel dans le dashboard.

    const socialDonut = document.getElementById('socialDonut'); // S: Sélection ID | R: Cible donut social | W: Recherche l'élément à masquer.
    if (socialDonut) socialDonut.parentElement.parentElement.parentElement.style.display = 'none'; // S: Navigation DOM ascendante | R: Masque le bloc complexe | W: Épure la mise en page.
  }, // S: Fin de adjustLayout

  renderStats(data, config = {}) {
    // S: Méthode de rendu statistique | R: Génère les visuels | W: Mappe les couleurs DPE, calcule les parts et instancie les graphiques.
    const ids = {
      // S: Objet constant | R: Mapping conteneurs | W: Définit où les graphiques doivent être injectés (overview vs détail).
      bar: config.bar || 'privateChart', // S: fallback ID | R: Cible barres | W: Utilise 'privateChart' par défaut.
      donut: config.donut || 'privateDonut', // S: fallback ID | R: Cible donut | W: Utilise 'privateDonut' par défaut.
      list: config.list || 'privateListContainer' // S: fallback ID | R: Cible légende | W: Utilise 'privateListContainer' par défaut.
    }; // S: Fin de l'objet ids

    // DPE Colors Mapping
    const dpeColorsMap = {
      // S: Objet de mapping | R: Palette officielle DPE | W: Associe chaque classe (A-G) à sa couleur réglementaire.
      A: '#009036', // S: Hex | R: Vert foncé | W: Couleur classe A.
      B: '#53af31', // S: Hex | R: Vert clair | W: Couleur classe B.
      C: '#c6d802', // S: Hex | R: Jaune-vert | W: Couleur classe C.
      D: '#f5e700', // S: Hex | R: Jaune | W: Couleur classe D.
      E: '#fbad18', // S: Hex | R: Orange clair | W: Couleur classe E.
      F: '#ec661e', // S: Hex | R: Orange foncé | W: Couleur classe F.
      G: '#e31d2b' // S: Hex | R: Rouge | W: Couleur classe G.
    }; // S: Fin du mapping couleurs

    const dpeItems = data.map((d) => ({
      // S: Méthode Array.map | R: Transformation de données | W: Prépare les objets pour ApexCharts avec noms, valeurs et couleurs.
      name: `Classe ${d.class}`, // S: Template string | R: Libellé | W: "Classe A", "Classe B", etc.
      value: d.count, // S: Propriété | R: Nombre de bâtiments | W: Valeur brute pour le volume.
      percent: -1, // S: Initialisation | R: Pourcentage vide | W: Sera calculé à l'étape suivante.
      color: dpeColorsMap[d.class] || '#ccc' // S: Accès dynamique | R: Couleur segment | W: Récupère la teinte via le map (fallback gris).
    })); // S: Fin du map dpeItems

    const total = dpeItems.reduce((acc, curr) => acc + curr.value, 0); // S: Array.reduce | R: Calcul du total | W: Additionne tous les bâtiments pour le calcul du %.
    dpeItems.forEach((item) => (item.percent = Math.round((item.value / total) * 100 * 10) / 10)); // S: Array.forEach + Math | R: Calcul % relatif | W: Met à jour chaque item avec sa part du gâteau (1 décimale).

    // Render Bar
    const barData = dpeItems.map((d) => ({ name: d.name, total: d.value, renovated: d.value })); // S: Transformation | R: Data barres simples | W: Adapté pour getBarOptions.

    if (document.querySelector(`#${ids.bar}`)) {
      // S: Sélecteur DOM | R: Test d'existence | W: Sécurise l'affichage.
      new ApexCharts( // S: Instanciation | R: Graphique Barres | W: Dessine le volume par classe énergétique.
        document.querySelector(`#${ids.bar}`), // S: Cible | R: Container | W: Lieu de rendu.
        getBarOptions(barData, 'Répartition DPE') // S: Helper config | R: Options barres | W: Stylise les barres DPE.
      ).render(); // S: render() | R: Affichage | W: Exécute le dessin.
    } // S: Fin bloc bar

    // Render Donut
    const dpeDonutOptions = getDonutOptions(dpeItems, 'DPE'); // S: Helper config | R: Options donut | W: Récupère la base de config circulaire.
    dpeDonutOptions.colors = dpeItems.map((d) => d.color); // S: Surcharge de propriété | R: Force les couleurs | W: Applique les couleurs A-G au lieu de la palette globale.

    if (document.querySelector(`#${ids.donut}`)) {
      // S: Sécurisation | R: Test DOM | W: Évite les erreurs null.
      new ApexCharts(document.querySelector(`#${ids.donut}`), dpeDonutOptions).render(); // S: Instanciation + render | R: Graphique Donut | W: Affiche le cercle chromatique DPE.
    } // S: Fin bloc donut

    renderList(ids.list, dpeItems); // S: Appel utilitaire | R: Légende textuelle | W: Génère la liste détaillée A-G sous les graphiques.
  } // S: Fin de renderStats
}; // S: Fin de DpeController
