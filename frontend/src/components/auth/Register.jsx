import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import UserService from "../../services/UserServices";
import { toast } from "react-toastify";
import EncryptButton from "../Butoon/EncryptButton";
const InputField = ({ label, type, name, value, onChange }) => {
  const autoCompleteType =
    name === "password" || name === "confirmPassword"
      ? "new-password"
      : name === "email"
      ? "email"
      : "off";

  return (
    <div className="w-full">
      <label className="sr-only">{label}</label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        required
        autoComplete={autoCompleteType}
        className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 bg-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder={label}
      />
    </div>
  );
};

const Register = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    userName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    
    const { userName, email, password, confirmPassword } = formData;

    if (!userName || !email || !password || !confirmPassword) {
      setError("Todos los campos son obligatorios.");
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden.");
      setLoading(false);
      return;
    }

    try {
      const response = await UserService.register({ userName, email, password });
      if (response.success) {
        toast.success("¡Cuenta creada exitosamente! Redirigiendo al login...", { position: "top-right", autoClose: 3000 });
        setTimeout(() => navigate("/login"), 3000);
      } else {
        setError(response.error || "Error al registrar usuario.");
        toast.error(response.error || "Error al registrar usuario.", { position: "top-right" });
      }
    } catch (err) {
      setError("Error al conectar con el servidor.");
      toast.error("Error al conectar con el servidor.", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white p-6 sm:p-8 rounded-lg shadow-md">
        <h2 className="text-center text-2xl font-bold text-gray-900">Crear una cuenta nueva</h2>
        {error && <div className="mt-4 text-red-600 text-center">{error}</div>}
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <InputField label="Usuario" type="text" name="userName" value={formData.userName} onChange={handleChange} />
          <InputField label="Correo electrónico" type="email" name="email" value={formData.email} onChange={handleChange} />
          <InputField label="Contraseña" type="password" name="password" value={formData.password} onChange={handleChange} />
          <InputField label="Confirmar contraseña" type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} />
          <EncryptButton
            type="submit"
            text={loading ? "Registrando..." : "Registrarse"}
            disabled={loading}
            className={`w-full p-2 text-white rounded-lg transition duration-300 ease-in-out 
              ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-700'}`}
          >
            
          </EncryptButton>
        </form>
      </div>
    </div>
  );
};

export default Register;
