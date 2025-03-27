import { Link } from 'react-router-dom';
import BannerImagen from '../../assets/Img/car_hero.webp'
import EncryptButton from '../Butoon/EncryptButton';
import {useTheme} from '../../context/ThemeContext';
export default function Hero() {

  const {darkMode} = useTheme();

  return (
    /* {`w-full z-50 shadow-sm ${darkMode ? " bg-[#352443] text-white" : "bg-gradient-to-r from-blue-500 to-purple-500 text-white"}`} */
    /* relative w-full isolate overflow-hidden px-6 pt-0 lg:px-8 */
    <div className={`w-full z-50 shadow-sm font-Roboto ${darkMode ? " bg-[#352443] text-white" : " text-gray-900"}`} >
      {/* Fondo decorativo */}
      <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
        <div
          className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
          style={{
            clipPath:
              'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
          }}
        />
      </div>
      {/* Imagen del Hero */}
      <div className="relative flex justify-center">
        <img
          src={BannerImagen}
          alt="CarPrediction - Predicción de precios de autos"
          className="w-full max-w-10xl mx-auto mask-gradient"
        />
      </div>
      {/* Contenido principal */}
      <div className="mx-auto max-w-2xl text-center mt-6 py-8 sm:py-12 lg:py-24">
        <h1 className="text-4xl font-bold tracking-tight  sm:text-6xl">
          Predice el precio de tu auto con IA
        </h1>
        <p className="mt-6 text-lg leading-8 ">
          Utiliza nuestro avanzado sistema de inteligencia artificial para obtener predicciones precisas
          del valor de tu vehículo basadas en múltiples factores del mercado.
        </p>

        {/* Botones */}
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <EncryptButton 
            to="/prediction"
            text='Comenzar predicción'
            className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold  shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
          </EncryptButton >
          <EncryptButton to="/about" className="text-sm font-semibold leading-6 text-gray-900"
          text={"Saber más →"}>
            
          </EncryptButton>
        </div>
      </div>
    </div>
  );
}