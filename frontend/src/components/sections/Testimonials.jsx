import * as motion from "motion/react-client";
import { useState, useEffect, useRef } from "react";
import testimonials from '../../data/TestimonialsData.json'
/**
 * Tarjeta individual de testimonio
 */
function TestimonialCard({ quote, authorName, authorRole, authorImage }) {
  return (
    <div className="min-w-[300px] bg-white p-6 shadow-md rounded-lg">
      <div className="flex justify-center -mt-12">
        <img
          className="h-20 w-20 rounded-full border-4 border-white object-cover shadow"
          src={authorImage}
          alt={authorName}
        />
      </div>
      <blockquote className="mt-4 text-center text-gray-700 italic">{quote}</blockquote>
      <div className="mt-4 text-center">
        <p className="font-semibold text-gray-900">{authorName}</p>
        <p className="text-sm text-gray-500">{authorRole}</p>
      </div>
    </div>
  );
}

/**
 * Componente principal: arrastrar horizontalmente los testimonios
 */
export default function TestimonialDrag() {
  const [activeDirection, setActiveDirection] = useState(null);
  const [containerWidth, setContainerWidth] = useState(0);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        setContainerWidth(containerRef.current.offsetWidth);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <section className="bg-white py-12 sm:py-16 flex flex-col items-center justify-center bg-gray-100 p-6">
      <div className="mb-10 text-center">
          <h2 className="text-3xl font-bold text-gray-900">Testimonials</h2>
          <p className="mt-2 text-gray-600">See what our customers are saying.</p>
      </div>
      {/* Contenedor del slider derecha */}
      <div ref={containerRef} className="relative w-full max-w-full border-none rounded-lg p-4 overflow-hidden">
        <motion.div
          drag="x" // Bloquea el arrastre solo en el eje horizontal
          onDragStart={() => setActiveDirection("x")}
          onDragEnd={() => setActiveDirection(null)}
          dragConstraints={{ left: -containerWidth, right: 0 }} // Ajusta según el ancho del contenedor
          dragElastic={0.2}
          whileDrag={{ cursor: "grabbing" }}
          className="flex gap-4 overflow-visible px-4 transition-opacity duration-500 ease-in-out"
        >
          {testimonials.map((item) => (
            <TestimonialCard key={item.id} {...item} />
          ))}
        </motion.div>

        {/* Indicador de dirección */}
        {activeDirection && (
          <p className="absolute bottom-2 right-2 text-sm text-gray-500">
            {/* Arrastrando: <strong>{activeDirection}</strong> */}
          </p>
        )}
      </div>
    </section>
  );
}
