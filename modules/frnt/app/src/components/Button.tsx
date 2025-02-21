// components/Button.tsx
import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  variant?: "blue" | "white" | "outline";
  onClick?: () => void;
  href?: string;
  className?: string; // Accepts additional classes
};

const Button: React.FC<ButtonProps> = ({ children, variant = "blue", onClick, href, className = "" }) => {
  const baseStyles = "inline-flex justify-center items-center rounded-full px-6 py-2 transition font-semibold";
  const variantStyles = {
    blue: "bg-[#1D9BF0] text-white hover:bg-[#1A8CD8]",
    white: "bg-white text-black hover:bg-gray-200",
    outline: "border-2 border-[#1D9BF0] text-[#1D9BF0] hover:bg-[#E8F5FE]",
  };

  const combinedStyles = `${baseStyles} ${variantStyles[variant]} ${className}`;

  if (href) {
    return (
      <a href={href} className={combinedStyles}>
        {children}
      </a>
    );
  }

  return (
    <button onClick={onClick} className={combinedStyles}>
      {children}
    </button>
  );
};

export default Button;
