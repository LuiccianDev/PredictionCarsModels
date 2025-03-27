import api from "./api"; // Asegúrate de que api.js esté configurado correctamente

const PredictionService = {
  predictAndSave: async (modelName, userId, predictionData, token) => {
    try {
      const response = await api.post(`/predict/save/${modelName}/${userId}`, predictionData, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });
      // Se asume que la respuesta contiene el campo "prediction" con los datos guardados, como "precio_estimado"
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || "Error al procesar la predicción"
      };
    }
  }
};

export default PredictionService;
