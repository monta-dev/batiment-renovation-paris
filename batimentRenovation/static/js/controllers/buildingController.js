/* 
Syntax: JavaScript ES6 (objets littéraux, méthodes, déstructuration).
Role: Contrôleur spécialisé dans le traitement et l'affichage des données de rénovation par type de bâtiment (Privé vs Social).
Workflow: Transforme les données brutes issues de l'API Fetch en formats compatibles avec ApexCharts et met à jour les éléments DOM du tableau de bord.
*/

import { getBarOptions, getDonutOptions, donutColors } from '../configChart.js'; // S: Importations nommées | R: Importe les utilitaires de graphiques | W: Permet la création uniforme des visuels ApexCharts.
import { renderList, updatePageTitle, setActiveMenu } from '../utils/ui.js'; // S: Importations nommées | R: Importe les utilitaires UI | W: Gère la manipulation DOM transverse.

export const BuildingController = {
  // S: Exportation d'un objet littéral | R: Namespace pour la logique "Bâtiment" | W: Regroupe toutes les fonctions liées à cette thématique.
  /**
   * Initializes the Building Dashboard view.
   * @param {Object} data - The full dataset (we'll extract buildings).
   */
  init(data, config = {}) {
    // S: Méthode d'objet avec paramètres par défaut | R: Prépare la vue | W: Configure l'interface et lance le rendu des statistiques.
    console.log('🏗️ [BuildingController] Initializing...'); // S: Log console | R: Trace d'activité | W: Indique le lancement du contrôleur dans la console.

    // 1. Set Headings & Menu (only if not in dashboard overview)
    if (!config.isOverview) {
      // S: Structure conditionnelle | R: Test de mode d'affichage | W: Applique les titres uniquement en mode "vue détaillée".
      updatePageTitle('Bâtiments Rénovés'); // S: Appel de fonction utilitaire | R: Change le H1 | W: Informe l'utilisateur qu'il consulte les bâtiments.
      setActiveMenu(0); // S: Appel avec entier | R: Surligne le menu | W: Indique visuellement dans la sidebar que la section 0 est active.
    } // S: Fin du bloc conditionnel

    // 2. Render content
    this.renderStats(data.buildings, config); // S: Appel de méthode interne | R: Déclenche l'affichage | W: Transmet les données de bâtiments pour le rendu graphique.
  }, // S: Fin de init

  renderStats(data, config = {}) {
    // S: Méthode de rendu | R: Construit les graphiques | W: Mappe les IDs, transforme les données et instancie les instances ApexCharts.
    const ids = {
      // S: Déclaration d'objet constant | R: Mapping d'IDs HTML | W: Permet de cibler les bons conteneurs selon le mode (Overview ou Détail).
      privateBar: config.privateBar || 'privateChart', // S: Opérateur de repli (OR) | R: ID barre privée | W: Flexible selon le paramétrage.
      socialBar: config.socialBar || 'socialChart', // S: OR | R: ID barre sociale | W: Flexible.
      privateDonut: config.privateDonut || 'privateDonut', // S: OR | R: ID donut privé | W: Flexible.
      socialDonut: config.socialDonut || 'socialDonut', // S: OR | R: ID donut social | W: Flexible.
      privateList: config.privateList || 'privateListContainer', // S: OR | R: ID liste privée | W: Flexible.
      socialList: config.socialList || 'socialListContainer' // S: OR | R: ID liste sociale | W: Flexible.
    }; // S: Fin de l'objet ids

    // Transform DTO to Chart format
    const privateData = data.map((d) => ({
      // S: Méthode Array.map | R: Projection de données | W: Convertit les objets métier en structures pour les barres privées.
      name: d.name, // S: Propriété | R: Nom de l'arrondissement | W: Utilisé pour l'axe X.
      total: d.total, // S: Propriété | R: Volume total de logements | W: Définit la barre de fond.
      renovated: d.private_renovated // S: Propriété | R: Volume rénové privé | W: Définit la barre de progression.
    })); // S: Fin du map privateData

    const socialData = data.map((d) => ({
      // S: Méthode Array.map | R: Projection de données | W: Convertit les objets métier pour les barres sociales.
      name: d.name, // S: Propriété | R: Nom | W: Libellé axe X.
      total: d.total * 0.4, // S: Calcul (40% du total) | R: Estimation volume social | W: Simule une partie de logements sociaux.
      renovated: d.social_renovated // S: Propriété | R: Volume rénové social | W: Définit la barre de progression sociale.
    })); // S: Fin du map socialData

    // Render Bar Charts
    if (document.querySelector(`#${ids.privateBar}`)) {
      // S: Sélecteur DOM | R: Test d'existence | W: Évite les erreurs si l'élément n'est pas dans la page.
      new ApexCharts( // S: Instanciation de classe | R: Crée le graphique | W: Initialise un objet ApexCharts avec les options barres.
        document.querySelector(`#${ids.privateBar}`), // S: Cible DOM | R: Zone de rendu | W: Identifie où dessiner le graphique.
        getBarOptions(privateData, 'Logement Privé') // S: Helper config | R: Fournit les options | W: Applique le style barre au dataset privé.
      ).render(); // S: Méthode render() | R: Affichage final | W: Dessine physiquement le graphique dans le navigateur.
    } // S: Fin du bloc bar privé

    if (document.querySelector(`#${ids.socialBar}`)) {
      // S: Sélecteur DOM | R: Test d'existence | W: Sécurité de rendu.
      new ApexCharts( // S: Instanciation | R: Crée le graphique | W: Prépare les barres sociales.
        document.querySelector(`#${ids.socialBar}`), // S: Cible DOM | R: Zone de rendu | W: Identifie le conteneur social.
        getBarOptions(socialData, 'Logement Social') // S: Helper config | R: Fournit les options | W: Applique le style barre au dataset social.
      ).render(); // S: Méthode render() | R: Affichage final | W: Exécute le dessin du graphique.
    } // S: Fin du bloc bar social

    // Prepare & Render Donut Data
    const generatePieData = (
      dataset // S: Fonction fléchée interne | R: Transformateur spécifique | W: Calcule les pourcentages et assigne des couleurs aux segments du donut.
    ) =>
      dataset.map((d, i) => ({
        // S: Méthode map avec index | R: Enrichissement de données | W: Prépare chaque part du donut.
        name: d.name, // S: Propriété | R: Nom segment | W: Nom de l'arrondissement.
        value: d.renovated, // S: Propriété | R: Valeur numérique | W: Volume absolu pour le calcul de la part.
        // S: Calcul mathématique complexe | R: Part en % | W: Calcule la valeur relative par rapport à la somme totale.
        percent:
          Math.round((d.renovated / dataset.reduce((a, b) => a + b.renovated, 0)) * 100 * 10) / 10, // S: reduce + round | R: Ratio arrondi | W: Garantit un affichage propre à une décimale.
        color: donutColors[i % 20] // S: Modulo sur palette | R: Assignation couleur | W: Cycle à travers les 20 couleurs définies.
      })); // S: Fin du map donut

    const pieDataPrivate = generatePieData(privateData); // S: Appel fonction transformation | R: Données donut privé | W: Résultats prêts pour ApexCharts.
    const pieDataSocial = generatePieData(socialData); // S: Appel fonction transformation | R: Données donut social | W: Résultats prêts pour ApexCharts.

    if (document.querySelector(`#${ids.privateDonut}`)) {
      // S: Sélecteur DOM | R: Test de présence | W: Sécurise l'instanciation.
      new ApexCharts( // S: Instanciation | R: Objet Donut | W: Prépare le cercle privé.
        document.querySelector(`#${ids.privateDonut}`), // S: Cible | R: Container | W: Lieu d'insertion.
        getDonutOptions(pieDataPrivate, 'PRIVÉ') // S: Helper config | R: Options cercle | W: Configure le donut avec les données calculées.
      ).render(); // S: render() | R: Dessin | W: Affiche le donut privé.
    } // S: Fin donut privé

    if (document.querySelector(`#${ids.socialDonut}`)) {
      // S: Sélecteur | R: Test | W: Sécurité.
      new ApexCharts( // S: Instanciation | R: Objet Donut | W: Prépare le cercle social.
        document.querySelector(`#${ids.socialDonut}`), // S: Cible | R: Container | W: Lieu d'insertion.
        getDonutOptions(pieDataSocial, 'SOCIAL') // S: Helper config | R: Options cercle | W: Configure le donut social.
      ).render(); // S: render() | R: Dessin | W: Affiche le donut social.
    } // S: Fin donut social

    // Render Lists
    renderList(ids.privateList, pieDataPrivate.slice(0, 20)); // S: Appel utilitaire | R: Affiche la légende | W: Génère le tableau HTML pour les 20 arrondissements privés.
    renderList(ids.socialList, pieDataSocial.slice(0, 20)); // S: Appel utilitaire | R: Affiche la légende | W: Génère le tableau HTML pour les 20 arrondissements sociaux.
  } // S: Fin de renderStats
}; // S: Fin de BuildingController
