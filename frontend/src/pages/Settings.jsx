// Settings.jsx
import SliderToggle from "../components/Butoon/Toogle";

export default function Settings() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Configuraciones</h1>
      <div className="mb-4 w-10">
        <SliderToggle />
      </div>
      {/* Otras configuraciones */}
    </div>
  );
}