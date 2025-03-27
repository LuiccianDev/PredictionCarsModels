import { motion } from "framer-motion";
import { FiMoon, FiSun } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext"; // Asegúrate de que esta ruta es correcta

const SliderToggle = () => {
  const { darkMode, setDarkMode } = useTheme(); // Accede al estado global del tema

  const handleToggle = () => {
    setDarkMode((prevMode) => !prevMode); // Alterna entre dark y light
  };

  return (
    <div 
      className="relative flex w-fit items-center rounded-full bg-slate-100 p-1.5 cursor-pointer"
      onClick={handleToggle} // Permite hacer click en cualquier parte del toggle
    >
      <button
        className={`flex items-center gap-2 px-4 py-2 transition-colors ${
          !darkMode ? "text-white" : "text-slate-600"
        }`}
      >
        <FiSun className="text-lg" />
        <span>Light</span>
      </button>
      
      <button
        className={`flex items-center gap-2 px-4 py-2 transition-colors ${
          darkMode ? "text-white" : "text-slate-600"
        }`}
      >
        <FiMoon className="text-lg" />
        <span>Dark</span>
      </button>

      {/* Indicador animado */}
      <motion.span
        layout
        transition={{ type: "spring", damping: 15, stiffness: 250 }}
        className={`absolute inset-0 z-0 flex ${
          darkMode ? "justify-end" : "justify-start"
        }`}
      >
        <motion.span
          layout
          className="h-full w-1/2 rounded-full bg-gradient-to-r from-violet-600 to-indigo-600"
        />
      </motion.span>
    </div>
  );
};

export default SliderToggle;
