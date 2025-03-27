import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";
import CarPredictionForm from "../pages/CarPredictionForm";
import ProtectedRoute from "./ProtectedRoute";
import Prices from "../components/sections/Prices";
import AboutModelSection from "../pages/About";
import SignUp from "../components/auth/signUp";
import Settings from "../pages/Settings";


const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/prices" element={<Prices />} />
      <Route path="/signUp" element={<SignUp />} />
      <Route path="/about" element={<AboutModelSection />} />
      <Route path="/settings" element={<Settings />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/prediction" element={<CarPredictionForm />} />
        {/* Puedes agregar más rutas protegidas aquí */}
      </Route>
    </Routes>
  );
};

export default AppRoutes;
