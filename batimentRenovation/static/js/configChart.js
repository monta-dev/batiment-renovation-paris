/* 
Syntax: JavaScript ES6 (objets de configuration, fonctions fléchées).
Role: Centralise la configuration visuelle et structurelle des graphiques ApexCharts utilisés dans le dashboard.
Workflow: Exporte des palettes de couleurs et des générateurs d'options (Barres, Donuts) pour garantir une apparence uniforme sur toutes les pages.
*/

// Configuration for ApexCharts and Visual Styles
export const donutColors = [
  // S: Exportation d'un tableau constant | R: Stocke une palette de couleurs hexadécimales | W: Utilisée par les graphiques Donut pour colorer chaque segment de manière unique.
  '#3B82F6', // S: Valeur string hexadécimale | R: Bleu primaire | W: Définit la couleur du premier segment.
  '#10B981', // S: Valeur string hexadécimale | R: Vert émeraude | W: Définit la couleur du second segment.
  '#F59E0B', // S: String hex | R: Terre d'ombre | W: Couleur de segment.
  '#EF4444', // S: String hex | R: Rouge corail | W: Couleur de segment.
  '#8B5CF6', // S: String hex | R: Violet | W: Couleur de segment.
  '#EC4899', // S: String hex | R: Rose | W: Couleur de segment.
  '#6366F1', // S: String hex | R: Indigo | W: Couleur de segment.
  '#14B8A6', // S: String hex | R: Teal | W: Couleur de segment.
  '#F97316', // S: String hex | R: Orange | W: Couleur de segment.
  '#06B6D4', // S: String hex | R: Cyan | W: Couleur de segment.
  '#84CC16', // S: String hex | R: Lime | W: Couleur de segment.
  '#D946EF', // S: String hex | R: Fuchsia | W: Couleur de segment.
  '#4F46E5', // S: String hex | R: Indigo foncé | W: Couleur de segment.
  '#0EA5E9', // S: String hex | R: Sky blue | W: Couleur de segment.
  '#2563EB', // S: String hex | R: Royal blue | W: Couleur de segment.
  '#065F46', // S: String hex | R: Vert forêt | W: Couleur de segment.
  '#991B1B', // S: String hex | R: Rouge foncé | W: Couleur de segment.
  '#7C3AED', // S: String hex | R: Violet vif | W: Couleur de segment.
  '#BE185D', // S: String hex | R: Rose foncé | W: Couleur de segment.
  '#4338CA' // S: String hex | R: Blue-Purple | W: Couleur de segment.
]; // S: Fin du tableau donutColors

