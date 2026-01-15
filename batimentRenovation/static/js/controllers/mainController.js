/* 
Syntax: JavaScript ES6 orienté objet (Classes) et architecture par modules.
Role: Contrôleur frontal principal (Main Front Controller) qui orchestre l'expérience Single Page Application (SPA) du tableau de bord.
Workflow: Initialise l'application, vérifie l'authentification, récupère les données globales et pilote le rendu dynamique des différentes vues (Overview, Bâtiments, DPE, Types).
*/

// Main Front Controller - SPA Architecture with Integrated Filters
import { fetchDashboardData } from '../apiFetch.js'; // S: Importation nommée | R: Importe le service de données | W: Permet au contrôleur de demander les datasets JSON.
import { AuthService } from '../services/authService.js'; // S: Importation nommée | R: Importe le service de sécurité | W: Utilisé pour valider l'accès à la page au démarrage.
import { BuildingController } from './buildingController.js'; // S: Importation nommée | R: Importe le contrôleur Bâtiments | W: Délègue le rendu de la section bâtiment.
import { TypesController } from './typesController.js'; // S: Importation nommée | R: Importe le contrôleur Types | W: Délègue le rendu de la section travaux.
import { DpeController } from './dpeController.js'; // S: Importation nommée | R: Importe le contrôleur DPE | W: Délègue le rendu de la section énergétique.

class FrontController {
  // S: Déclaration de classe ES6 | R: Définit l'orchestrateur de l'application | W: Centralise la logique de navigation et d'initialisation.
  constructor() {
    // S: Méthode constructor | R: Initialise l'instance de la classe | W: Prépare les variables de stockage (propriétés de l'instance).
    this.data = null; // S: Assignation de propriété | R: Stockage local du dataset | W: Maintient les données en mémoire pour éviter de multiples fetch.
  } // S: Fin du constructeur

  async init() {
    // S: Méthode asynchrone | R: Point d'entrée de la logique métier | W: S'exécute au chargement du DOM pour construire la page.
    console.log('🚀 [SPA] Booting Single Page Dashboard'); // S: Log console | R: Signale le démarrage | W: Trace visuelle pour le débogage.

    try {
      // S: Bloc de protection | R: Gère les erreurs fatales | W: Capture les échecs de fetch ou d'authentification.
      if (!AuthService.isAuthenticated()) return; // S: Condition if | R: Vérifie le statut de connexion | W: Stoppe l'exécution si l'utilisateur n'est pas autorisé.

      this.data = await fetchDashboardData(); // S: Attribution avec await | R: Récupère les données JSON | W: Attend la réponse du service apiFetch avant de continuer.
      this.renderAll(); // S: Appel de méthode interne | R: Lance l'affichage global | W: Déclenche le rendu initial de tous les composants graphiques.
      this.setupNavigation(); // S: Appel de méthode interne | R: Active l'interactivité | W: Initialise les écouteurs d'événements sur la sidebar.

      // Default view
      this.switchView('overview'); // S: Appel de méthode avec string | R: Affiche la vue par défaut | W: Garantit que l'utilisateur voit l'aperçu global à l'arrivée.
    } catch (error) {
      // S: Bloc catch | R: Intercepte les exceptions | W: Journalise l'erreur pour analyse technique.
      console.error('❌ [FrontController] Failure:', error); // S: Log d'erreur console | R: Affiche le détail de l'échec | W: Aide à la résolution d'incidents.
    } // S: Fin du bloc try-catch
  } // S: Fin de la méthode init

  renderAll() {
    // S: Méthode de rendu | R: Agrège les sous-rendus | W: Appelle chaque contrôleur spécialisé pour peupler les graphiques.
    BuildingController.init(this.data, { isOverview: true }); // S: Méthode statique | R: Initialise la vue Bâtiments | W: Transmet les données en mode "aperçu".
    TypesController.init(this.data, {
      // S: Méthode statique + objet config | R: Initialise la vue Types | W: Configure les IDs de conteneurs pour le rendu.
      isOverview: true, // S: Propriété booléenne | R: Flag de mode | W: Indique un rendu partiel (aperçu).
      bar: 'typesBar', // S: Propriété string | R: ID conteneur barres | W: Cible l'élément HTML précis.
      donut: 'typesDonut', // S: String | R: ID conteneur donut | W: Cible l'élément HTML.
      list: 'typesList' // S: String | R: ID conteneur liste | W: Cible l'élément HTML.
    }); // S: Fin de l'appel config Types
    DpeController.init(this.data, {
      // S: Méthode statique + objet config | R: Initialise la vue DPE | W: Configure les IDs pour le rendu énergétique.
      isOverview: true, // S: Booléen | R: Mode aperçu | W: Active l'affichage condensé.
      bar: 'dpeBar', // S: String | R: ID barres | W: Cible HTML.
      donut: 'dpeDonut', // S: String | R: ID donut | W: Cible HTML.
      list: 'dpeList' // S: String | R: ID liste | W: Cible HTML.
    }); // S: Fin de l'appel config DPE
  } // S: Fin de renderAll

