import { useRef, useState } from "react";
import { FiLock } from "react-icons/fi";
import { motion } from "framer-motion";
import { Link } from "react-router-dom"; // Importa Link

const CHARS = "!@#$%^&*():{};|,.<>/?";
const CYCLES_PER_LETTER = 2;
const SHUFFLE_TIME = 50;

const EncryptButton = ({ text = "Encrypt Data", to, type = "button" }) => {
  const intervalRef = useRef(null);
  const [displayText, setDisplayText] = useState(text);

  const scramble = () => {
    let pos = 0;
    intervalRef.current = setInterval(() => {
      const scrambled = text
        .split("")
        .map((char, index) =>
          pos / CYCLES_PER_LETTER > index
            ? char
            : CHARS[Math.floor(Math.random() * CHARS.length)]
        )
        .join("");

      setDisplayText(scrambled);
      pos++;

      if (pos >= text.length * CYCLES_PER_LETTER) {
        stopScramble();
      }
    }, SHUFFLE_TIME);
  };

  const stopScramble = () => {
    clearInterval(intervalRef.current);
    setDisplayText(text);
  };

  const ButtonContent = (
    <>
      <div className="relative z-10 flex items-center gap-2">
        <FiLock />
        <span>{displayText}</span>
      </div>

      <motion.span
        initial={{ y: "100%" }}
        animate={{ y: "-100%" }}
        transition={{
          repeat: Infinity,
          repeatType: "mirror",
          duration: 1,
          ease: "linear",
        }}
        className="absolute inset-0 z-0 scale-125
                   bg-gradient-to-t from-blue-200/0 from-40% via-blue-200/100 to-blue-200/0 to-60%
                   opacity-0 transition-opacity group-hover:opacity-100"
      />
    </>
  );

  return to ? (
    <Link
      to={to}
      onMouseEnter={scramble}
      onMouseLeave={stopScramble}
      className="group relative overflow-hidden rounded-lg border-none
                 bg-gradient-to-r from-blue-500 to-purple-500 px-4 py-2
                 font-mono font-medium uppercase text-white
                 transition duration-300 hover:shadow-xl w-full
                 flex items-center justify-center gap-2"
    >
      {ButtonContent}
    </Link>
  ) : (
    <motion.button
      type={type}
      whileHover={{ scale: 1.025 }}
      whileTap={{ scale: 0.975 }}
      onMouseEnter={scramble}
      onMouseLeave={stopScramble}
      className="group relative overflow-hidden rounded-lg border-none
                 bg-gradient-to-r from-blue-500 to-purple-500 px-4 py-2
                 font-mono font-medium uppercase text-white
                 transition duration-300 hover:shadow-xl w-full
                 flex items-center justify-center gap-2"
    >
      {ButtonContent}
    </motion.button>
  );
};

export default EncryptButton;
