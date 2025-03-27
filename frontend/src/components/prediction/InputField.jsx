import React from "react";

const InputField = ({
  label,
  name,
  type = "text",
  value,
  onChange,
  min,
  max,
  step,
}) => {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">
        {label}
      </label>
      <input
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        min={min}
        max={max}
        step={step}
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
      />
    </div>
  );
};

export default InputField;
