/* 
Syntax: JavaScript ES6 (manipulation pure du DOM, clones de nodes, modèles de chaînes de caractères).
Role: Bibliothèque d'utilitaires UI partagés par tous les contrôleurs du tableau de bord.
Workflow: Centralise les fonctions répétitives comme la mise à jour des titres de page, la gestion des menus accordéons et le rendu des listes de légendes.
*/

/**
 * UI Utility Functions
 * Handles DOM manipulations shared across controllers.
 */

/**
 * Updates the main page title (h1 in header).
 * @param {string} title - The new title to display.
 */
export function updatePageTitle(title) {
  // S: Exportation de fonction nommée | R: Modifie l'en-tête de la page | W: Sélectionne la balise H1 et met à jour son contenu textuel dynamiquement.
  const titleEl = document.querySelector('header h1'); // S: Appel querySelector | R: Cible l'élément titre | W: Recherche le H1 dans le header pour la modification.
  if (titleEl) titleEl.textContent = title; // S: Condition if + assignation textContent | R: Mise à jour sécurisée | W: Change le texte affiché si l'élément existe bien dans le DOM.
} // S: Fin de updatePageTitle

/**
 * Hides sidebar sections that do not match the current page type.
 * @param {string} pageType - The active page identifier ('batiment', 'types', 'dpe').
 */
export function setSidebarVisibility(pageType) {
  // S: Fonction exportée | R: Masquage sélectif du menu | W: Parcourt les sections de la sidebar pour n'afficher que celle correspondant au contexte.
  const sections = document.querySelectorAll('.accordion-section'); // S: querySelectorAll | R: Liste des blocs menus | W: Récupère tous les accordéons pour filtrage.

  // If we are on the global dashboard, show everything
  if (pageType === 'dashboard') {
    // S: Comparaison de string | R: Cas vue globale | W: Affiche toutes les options de navigation si l'utilisateur est sur l'accueil.
    sections.forEach((s) => (s.style.display = 'block')); // S: Boucle forEach | R: Affichage total | W: Rétablit la visibilité de chaque menu.
    return; // S: Sortie de fonction | R: Fin procédure | W: Évite d'exécuter la logique de masquage suivante.
  } // S: Fin bloc dashboard

  sections.forEach((section, index) => {
    // S: Boucle itérative avec index | R: Filtrage individuel | W: Compare chaque menu avec le type de page demandé.
    // Logic: 0=Batiments, 1=Types, 2=DPE
    const typeIndexMap = {
      // S: Objet littéral | R: Dictionnaire de correspondance | W: Associe un nom technique à l'index physique du menu dans le HTML.
      batiment: 0, // S: Propriété | R: Index bâtiments | W: Lien vers le 1er accordéon.
      types: 1, // S: Propriété | R: Index types | W: Lien vers le 2ème accordéon.
      dpe: 2 // S: Propriété | R: Index DPE | W: Lien vers le 3ème accordéon.
    }; // S: Fin de typeIndexMap

    const targetIndex = typeIndexMap[pageType]; // S: Accès dynamique par clé | R: Détermination de la cible | W: Identifie le seul menu qui doit rester visible.

    if (index !== targetIndex && targetIndex !== undefined) {
      // S: Condition d'exclusion | R: Masquage des intrus | W: Cache toutes les sections sauf celle qui correspond à targetIndex.
      section.style.display = 'none'; // S: Style en ligne | R: Disparition | W: Rend la section invisible et retire sa place dans le layout.
    } else {
      // S: Clause alternative | R: Affichage de l'élue | W: Force la visibilité de la section active.
      section.style.display = 'block'; // S: Style en ligne | R: Apparition | W: Affiche la section.
    } // S: Fin condition logic
  }); // S: Fin de boucle sections
} // S: Fin de setSidebarVisibility

/**
 * Expands the active menu item and its submenu.
 * @param {number} index - Index of the menu item to activate.
 */
export function setActiveMenu(index) {
  // S: Fonction exportée | R: Ouvre un accordéon par défaut | W: Manipule les classes CSS pour déplier le menu correspondant à l'index reçu.
  const sections = document.querySelectorAll('.accordion-section'); // S: Sélection multiple | R: Liste des sections | W: Accès aux éléments de navigation.
  sections.forEach((section, i) => {
    // S: Itération | R: Traitement unitaire | W: Recherche le menu à l'index spécifique.
    const btn = section.querySelector('.accordion-btn'); // S: querySelector interne | R: Cible le bouton | W: Permet d'ajouter la classe 'open'.
    const submenu = section.querySelector('.submenu'); // S: querySelector interne | R: Cible la liste enfant | W: Permet de retirer la classe 'hidden'.
    const chevron = btn?.querySelector('.material-symbols-outlined:last-child'); // S: Optionnal chaining | R: Cible l'icône flèche | W: Permet d'appliquer la rotation de l'icône.

    if (i === index) {
      // S: Comparaison d'index | R: Identification de la cible | W: Si l'index correspond, on déclenche l'ouverture.
      btn?.classList.add('open'); // S: Ajout de classe | R: État visuel ouvert | W: Change l'apparence du bouton.
      submenu?.classList.remove('hidden'); // S: Retrait de classe | R: Déploiement menu | W: Rend la sous-liste visible.
      chevron?.classList.add('rotate-180'); // S: Ajout de classe | R: Rotation icône | W: Oriente la flèche vers le haut.
    } // S: Fin transition menu
  }); // S: Fin boucle sections
} // S: Fin de setActiveMenu