export const getBarOptions = (data, title) => ({
  // S: Fonction fléchée exportée | R: Génère la config pour les graphiques en barres | W: Prend des données brutes et un titre pour produire un objet compatible ApexCharts.
  series: [
    // S: Propriété d'objet (tableau) | R: Définit les séries de données | W: Organise les valeurs en colonnes comparatives.
    {
      // S: Objet série | R: Représente le volume total | W: Affiche la barre de fond pour chaque catégorie.
      name: "L'ensemble des logements", // S: Propriété String | R: Libellé de la légende | W: Identifie la série dans le graphique.
      data: data.map((d) => d.total) // S: Méthode Array.map | R: Extrait les valeurs totales | W: Transforme le dataset en liste de nombres pour la série.
    }, // S: Fin de la première série
    {
      // S: Objet série | R: Représente les logements rénovés | W: Superpose la barre de rénovation sur la barre totale.
      name: 'Nombre de logements rénovés', // S: String | R: Libellé légende | W: Identifie la série.
      data: data.map((d) => d.renovated) // S: Array.map | R: Extrait les valeurs rénovées | W: Transforme le dataset en liste de nombres.
    } // S: Fin de la seconde série
  ], // S: Fin du tableau series
  chart: {
    // S: Objet de configuration graphique | R: Définit les paramètres techniques | W: Gère le type de graphique, la taille et les polices.
    type: 'bar', // S: Valeur string | R: Type de graphique | W: Indique à ApexCharts d'afficher des barres.
    height: 380, // S: Valeur numérique | R: Hauteur en pixels | W: Définit la dimension verticale du graphique.
    toolbar: { show: false }, // S: Objet | R: Désactive la barre d'outils | W: Épure l'interface utilisateur.
    background: 'transparent', // S: String | R: Fond transparent | W: Permet d'adopter le style Neumorphique du parent.
    fontFamily: 'Inter, sans-serif' // S: String | R: Police de caractères | W: Assure la cohérence typographique.
  }, // S: Fin de l'objet chart
  colors: ['#87CEEB', '#C4B5FD'], // S: Tableau de strings (Hex) | R: Couleurs des barres | W: Applique les teintes pastel aux deux séries.
  plotOptions: { bar: { horizontal: false, columnWidth: '12px', borderRadius: 4 } }, // S: Objet complexe | R: Style des barres | W: Gère l'orientation, la largeur et les coins arrondis.
  dataLabels: { enabled: false }, // S: Objet | R: Désactive les étiquettes de données | W: Évite de surcharger visuellement les barres.
  xaxis: {
    // S: Objet de config de l'axe X | R: Paramètre l'axe horizontal | W: Affiche les catégories (noms des arrondissements/types).
    categories: data.map((d) => d.name), // S: Array.map | R: Définit les labels | W: Récupère les noms pour les afficher sous chaque barre.
    axisBorder: { show: false }, // S: Objet | R: Cache la bordure de l'axe | W: Participe au design minimaliste.
    axisTicks: { show: false }, // S: Objet | R: Cache les graduations | W: Nettoie l'apparence de l'axe.
    labels: { style: { colors: '#94A3B8', fontSize: '10px', fontWeight: 600 } } // S: Objet | R: Style des textes | W: Rend les labels lisibles et grisés.
  }, // S: Fin de l'objet xaxis
  yaxis: { labels: { style: { colors: '#94A3B8', fontSize: '10px' } } }, // S: Objet | R: Style axe vertical | W: Affiche les échelles numériques de manière discrète.
  grid: { borderColor: 'rgba(0,0,0,0.05)', strokeDashArray: 4 }, // S: Objet | R: Style de la grille de fond | W: Dessine des lignes pointillées légères.
  legend: {
    // S: Objet de config de la légende | R: Paramètre la liste des séries | W: Positionne et stylise les indicateurs de couleur en bas.
    position: 'bottom', // S: String | R: Emplacement | W: Place la légende sous le graphique.
    horizontalAlign: 'center', // S: String | R: Alignement | W: Centre les éléments de légende.
    fontSize: '12px', // S: String | R: Taille texte | W: Standardise la lisibilité.
    fontWeight: 500, // S: Nombre | R: Graisse texte | W: Améliore le contraste.
    markers: { radius: 12, offsetX: -4 }, // S: Objet | R: Puces de légende | W: Crée des points de couleur circulaires.
    itemMargin: { horizontal: 20, vertical: 10 } // S: Objet | R: Marges | W: Espace les éléments pour éviter l'encombrement.
  }, // S: Fin de l'objet legend
  title: { text: title, align: 'left', style: { fontSize: '14px', color: '#64748B' } } // S: Objet titre | R: Libellé du graphique | W: Affiche le nom transmis en argument en haut à gauche.
}); // S: Fin de la fonction getBarOptions

export const getDonutOptions = (data, centerLabel) => ({
  // S: Fonction fléchée exportée | R: Génère la config pour les graphiques Donut | W: Transforme les données circulaires pour ApexCharts.
  series: data.map((d) => d.value), // S: Array.map | R: Valeurs numériques | W: Définit la part de chaque segment du donut.
  chart: { type: 'donut', height: 350 }, // S: Objet | R: Type de graphique | W: Définit la forme circulaire évidée à 350px de haut.
  labels: data.map((d) => d.name), // S: Array.map | R: Noms des segments | W: Associe un nom à chaque valeur pour les infobulles.
  colors: donutColors, // S: Référence au tableau constant | R: Palette de couleurs | W: Réutilise les couleurs définies en haut du fichier.
  dataLabels: { enabled: false }, // S: Objet | R: Désactive les labels internes | W: Garde le centre du donut dégagé.
  legend: { show: false }, // S: Objet | R: Masque la légende native | W: On utilise une liste personnalisée dans le DOM (`ui.js`).
  stroke: { show: true, width: 4, colors: ['#fff'] }, // S: Objet | R: Bordure des segments | W: Ajoute un espacement blanc de 4px entre les parts.
  plotOptions: {
    // S: Objet complexe | R: Paramètres de rendu | W: Gère la forme spécifique du donut.
    pie: { donut: { size: '65%', background: 'transparent' } } // S: Objet | R: Taille du trou | W: Définit l'épaisseur de l'anneau à 65%.
  }, // S: Fin de plotOptions
  tooltip: { y: { formatter: (val) => val.toLocaleString() } } // S: Objet | R: Formatage info-bulle | W: Formate les nombres avec des séparateurs de milliers lors du survol.
}); // S: Fin de la fonction getDonutOptions