  setupNavigation() {
    // S: Méthode d'interaction | R: Gère les clics utilisateur | W: Connecte les boutons de la sidebar à la logique de changement de vue.
    // 1. Manage Sidebar Navigation & Accordions
    const sidebar = document.getElementById('sidebarNav'); // S: Sélection DOM | R: Cible la barre latérale | W: Point d'ancrage pour la délégation d'événements.

    sidebar.addEventListener('click', (e) => {
      // S: Écouteur d'événement | R: Détecte les clics (délégation) | W: Centralise la gestion des interactions sur un seul parent.
      const btn = e.target.closest('.accordion-btn, .nav-item'); // S: Méthode closest() | R: Identifie l'élément cliquable | W: Remonte la hiérarchie pour trouver le bouton, même si on clique sur l'icône.
      if (!btn) return; // S: Garde-fou (guard) | R: Ignore les clics hors boutons | W: Évite d'exécuter la logique sur du vide.

      e.preventDefault(); // S: Méthode Event | R: Bloque le comportement natif | W: Empêche le rechargement de la page lié aux balises <a>.
      const view = btn.getAttribute('data-view'); // S: Lecture d'attribut | R: Récupère la destination | W: Détermine quelle section afficher.

      if (view) {
        // S: Condition if | R: Vérifie si une vue est définie | W: Lance le switch de section si l'attribut est présent.
        this.switchView(view); // S: Appel Switch | R: Change l'onglet actif | W: Met à jour l'affichage principal.
        this.updateActiveStyles(btn); // S: Appel Style | R: Met à jour l'aspect visuel | W: Déplace le curseur "actif" sur le menu cliqué.
      } // S: Fin du bloc if view
    }); // S: Fin de l'écouteur click

    // 2. Manage Submenu Filtering (Mock functionality)
    document.querySelectorAll('.submenu-item').forEach((item) => {
      // S: Boucle sur sélection multiple | R: Initialise les filtres | W: Ajoute l'interactivité aux sous-menus (Années, Travaux...).
      item.addEventListener('click', (e) => {
        // S: Écouteur individuel | R: Gère le clic de filtrage | W: Pourrait déclencher un nouveau rendu filtré (simulation ici).
        e.preventDefault(); // S: Bloque navigation | R: Reste sur la page | W: Comportement attendu d'une SPA.
        // Visual toggle for filter
        item.parentElement // S: Navigation DOM ascendante | R: Cible le conteneur | W: Permet de réinitialiser les frères.
          .querySelectorAll('.submenu-item') // S: Sélection descendante | R: Trouve les autres items | W: Prépare le nettoyage de la sélection.
          .forEach((el) => el.classList.remove('selected')); // S: Boucle et suppression de classe | R: Efface l'état "sélectionné" | W: Nettoie visuellement le groupe de filtres.
        item.classList.add('selected'); // S: Ajout de classe | R: Marque l'élément actif | W: Met en évidence le filtre choisi par l'utilisateur.
        console.log(`🔍 [Filter] Applied: ${item.textContent}`); // S: Log console | R: Trace du filtre | W: Permet de vérifier que l'action est enregistrée.
      }); // S: Fin d'écouteur filtre
    }); // S: Fin de la boucle filters
  } // S: Fin de setupNavigation

