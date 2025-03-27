import React from 'react'

/**
 * Sección "About" para describir el modelo de predicción
 */
export default function AboutModelSection() {
  return (
    <section id="about-model" className="bg-white py-12 sm:py-16 px-6">
      <div className="mx-auto max-w-7xl">
        <h2 className="text-center text-3xl font-bold text-gray-900">
          ¿Cómo Funciona Nuestro Modelo de Predicción?
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-gray-600">
          Nuestro sistema utiliza un avanzado modelo de inteligencia artificial
          para analizar múltiples factores y brindar estimaciones precisas del valor
          de un vehículo. Con esta tecnología, puedes tomar mejores decisiones al
          momento de comprar o vender un auto.
        </p>

        {/* Características principales */}
        <div className="mx-auto mt-10 max-w-4xl">
          <h3 className="text-xl font-semibold text-gray-900 mb-3">
            Principales Ventajas:
          </h3>
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            <li>
              <strong>Modelos de IA entrenados</strong> con miles de datos históricos de vehículos.
            </li>
            <li>
              <strong>Factores clave</strong> como marca, modelo, kilometraje, año y estado del auto.
            </li>
            <li>
              <strong>Comparación con precios de mercado</strong> en tiempo real.
            </li>
            <li>
              <strong>Mejora continua</strong> a medida que recopilamos más información y afinamos el modelo.
            </li>
          </ul>
        </div>

        {/* Modo de uso */}
        <div className="mx-auto mt-10 max-w-4xl">
          <h3 className="text-xl font-semibold text-gray-900 mb-3">
            ¿Cómo usarlo?
          </h3>
          <p className="text-gray-600">
            Solo necesitas ingresar algunos datos básicos de tu vehículo (marca, modelo, año, etc.) 
            y nuestro modelo se encargará de analizar la información para ofrecerte una estimación 
            precisa del valor del auto. ¡Es rápido y sencillo!
          </p>
        </div>
      </div>
    </section>
  )
}
