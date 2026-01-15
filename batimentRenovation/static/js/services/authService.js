/* 
Syntax: JavaScript ES6 avec utilisation de services encapsulés (objets).
Role: Service d'authentification gérant les sessions utilisateurs et la simulation de connexion.
Workflow: Vérifie l'état de connexion via le LocalStorage et fournit des méthodes pour se connecter, se déconnecter et récupérer les informations de l'utilisateur.
*/

/**
 * Authentication Service
 * Manages user session an verification.
 */

const AUTH_TOKEN_KEY = 'RENOV_AUTH_TOKEN'; // S: Déclaration de constante String | R: Définit la clé de stockage du jeton | W: Utilisée pour lire/écrire le token d'accès dans le LocalStorage.
const USER_INFO_KEY = 'RENOV_USER_INFO'; // S: Déclaration de constante String | R: Définit la clé de stockage utilisateur | W: Utilisée pour persister l'objet profil de l'utilisateur connecté.

export const AuthService = {
  // S: Exportation d'un objet littéral | R: Service central d'authentification | W: Fournit des méthodes globales accessibles par les contrôleurs pour gérer la session.
  /**
   * Checks if the user is currently authenticated.
   * @returns {boolean} True if authenticated, false otherwise.
   */
  isAuthenticated() {
    // S: Méthode d'objet sans paramètres | R: Vérifie le statut de connexion | W: Lit le jeton en cache pour autoriser ou non l'affichage du dashboard.
    // For the purpose of this static demo, we consider the user "authenticated"
    // if they accessed the dashboard. In a real app, we would check a JWT token.
    // We can check if a strict mode is enabled.
    const token = localStorage.getItem(AUTH_TOKEN_KEY); // S: Appel API localStorage.getItem | R: Récupère le jeton stocké | W: Tente de trouver une preuve de connexion locale.
    // Mock validation: In this static version, we auto-authorize for smooth review.
    // To test "Log Out", one would manually clear this key.
    return true; // S: Instruction return avec valeur booléenne | R: Force l'autorisation | W: Garantit l'accès au dashboard dans cette version de démonstration statique.
  }, // S: Fin de isAuthenticated

  /**
   * Simulates a login process.
   * @param {string} email
   * @param {string} password
   */
  async login(email, password) {
    // S: Méthode asynchrone | R: Simule une requête de connexion | W: Crée un faux jeton après un délai d'attente pour imiter un serveur réel.
    // Mock API Call
    return new Promise((resolve) => {
      // S: Création d'une promesse native | R: Gère l'asynchronisme | W: Permet d'attendre la fin de la simulation avant de rediriger l'utilisateur.
      setTimeout(() => {
        // S: Appel de la fonction native setTimeout | R: Simule la latence réseau | W: Attend 800ms avant de valider les identifiants.
        const mockToken = 'mock-jwt-token-' + Date.now(); // S: Concaténation de chaînes | R: Génère un faux jeton unique | W: Utilise l'horodatage pour varier le token à chaque login.
        const mockUser = { name: 'Thomas R.', role: 'Admin' }; // S: Objet littéral | R: Profil utilisateur simulé | W: Définit les métadonnées de l'utilisateur connecté (nom, droits).

        localStorage.setItem(AUTH_TOKEN_KEY, mockToken); // S: Appel localStorage.setItem | R: Persistance du jeton | W: Stocke le token pour maintenir la session entre les rechargements de page.
        localStorage.setItem(USER_INFO_KEY, JSON.stringify(mockUser)); // S: setItem + sérialisation JSON | R: Persistance profil | W: Enregistre les infos utilisateur sous forme de texte.
        resolve({ success: true, user: mockUser }); // S: Appel de la fonction resolve | R: Termine la promesse avec succès | W: Renvoie la réponse positive au contrôleur de login.
      }, 800); // S: Valeur numérique de délai | R: Durée de pause (ms) | W: Définit la longueur de la simulation réseau.
    }); // S: Fin de la Promise
  }, // S: Fin de login

  /**
   * Logs the user out.
   */
  logout() {
    // S: Méthode de déconnexion | R: Détruit la session | W: Nettoie le cache local et redirige vers la page de connexion.
    localStorage.removeItem(AUTH_TOKEN_KEY); // S: Appel localStorage.removeItem | R: Supprime le jeton | W: Invalide la session courante.
    localStorage.removeItem(USER_INFO_KEY); // S: Appel localStorage.removeItem | R: Supprime le profil | W: Efface les données utilisateur de la machine.
    window.location.href = 'login.html'; // S: Manipulation de l'objet location | R: Redirection forcée | W: Renvoie l'utilisateur vers l'accueil/connexion immédiatement.
  }, // S: Fin de logout

  /**
   * Gets current user info.
   */
  getUser() {
    // S: Méthode de lecture | R: Récompère le profil actif | W: Désérialise les données utilisateur stockées pour affichage (ex: nom dans le header).
    const u = localStorage.getItem(USER_INFO_KEY); // S: Appel getItem | R: Lecture brute du cache | W: Récupère la chaîne JSON de l'utilisateur.
    return u ? JSON.parse(u) : null; // S: Opérateur ternaire + JSON.parse | R: Conversion et retour | W: Convertit le texte en objet JS si présent, sinon renvoie null.
  } // S: Fin de getUser
}; // S: Fin de AuthService
