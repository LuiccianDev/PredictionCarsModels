import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { CheckIcon } from "@heroicons/react/20/solid";

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

const tiers = [
  {
    name: "Básico",
    id: "tier-basic",
    href: "/register",
    priceMonthly: "$5",
    description:
      "Perfecto para usuarios individuales que quieren empezar a predecir precios de autos.",
    features: [
      "Hasta 10 predicciones mensuales",
      "Acceso a modelos básicos",
      "Histórico de predicciones",
      "Soporte por email",
    ],
    featured: false,
  },
  {
    name: "Profesional",
    id: "tier-pro",
    href: "/register",
    priceMonthly: "$10",
    description:
      "Ideal para concesionarios y vendedores profesionales de autos.",
    features: [
      "Predicciones ilimitadas",
      "Modelos avanzados de predicción",
      "Análisis de mercado",
      "Soporte prioritario",
      "Exportación de reportes",
    ],
    featured: true,
  },
  {
    name: "Empresarial",
    id: "tier-enterprise",
    href: "/register",
    priceMonthly: "$15",
    description:
      "Para grandes empresas automotrices y grupos de concesionarios.",
    features: [
      "Predicciones ilimitadas",
      "API dedicada",
      "Modelos personalizados",
      "Soporte 24/7",
      "Análisis avanzado de mercado",
      "Integración con CRM",
    ],
    featured: false,
  },
];

export default function Prices() {
  const { user } = useAuth();
  const navigate = useNavigate();

  // Maneja la acción del botón en cada plan
  const handlePlanClick = (tier) => {
    if (!user) {
      // Si NO está logueado, redirige a /login
      navigate("/login");
    } else {
      // Si SÍ está logueado, redirige a /subscribe (o donde manejes la suscripción)
      navigate(`/subscribe?plan=${tier.id}`);
    }
  };

  return (
    <div
      className="relative isolate bg-white px-6 py-24 sm:py-32 lg:px-8"
      id="precios"
    >
      <div
        aria-hidden="true"
        className="absolute inset-x-0 -top-3 -z-10 transform-gpu overflow-hidden px-36 blur-3xl"
      >
        <div
          style={{
            clipPath:
              "polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)",
          }}
          className="mx-auto aspect-1155/678 w-[72.1875rem] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30"
        />
      </div>

      <div className="mx-auto max-w-4xl text-center">
        <h2 className="text-base/7 font-semibold text-indigo-600">Precios</h2>
        <p className="mt-2 text-5xl font-semibold tracking-tight text-balance text-gray-900 sm:text-6xl">
          Elige el plan perfecto para ti
        </p>
      </div>
      <p className="mx-auto mt-6 max-w-2xl text-center text-lg font-medium text-pretty text-gray-600 sm:text-xl/8">
        Selecciona un plan accesible que incluya las mejores características
        para predecir precios de vehículos, analizar el mercado y tomar mejores
        decisiones de compra/venta.
      </p>

      <div className="mx-auto mt-16 grid max-w-lg grid-cols-1 items-center gap-y-6 sm:mt-20 sm:gap-y-0 lg:max-w-4xl lg:grid-cols-3">
        {tiers.map((tier) => (
          <div
            key={tier.id}
            className={classNames(
              "rounded-3xl p-8 ring-1 ring-gray-900/10 sm:p-10 transition-transform duration-300 ease-in-out hover:-translate-y-1 hover:shadow-2xl",
              tier.featured
                ? "relative bg-gray-900 shadow-2xl"
                : "bg-white/60 sm:mx-8 lg:mx-0"
            )}
          >
            <h3
              id={tier.id}
              className={classNames(
                tier.featured ? "text-indigo-400" : "text-indigo-600",
                "text-base/7 font-semibold"
              )}
            >
              {tier.name}
            </h3>
            <p className="mt-4 flex items-baseline gap-x-2">
              <span
                className={classNames(
                  tier.featured ? "text-white" : "text-gray-900",
                  "text-5xl font-semibold tracking-tight"
                )}
              >
                {tier.priceMonthly}
              </span>
              <span
                className={classNames(
                  tier.featured ? "text-gray-400" : "text-gray-500",
                  "text-base"
                )}
              >
                /mes
              </span>
            </p>
            <p
              className={classNames(
                tier.featured ? "text-gray-300" : "text-gray-600",
                "mt-6 text-base/7"
              )}
            >
              {tier.description}
            </p>
            <ul
              role="list"
              className={classNames(
                tier.featured ? "text-gray-300" : "text-gray-600",
                "mt-8 space-y-3 text-sm/6 sm:mt-10"
              )}
            >
              {tier.features.map((feature) => (
                <li key={feature} className="flex gap-x-3">
                  <CheckIcon
                    aria-hidden="true"
                    className={classNames(
                      tier.featured ? "text-indigo-400" : "text-indigo-600",
                      "h-6 w-5 flex-none"
                    )}
                  />
                  {feature}
                </li>
              ))}
            </ul>
            <button
              onClick={() => handlePlanClick(tier)}
              className={classNames(
                tier.featured
                  ? "bg-indigo-500 text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-indigo-500"
                  : "text-indigo-600 ring-1 ring-indigo-200 ring-inset hover:ring-indigo-300 focus-visible:outline-indigo-600",
                "mt-8 block w-full rounded-md px-3.5 py-2.5 text-center text-sm font-semibold focus-visible:outline-2 focus-visible:outline-offset-2 sm:mt-10"
              )}
            >
              {user ? "Elegir este plan" : "Iniciar Sesión"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