/**
 * Renders a list of items with colored dots (legend style).
 * @param {string} containerId - The ID of the container element.
 * @param {Array} data - Array of objects {name, percent, color}.
 */
export function renderList(containerId, data) {
  // S: Fonction exportée | R: Génère des légendes HTML | W: Prend des données traitées et crée une structure en deux colonnes de légendes colorées.
  const container = document.getElementById(containerId); // S: getElementById | R: Conteneur de destination | W: Point d'insertion du HTML généré.
  if (!container) return; // S: Guard | R: Sécurité DOM | W: Évite les crashs si le conteneur est absent sur une page donnée.

  container.innerHTML = ''; // S: Remise à zéro | R: Nettoyage | W: Vide la liste précédente avant de re-dessiner.
  const mid = Math.ceil(data.length / 2); // S: Calcul mathématique (arrondi sup) | R: Point de coupe | W: Détermine la séparation pour l'affichage en deux colonnes équilibrées.
  const col1 = data.slice(0, mid); // S: Array.slice | R: Première colonne | W: Prend la première moitié des données.
  const col2 = data.slice(mid); // S: Array.slice | R: Seconde colonne | W: Prend le reste des données.

  const createCol = (items) => {
    // S: Fonction fléchée interne | R: Usine à colonnes | W: Génère une balise div contenant le HTML pour une liste d'éléments.
    const col = document.createElement('div'); // S: createElement | R: Balise conteneur | W: Crée le parent de la colonne.
    col.className = 'list-column'; // S: Propriété className | R: Style CSS | W: Applique le layout flexbox défini en CSS.
    items.forEach((item) => {
      // S: Boucle sur items | R: Remplissage HTML | W: Construit chaque ligne de légende dynamiquement.
      col.innerHTML += `
                  <div class="list-row">
                      <div class="dot" style="background-color: ${item.color};"></div>
                      <div class="row-content">
                          <span class="row-name">${item.name}</span>
                          <span class="row-percent">${item.percent}%</span>
                      </div>
                  </div>
              `; // S: Template literal multi-ligne | R: Gabarit HTML | W: Injecte les classes, couleurs et textes de chaque arrondissement/type.
    }); // S: Fin boucle items
    return col; // S: Retour d'élément DOM | R: Objet prêt | W: Fournit la colonne construite à la fonction parente.
  }; // S: Fin createCol

  container.appendChild(createCol(col1)); // S: appendChild | R: Insertion DOM | W: Ajoute la colonne gauche au conteneur principal.
  container.appendChild(createCol(col2)); // S: appendChild | R: Insertion DOM | W: Ajoute la colonne droite.
} // S: Fin de renderList

/**
 * Initializes accordion interactions.
 */
export function initInteractions() {
  // S: Fonction exportée | R: Active les clics JS | W: Branche des écouteurs d'événements sur tous les accordéons pour gérer l'ouverture/fermeture manuelle.
  document.querySelectorAll('.accordion-btn').forEach((btn) => {
    // S: querySelectorAll + itération | R: Liste les boutons | W: Parcours tous les boutons menus du document.
    // Remove existing listeners to avoid duplicates if re-init (though usually called once)
    const newBtn = btn.cloneNode(true); // S: cloneNode(true) | R: Copie propre d'élément | W: Technique pour supprimer tous les écouteurs précédents en remplaçant l'élément.
    btn.parentNode.replaceChild(newBtn, btn); // S: replaceChild | R: Remplacement DOM | W: Enlève l'ancien bouton rattaché et insère le nouveau clone vierge d'événements.

    newBtn.addEventListener('click', () => {
      // S: addEventListener | R: Détecteur de clic | W: Déclenche la bascule (toggle) de l'accordéon au clic.
      const section = newBtn.parentElement; // S: Navigation parente | R: Bloc accordéon | W: Utile pour cibler le contexte.
      const submenu = newBtn.nextElementSibling; // S: nextElementSibling | R: Sous-menu | W: Identifie la liste à afficher ou masquer.
      const chevron = newBtn.querySelector('.material-symbols-outlined:last-child'); // S: querySelector | R: Flèche d'état | W: Récupère l'icône pour l'animation de rotation.
      if (submenu) {
        // S: Test existence | R: Sécurité | W: Vérifie que le bouton possède bien un menu enfant rattaché.
        const isOpen = !submenu.classList.contains('hidden'); // S: contains class | R: Lecture état actuel | W: Détermine si le menu est déjà ouvert ou non.
        submenu.classList.toggle('hidden', isOpen); // S: toggle class | R: Inversion visibilité | W: Ajoute 'hidden' si ouvert, le retire si fermé.
        chevron.classList.toggle('rotate-180', !isOpen); // S: toggle class | R: Inversion rotation | W: Fait pivoter la flèche selon le nouvel état.
        newBtn.classList.toggle('open', !isOpen); // S: toggle class | R: Inversion état bouton | W: Applique le style 'open' (relief inversé) au bouton.
      } // S: Fin interaction logic
    }); // S: Fin écouteur click
  }); // S: Fin boucle accordion-btn
} // S: Fin de initInteractions
