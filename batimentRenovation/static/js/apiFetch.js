/* 
Syntax: JavaScript ES6 utilisant les modules (export), les fonctions asynchrones (async/await) et l'API Storage (localStorage).
Role: Service de récupération des données (Data Fetching) avec une stratégie de mise en cache pour optimiser les performances.
Workflow: Vérifie d'abord la validité d'un cache local. Si absent ou expiré, il récupère les fichiers JSON via des requêtes réseau simultanées (Promise.allSettled) et rafraîchit le cache.
*/

// Data Fetching Service with Caching Strategy
const CACHE_KEY = 'RENOVATION_DASHBOARD_DATA'; // S: Constante de type String | R: Définit la clé unique pour le LocalStorage | W: Sert d'identifiant pour stocker et récupérer les données mises en cache.
const CACHE_DURATION = 2 * 60 * 60 * 1000; // S: Expression arithmétique (2h en ms) | R: Définit la durée de vie du cache | W: Utilisée pour comparer l'âge du cache avec l'heure actuelle.
const apiBatimentRenovates = 'http://127.0.0.1:8000/api/Batiment_renovates/';
/**
 * Fetches all necessary dashboard data from distinct sources.
 * Uses LocalStorage for caching to minimize network requests.
 * @param {boolean} forceRefresh - If true, ignores cache and fetches fresh data.
 * @returns {Promise<Object>} Object containing all datasets (buildings, types, dpe).
 */
