import React from "react";

const MODELS = {
  model1: "Modelo de Precios",
  model2: "Modelo de Segmentación",
  model3: "Modelo de Clustering",
};

const PredictionCard = ({ model, prediction, onClose }) => {
  // Si el modelo está en el objeto MODELS, lo usamos; de lo contrario, mostramos el valor original
  const modelName = MODELS[model] || model;

  return (
    <div className="bg-white rounded-lg shadow p-6 relative">
      {/* Botón para cerrar la card (opcional) */}
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        >
          X
        </button>
      )}

      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Resultado de Predicción
      </h2>

      <p className="text-gray-600">
        Modelo utilizado:{" "}
        <span className="font-semibold">{modelName}</span>
      </p>

      {/* Si la predicción es un número, se muestra directamente; si es un objeto, se recorren sus propiedades */}
      {typeof prediction === "number" ? (
        <p className="mt-2 text-gray-600">
          Precio estimado:{" "}
          <span className="font-semibold">${prediction.toLocaleString()}</span>
        </p>
      ) : (
        <div className="mt-2">
          {Object.entries(prediction).map(([key, value]) => (
            <p key={key} className="text-gray-600">
              {key}: <span className="font-semibold">{value}</span>
            </p>
          ))}
        </div>
      )}
    </div>
  );
};

export default PredictionCard;

