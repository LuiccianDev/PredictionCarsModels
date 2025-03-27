import api from "./api"; // Importa la configuración de Axios

const AuthService = {
  // 🟢 Iniciar sesión
  login: async (email, password) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(`/auth/login`, formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        withCredentials: true, // Permitir cookies (para refresh_token)
      });
      
      // Supongamos que la respuesta incluye { access_token, user }
      const userData = {
        id: response.data.user ,// Asegúrate de que el backend devuelva user_id
        token: response.data.access_token,
      };
    
      // Guarda el objeto usuario en sessionStorage
      sessionStorage.setItem("user", JSON.stringify(userData));
      return response.data;
    } catch (error) {
      console.error("Error en login:", error);
      throw error;
    }
  },

  // 🟢 Renovar el token de acceso
  refreshToken: async () => {
    try {
      const response = await api.post(`/auth/refresh`, {}, { withCredentials: true });
      // Actualizar solo el token dentro del objeto usuario
      const storedUser = JSON.parse(sessionStorage.getItem("user"));
      if (storedUser) {
        storedUser.token = response.data.access_token;
        sessionStorage.setItem("user", JSON.stringify(storedUser));
      }
      return response.data;
    } catch (error) {
      console.error("Error al refrescar el token:", error);
      throw error;
    }
  },

  // 🟢 Cerrar sesión
  logout: async () => {
    try {
      await api.post(`/auth/logout`, {}, { withCredentials: true });
      sessionStorage.removeItem("user");
    } catch (error) {
      console.error("Error en logout:", error);
      throw error;
    }
  },

  // 🟢 Obtener el usuario actual
  getCurrentUser: () => {
    return JSON.parse(sessionStorage.getItem("user"));
  },
};

export default AuthService;



/* import api from "./api"; // Importa la configuración de Axios


const AuthService = {
  // 🟢 Iniciar sesión
  login: async (email, password) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(`/auth/login`, formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        withCredentials: true, // Permitir cookies (para refresh_token)
      });
      
      localStorage.setItem("token", response.data.access_token);
      return response.data;
    } catch (error) {
      console.error("Error en login:", error);
      throw error;
    }
  },

  // 🟢 Renovar el token de acceso
  refreshToken: async () => {
    try {
      const response = await api.post(`auth/refresh`, {}, { withCredentials: true });
      localStorage.setItem("token", response.data.access_token);
      return response.data;
    } catch (error) {
      console.error("Error al refrescar el token:", error);
      throw error;
    }
  },

  // 🟢 Cerrar sesión
  logout: async () => {
    try {
      await api.post(`/auth/logout`, {}, { withCredentials: true });
      localStorage.removeItem("token");
    } catch (error) {
      console.error("Error en logout:", error);
      throw error;
    }
  },

  // 🟢 Obtener el token actual
  getAccessToken: () => {
    return localStorage.getItem("token");
  },
};

export default AuthService;
 */