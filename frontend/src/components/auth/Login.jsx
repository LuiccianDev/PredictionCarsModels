import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthService from "../../services/AuthServices";
import { useAuth } from "../../context/AuthContext";
import { toast } from "react-toastify";
import Google from '../../assets/Icons/google.png';
import Linkedin from '../../assets/Icons/linkedin.png';
import Github from '../../assets/Icons/github.png';
import EncryptButton from "../Butoon/EncryptButton";

function ErrorMessage({ message }) {
  if (!message) return null;
  return (
    <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
      {message}
    </div>
  );
}

function InputField({ id, label, type, value, onChange, autoComplete, required = true, placeholder }) {
  return (
    <div className="w-full">
      <label htmlFor={id} className="mb-2 text-lg text-gray-900">
        {label}
      </label>
      <input
        id={id}
        name={id}
        type={type}
        autoComplete={autoComplete}
        required={required}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="border p-3 bg-white text-gray-900 shadow-md placeholder:text-base focus:scale-105 ease-in-out duration-300 border-gray-300 rounded-lg w-full"
      />
    </div>
  );
}

function PasswordField({ value, onChange, placeholder = "Password" }) {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between">
        <label htmlFor="password" className="mb-2 text-lg text-gray-900">Password</label>
        <a href="#" className="text-blue-400 text-sm hover:underline">Forget your password?</a>
      </div>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        required
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="border p-3 bg-white text-gray-900 shadow-md placeholder:text-base focus:scale-105 ease-in-out duration-300 border-gray-300 rounded-lg w-full"
      />
    </div>
  );
}

function SubmitButton({ loading }) {
  return (
    <button
      type="submit"
      disabled={loading}
      className="bg-gradient-to-r from-blue-500 to-purple-500 shadow-lg mt-6 p-3 text-white rounded-lg w-full hover:scale-105 transition duration-300 ease-in-out"
    >
      {loading ? "Iniciando sesión..." : "LOG IN"}
    </button>
  );
}

export default function Login() {
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await AuthService.login(email, password);
      authLogin({ id: response.user, token: response.access_token });
      toast.success("Inicio de sesión exitoso!", { position: "top-right", autoClose: 2000 });
      navigate("/");
    } catch (err) {
      console.error("Error al iniciar sesión:", err);
      setError("Error al conectar con el servidor");
      toast.error("Error al conectar con el servidor", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-white font-poppins px-4">
      <div className="w-full max-w-md bg-white shadow-lg rounded-2xl p-6">
        <h1 className="text-center text-3xl font-bold text-gray-900">CarPredict Log in</h1>
        <ErrorMessage message={error} />
        <form onSubmit={handleSubmit} className="space-y-4">
          <InputField
            id="email"
            label="Email"
            type="email"
            autoComplete="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <PasswordField value={password} onChange={(e) => setPassword(e.target.value)} />
          {/* <SubmitButton loading={loading} /> */}
          <div className="flex items-center justify-center">
          <EncryptButton
            type="submit"
            text={loading ? "Iniciando sesión..." : "LOG IN"}
            onClick={() => {
              if (!loading) {
                handleLogin();
              }
            }}
          />
          </div>
        </form>
        <p className="text-center text-gray-900 mt-4">
          Don't have an account?{' '}
          <Link to="/register" className="text-blue-400 hover:underline">Sign Up</Link>
        </p>
        <div className="flex justify-center mt-4 space-x-4">
          <button className="p-2 hover:scale-105">
            <img className="w-8" src={Google} alt="Google" />
          </button>
          <button className="p-2 hover:scale-105">
            <img className="w-8" src={Linkedin} alt="Linkedin" />
          </button>
          <button className="p-2 hover:scale-105">
            <img className="w-8" src={Github} alt="Github" />
          </button>
        </div>
        <p className="text-center text-gray-500 text-sm mt-4">
          By signing in, you agree to our <a href="#" className="text-blue-400 hover:underline">Terms</a> and <a href="#" className="text-blue-400 hover:underline">Privacy Policy</a>
        </p>
      </div>
    </div>
  );
}

