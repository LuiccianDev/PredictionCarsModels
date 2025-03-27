import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Dialog } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { useAuth } from "../context/AuthContext";
import AuthService from "../services/AuthServices";
import { useTheme } from "../context/ThemeContext";
// import CarImagen from "../../public/car_logo.png"
const navigation = [
  { name: "Inicio", href: "/" },
  { name: "Predicción", href: "/prediction" },
  { name: "Precios", href: "/prices" },
  { name: "Acerca de", href: "/about" },
  { name: "Configuarciones", href: "/settings" },
];

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const { darkMode } = useTheme();
  const navigate = useNavigate();

  const isAuthenticated = Boolean(user && user.token);

  const handleLogout = async () => {
    await AuthService.logout();
    logout();
    navigate("/login");
  };

  return (
    <header className={`w-full z-50 shadow-sm font-Roboto ${darkMode ? " bg-[#09122C] text-white" : "bg-gradient-to-r from-blue-500 to-purple-500 text-white"}`} >
    {/* "w-full z-50 shadow-sm dark:bg-gradient-to-r from-blue-500 to-purple-500 dark:text-white bg-gray-900 " */ }
      <nav className="container mx-auto flex items-center justify-between p-4 lg:px-8" aria-label="Global">
        <div className="flex flex-1">
          <Link to="/" className="p-1">
            {/* <img className="w-12 h-12"
            src={CarImagen} alt="Logo de l prediciojde de preciode d e caroro " 
            /> */}
            <span className="text-2xl font-bold  ">CarPredict</span>
          </Link>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            className="p-2 "
            onClick={() => setMobileMenuOpen(true)}
          >
            <span className="sr-only">Abrir menú principal</span>
            <Bars3Icon className="h-6 w-6n" aria-hidden="true" />
          </button>
        </div>
        <div className="hidden lg:flex space-x-8">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className="text-sm font-semibold "
            >
              {item.name}
            </Link>
          ))}
        </div>
        <div className="hidden lg:flex flex-1 justify-end">
          {isAuthenticated ? (
            <button onClick={handleLogout} className="text-sm font-semibold ">
              Cerrar sesión <span aria-hidden="true">&rarr;</span>
            </button>
          ) : (
            <Link to="/login" className="text-sm font-semibold ">
              Iniciar sesión <span aria-hidden="true">&rarr;</span>
            </Link>
          )}
        </div>
      </nav>

      {/* Menú móvil */}
      <Dialog as="div" className="lg:hidden" open={mobileMenuOpen} onClose={setMobileMenuOpen}>
        <div className="fixed inset-0 z-10" />
        <Dialog.Panel className="fixed inset-y-0 right-0 z-10 w-full max-w-sm bg-white p-6 overflow-y-auto">
          <div className="flex items-center justify-between">
            <Link to="/" className="p-1">
              <span className="text-2xl font-bold text-indigo-600">CarPredict</span>
            </Link>
            <button
              type="button"
              className="p-2 text-gray-700"
              onClick={() => setMobileMenuOpen(false)}
            >
              <span className="sr-only">Cerrar menú</span>
              <XMarkIcon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div className="mt-6">
            <div className="space-y-4">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className="block rounded px-3 py-2 text-base font-semibold text-gray-900 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </div>
            <div className="mt-4">
              {isAuthenticated ? (
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full text-left rounded px-3 py-2 text-base font-semibold text-red-600 hover:bg-gray-50"
                >
                  Cerrar sesión
                </button>
              ) : (
                <Link
                  to="/login"
                  className="block rounded px-3 py-2 text-base font-semibold text-gray-900 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Iniciar sesión
                </Link>
              )}
            </div>
          </div>
        </Dialog.Panel>
      </Dialog>
    </header>
  );
}

