import api from "./api"; // Importa la configuración de Axios

const UserService = {
  // 🔹 Registrar un usuario
  register: async (userData) => {
    try {
      const response = await api.post("/users/register", {
        email: userData.email,
        password: userData.password,
        username: userData.userName,  // Se envía como username lo que corresponde al nombre
                                        // Incluye el apellido si es requerido en el backend
      });
      // Retornamos un objeto indicando éxito y los datos recibidos
      return { success: true, data: response.data };
    } catch (error) {
      // En lugar de lanzar un error, retornamos un objeto con success: false y el mensaje de error
      return { 
        success: false, 
        error: error.response?.data?.detail || "Error al registrar usuario" 
      };
    }
  },

  // 🔹 Obtener usuario por ID
  getUser: async (userId) => {
    try {
      const response = await api.get(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || "Error al obtener usuario";
    }
  },

  // 🔹 Actualizar usuario
  updateUser: async (userId, userData) => {
    try {
      const response = await api.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || "Error al actualizar usuario";
    }
  },

  // 🔹 Eliminar usuario
  deleteUser: async (userId) => {
    try {
      const response = await api.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || "Error al eliminar usuario";
    }
  },
};

export default UserService;