export async function fetchDashboardData(forceRefresh = false) {
  // S: Exportation de fonction asynchrone | R: Point d'entrée pour obtenir les données | W: Orchestre la vérification du cache puis l'appel réseau si nécessaire.
  console.log(`🚀 [apiFetch] Requesting Data... (Force Refresh: ${forceRefresh})`); // S: Appel de méthode console.log | R: Affiche le statut de la requête dans la console | W: Aide au débogage en indiquant si un rafraîchissement forcé est actif.

  // 1. Check Cache
  if (!forceRefresh) {
    // S: Structure conditionnelle | R: Vérifie si on ne force pas le rafraîchissement | W: Si faux, on tente de lire le cache avant de faire un appel réseau.
    const cached = localStorage.getItem(CACHE_KEY); // S: Appel d'API Web LocalStorage | R: Récupère la chaîne JSON stockée sous la clé CACHE_KEY | W: Première étape de la récupération des données locales.
    if (cached) {
      // S: Test de vérité sur la variable cached | R: Vérifie si des données existent en cache | W: Si présent, on passe à l'analyse de la date d'expiration.
      try {
        // S: Bloc de gestion d'erreurs | R: Sécurise le parsing JSON | W: Prévient le plantage de l'app si le cache est corrompu.
        const { timestamp, data } = JSON.parse(cached); // S: Destructuration d'objet et JSON.parse | R: Extrait le timestamp et les données | W: Transforme la chaîne stockée en objet utilisable.
        const now = Date.now(); // S: Appel de méthode statique Date.now() | R: Capture l'heure actuelle en millisecondes | W: Base de comparaison pour l'expiration.
        if (now - timestamp < CACHE_DURATION) {
          // S: Comparaison temporelle | R: Vérifie si le cache a moins de 2 heures | W: Si valide, renvoie immédiatement les données sans appel réseau.
          console.log('✅ [apiFetch] Returning valid CACHED data'); // S: Journalisation console | R: Confirme l'utilisation du cache | W: Information visuelle pour le développeur.
          return data; // S: Instruction return | R: Renvoie les données mises en cache | W: Termine l'exécution de la fonction avec succès.
        } else {
          // S: Clause else | R: Gère le cas d'un cache expiré | W: Indique que le cache ne doit plus être utilisé.
          console.log('⚠️ [apiFetch] Cache expired'); // S: Journalisation console | R: Signale l'expiration | W: Informe que l'étape suivante sera la récupération réseau.
        }
      } catch (e) {
        // S: Capture d'exception | R: Gère les échecs de lecture | W: En cas d'erreur JSON, on passe à la récupération réseau par sécurité.
        console.warn('⚠️ [apiFetch] Cache corrupted, fetching fresh data'); // S: Avertissement console | R: Signale un cache défectueux | W: Informe l'utilisateur (dev) de la corruption.
      }
    }
  }

  // 2. Fetch from Network
  console.log('🌐 [apiFetch] Fetching from network...'); // S: Journalisation console | R: Indique le lancement du fetch | W: Informe que le cache était absent ou invalide.

  // Récupération des URLs depuis la configuration globale
  debugger;
    const urls = window.DATA_URLS || {
      buildings: apiBatimentRenovates,
      types: '/static/data/stats_types.json',
      dpe: '/static/data/stats_dpe.json',
    };

  // We use Promise.allSettled to ensure that if one fails, others can still proceed.
  const results = await Promise.allSettled([
    // S: Appel asynchrone Promise.allSettled | R: Lance 3 requêtes en parallèle | W: Attend que toutes les promesses soient terminées (succès ou échec).
    fetch(urls.buildings).then(
      (
        r // S: Appel Fetch | R: Récupère les stats bâtiments | W: Transforme la réponse en JSON si OK.
      ) => (r.ok ? r.json() : Promise.reject('Components Error')) // S: Opérateur ternaire | R: Valide la réponse HTTP | W: Rejette en cas d'erreur 404 ou 500.
    ), // S: Fin du premier élément du tableau
    fetch(urls.types).then((r) => (r.ok ? r.json() : Promise.reject('Types Error'))), // S: Fetch pour les types de travaux | R: Récupère le JSON des types | W: Logique identique au premier fetch.
    fetch(urls.dpe).then((r) => (r.ok ? r.json() : Promise.reject('DPE Error'))) // S: Fetch pour le DPE | R: Récupère le JSON DPE | W: Logique identique.
  ]); // S: Fin du tableau et de Promise.allSettled

  // 3. Process Results
  const [buildingsResult, typesResult, dpeResult] = results; // S: Destructuration de tableau | R: Isole les résultats des 3 promesses | W: Permet une manipulation individuelle simplifiée.

  const finalData = {
    // S: Création d'un objet littéral | R: Structure finale des données | W: Regroupe les 3 sources en un seul objet cohérent.
    buildings: buildingsResult.status === 'fulfilled' ? buildingsResult.value : [], // S: Opérateur conditionnel | R: Récupère la valeur ou un tableau vide | W: Sécurise l'objet final contre les échecs réseau partiels.
    types: typesResult.status === 'fulfilled' ? typesResult.value : [], // S: Logique identique pour les types | R: Valorise la propriété types | W: Assure une structure d'objet prévisible.
    dpe: dpeResult.status === 'fulfilled' ? dpeResult.value : [] // S: Logique identique pour le DPE | R: Valorise la propriété dpe | W: Complète l'objet final.
  }; // S: Fin de l'objet finalData

  // Log failures if any
  if (buildingsResult.status === 'rejected') console.error('❌ Failed to fetch Buildings data'); // S: Condition if | R: Log d'erreur spécifique | W: Notifie l'échec du chargement des bâtiments.
  if (typesResult.status === 'rejected') console.error('❌ Failed to fetch Types data'); // S: Condition if | R: Log d'erreur spécifique | W: Notifie l'échec du chargement des types.
  if (dpeResult.status === 'rejected') console.error('❌ Failed to fetch DPE data'); // S: Condition if | R: Log d'erreur spécifique | W: Notifie l'échec du chargement du DPE.

  // 4. Save to Cache (only if we have at least some data)
  if (finalData.buildings.length || finalData.types.length || finalData.dpe.length) {
    // S: Condition complexe OR | R: Vérifie la présence de données | W: Prévient la mise en cache d'un objet vide en cas d'échec total.
    try {
      // S: Bloc try-catch | R: Sécurise l'écriture disque | W: Prévient les erreurs si le LocalStorage est plein.
      const cacheObject = {
        // S: Création d'objet | R: Prépare le paquet de cache | W: Associe les données au timestamp de création.
        timestamp: Date.now(), // S: Horodatage | R: Définit l'heure de sauvegarde | W: Utilisé ultérieurement pour calculer l'expiration.
        data: finalData // S: Propriété data | R: Contient l'objet complet | W: Stocke les données récupérées.
      }; // S: Fin de cacheObject
      localStorage.setItem(CACHE_KEY, JSON.stringify(cacheObject)); // S: setItem et JSON.stringify | R: Sauvegarde physique en cache | W: Convertit l'objet en texte pour le stockage persistant.
      console.log('💾 [apiFetch] Data saved to cache'); // S: Log de succès | R: Confirme la persistance | W: Trace visuelle de la mise à jour du cache.
    } catch (e) {
      // S: Capture d'erreur | R: Gère les exceptions de quota | W: Log l'erreur sans bloquer l'application.
      console.error('❌ [apiFetch] Failed to save to localStorage (Quota exceeded?)', e); // S: Log d'erreur | R: Détaille l'échec de cache | W: Aide au diagnostic technique.
    }
  }

  return finalData; // S: Instruction return | R: Renvoie l'objet final | W: Fournit les données prêtes à l'emploi au contrôleur appelant.
} // S: Fin de la fonction fetchDashboardData
