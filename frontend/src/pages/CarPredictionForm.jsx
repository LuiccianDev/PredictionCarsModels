import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import PredictionService from "../services/PredictionServices";
import { toast } from "react-toastify";
import PredictionCard from "../components/prediction/PredictionCar"
import InputField from "../components/prediction/InputField";
import SelectField from "../components/prediction/SelectField";
import EncryptButton from "../components/Butoon/EncryptButton";


const INITIAL_FORM_DATA = {
  brand: "",
  model: "",
  year: "",
  engineSize: "",
  fuelType: "Hybrid",
  transmission: "Manual",
  mileage: "",
  doors: "",
  ownerCount: "",
  selectedModel: "model1",
  predictedResult: null,
};

const CarPredictionForm = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);

  const [predictedModel, setPredictedModel] = useState(null);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const clearResult = () => {
    setFormData((prev) => ({ ...prev, predictedResult: null }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Validación de campos obligatorios
    const {
      brand,
      model,
      year,
      engineSize,
      fuelType,
      transmission,
      mileage,
      doors,
      ownerCount,
      selectedModel,
    } = formData;

    if (
      !brand ||
      !model ||
      !year ||
      !engineSize ||
      !fuelType ||
      !transmission ||
      !mileage ||
      !doors ||
      !ownerCount ||
      !selectedModel
    ) {
      setError("Todos los campos son obligatorios.");
      setLoading(false);
      return;
    }

    // Construcción de datos para la predicción
    const predictionData = {
      Brand: brand,
      Model: model,
      Year: parseInt(year),
      Engine_Size: parseFloat(engineSize),
      Fuel_Type: fuelType,
      Transmission: transmission,
      Mileage: parseInt(mileage),
      Doors: parseInt(doors),
      Owner_Count: parseInt(ownerCount),
    };

    try {
      const response = await PredictionService.predictAndSave(
        selectedModel,
        user.id,
        predictionData,
        user.token
      );
      if (response.success) {
        setPredictedModel(selectedModel);
        setFormData((prev) => ({
          ...prev,
          predictedResult: response.data.prediction,
        }));
        toast.success("Predicción procesada exitosamente!", {
          position: "top-right",
          autoClose: 2000,
        });
      } else {
        setError(response.error || "Error al procesar la predicción");
        toast.error(response.error || "Error al procesar la predicción", {
          position: "top-right",
        });
      }
    } catch (err) {
      setError("Error al conectar con el servidor");
      toast.error("Error al conectar con el servidor", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-200 flex items-center justify-center px-6 bg-gray-50">
      {/* Contenedor dinámico: al inicio es solo el formulario, luego se expande */}
      <div className={`flex flex-col md:flex-row items-center gap-6 transition-all duration-300 ${formData.predictedResult ? "md:items-start" : ""}`}>
        {/* Formulario centrado */}
        <div className="bg-white p-8 shadow-md rounded-lg w-full max-w-lg">
          <h2 className="text-center text-2xl font-bold text-gray-900 mb-6">
            Predicción de Precio de Vehículo
          </h2>

          {error && (
            <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <form className="grid grid-cols-1 md:grid-cols-2 gap-4" onSubmit={handleSubmit}>
            <InputField label="Marca" name="brand" value={formData.brand} onChange={handleChange} />
            <InputField label="Modelo" name="model" value={formData.model} onChange={handleChange} />
            <InputField label="Año" name="year" type="number" value={formData.year} onChange={handleChange} />
            <InputField label="Tamaño del Motor" name="engineSize" type="number" value={formData.engineSize} onChange={handleChange} />
            <InputField label="Kilometraje" name="mileage" type="number" value={formData.mileage} onChange={handleChange} />
            <InputField label="Número de Puertas" name="doors" type="number" value={formData.doors} onChange={handleChange} />
            <InputField label="Número de Dueños" name="ownerCount" type="number" value={formData.ownerCount} onChange={handleChange} />
            <SelectField
              label="Tipo de Modelo"
              name="selectedModel"
              value={formData.selectedModel}
              onChange={handleChange}
              options={[
                { value: "model1", label: "Model 1" },
                { value: "model2", label: "Model 2" },
                { value: "model3", label: "Model 3" },
              ]}
            />
            {/* <div className="md:col-span-2 mt-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 px-4 bg-indigo-600 text-white font-semibold rounded-md shadow-md hover:bg-indigo-700 disabled:opacity-50"
              >
                {loading ? "Calculando..." : "Calcular Precio"}
              </button>
            </div> */}
            {/* Reemplazamos el botón normal por EncryptButton con type=\"submit\" */}
            <div className="md:col-span-2 mt-4">
              <EncryptButton
                text={loading ? "Calculando..." : "Calcular Precio"}
                // Al ser type=\"submit\", presionar Enter o clic dispara onSubmit
                type="submit"
                disabled={loading}
              />
            </div>
          </form>
        </div>

        {/* Tarjeta de Predicción (Aparece solo si hay resultado) */}
        {formData.predictedResult && (
          <div className="w-full max-w-md">
            <PredictionCard
              model={predictedModel}
              prediction={formData.predictedResult}
              onClose={clearResult}
            />
          </div>
        )}
      </div>
    </div>
  );

};

export default CarPredictionForm;