  updateActiveStyles(activeBtn) {
    // S: Méthode utilitaire | R: Gère l'état visuel du menu | W: Désactive les anciens menus et active le nouveau avec ses sous-menus.
    // Reset all
    document.querySelectorAll('.nav-item, .accordion-btn').forEach((el) => {
      // S: Boucle sur boutons | R: Réinitialise l'état | W: Ferme les menus ouverts et retire les marques de sélection.
      el.classList.remove('active', 'open'); // S: Suppression de classes CSS | R: Nettoyage graphique | W: Remet tous les items à l'état neutre.
      const sub = el.nextElementSibling; // S: Navigation DOM | R: Trouve le sous-menu | W: Permet de manipuler la visibilité des listes enfants.
      if (sub && sub.classList.contains('submenu')) sub.classList.add('hidden'); // S: if + addClass | R: Cache les listes | W: Replie les accordéons.
    }); // S: Fin de boucle reset

    // Activate current
    activeBtn.classList.add('active'); // S: Ajout de classe | R: Marque le bouton cliqué | W: Change la couleur/style du menu sélectionné.
    if (activeBtn.classList.contains('accordion-btn')) {
      // S: Test de classe | R: Détecte un accordéon | W: Ouvre le dossier si c'est un menu à tiroirs.
      activeBtn.classList.add('open'); // S: Ajout classe | R: État ouvert | W: Prépare le déploiement visuel.
      const submenu = activeBtn.nextElementSibling; // S: Navigation DOM | R: Cible l'enfant | W: Permet d'afficher la liste correspondante.
      if (submenu) submenu.classList.remove('hidden'); // S: Retrait classe | R: Affiche le contenu | W: Déploie la liste des filtres sous le menu.
    } // S: Fin du bloc activation
  } // S: Fin de updateActiveStyles

  switchView(viewType) {
    // S: Méthode de routing interne | R: Bascule l'affichage des sections | W: Gère la visibilité des blocs HTML et met à jour les titres de l'en-tête.
    const sections = document.querySelectorAll('.view-section'); // S: Sélection de masse | R: Liste toutes les pages SPA | W: Permet de les masquer/afficher en bloc.
    const title = document.getElementById('viewTitle'); // S: Cible titre | R: En-tête principal | W: Zone de mise à jour textuelle.
    const subtitle = document.getElementById('viewSubtitle'); // S: Cible sous-titre | R: Description secondaire | W: Zone de mise à jour textuelle.

    if (viewType === 'overview') {
      // S: Structure conditionnelle | R: Cas "Vue Globale" | W: Affiche toutes les sections simultanément.
      sections.forEach((s) => (s.style.display = 'block')); // S: Boucle + style inline | R: Affiche tout | W: Rend visibles les 3 dashboards en même temps.
      title.textContent = 'Tableau de Bord Global'; // S: Texte | R: Titre général | W: Informe l'utilisateur du mode "Synthèse".
      subtitle.textContent = 'Synthèse Interactive'; // S: Texte | R: Sous-titre | W: Complète l'information.
    } else {
      // S: Clause else | R: Cas "Vue Spécifique" | W: Sélectionne une seule section à afficher.
      sections.forEach((s) => {
        // S: Boucle de filtrage | R: Masque les éléments non ciblés | W: Assure qu'une seule "page" est visible à la fois dans le conteneur principal.
        s.style.display = s.id === `section-${viewType}` ? 'block' : 'none'; // S: Opérateur ternaire | R: Visibilité sélective | W: Compare l'ID avec la cible demandée.
      }); // S: Fin boucle sections
      const labels = { batiment: 'Bâtiments', types: 'Types', dpe: 'DPE' }; // S: Objet de mapping | R: Traductions des IDs | W: Associe un joli texte à chaque identifiant technique.
      title.textContent = labels[viewType] || 'Détails'; // S: Assignation fallback | R: Mise à jour titre | W: Affiche le nom correspondant ou "Détails" par défaut.
      subtitle.textContent = 'Filtres actifs appliqués'; // S: Texte fixe | R: Sous-titre | W: Indique que la vue est filtrable.
    } // S: Fin du bloc conditionnel

    window.scrollTo({ top: 0, behavior: 'smooth' }); // S: API Window Scroll | R: Remonte au sommet | W: Améliore l'UX lors de la navigation SPA en évitant de rester en bas de page.
    setTimeout(() => window.dispatchEvent(new Event('resize')), 100); // S: setTimeout + Event Dispatch | R: Force le redimensionnement | W: Indispensable pour que ApexCharts recalcule sa taille après le changement de display:none à block.
  } // S: Fin de switchView
} // S: Fin de la classe FrontController

document.addEventListener('DOMContentLoaded', () => {
  // S: Écouteur système | R: Détecteur de chargement DOM | W: Point de lancement sécurisé de l'application JS.
  new FrontController().init(); // S: Instanciation et appel | R: Initialisation globale | W: Crée l'objet contrôleur et lance la procédure de démarrage (boot).
}); // S: Fin du script
