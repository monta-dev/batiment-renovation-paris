/**
 * Authentication Service
 * Manages user session an verification.
 */

const AUTH_TOKEN_KEY = 'RENOV_AUTH_TOKEN';
const USER_INFO_KEY = 'RENOV_USER_INFO';

export const AuthService = {
    /**
     * Checks if the user is currently authenticated.
     * @returns {boolean} True if authenticated, false otherwise.
     */
    isAuthenticated() {
        // For the purpose of this static demo, we consider the user "authenticated"
        // if they accessed the dashboard. In a real app, we would check a JWT token.
        // We can check if a strict mode is enabled.
        const token = localStorage.getItem(AUTH_TOKEN_KEY);
        // Mock validation: In this static version, we auto-authorize for smooth review.
        // To test "Log Out", one would manually clear this key.
        return true; 
    },

    /**
     * Simulates a login process.
     * @param {string} email 
     * @param {string} password 
     */
    async login(email, password) {
        // Mock API Call
        return new Promise((resolve) => {
            setTimeout(() => {
                const mockToken = 'mock-jwt-token-' + Date.now();
                const mockUser = { name: 'Thomas R.', role: 'Admin' };
                
                localStorage.setItem(AUTH_TOKEN_KEY, mockToken);
                localStorage.setItem(USER_INFO_KEY, JSON.stringify(mockUser));
                resolve({ success: true, user: mockUser });
            }, 800);
        });
    },

    /**
     * Logs the user out.
     */
    logout() {
        localStorage.removeItem(AUTH_TOKEN_KEY);
        localStorage.removeItem(USER_INFO_KEY);
        window.location.href = 'login.html';
    },

    /**
     * Gets current user info.
     */
    getUser() {
        const u = localStorage.getItem(USER_INFO_KEY);
        return u ? JSON.parse(u) : null;
    }
};
