import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  variant?: "blue" | "white" | "outline";
  onClick?: () => void;
  href?: string;
  className?: string;
  icon?: React.ReactNode; // Optional icon
};

const Button: React.FC<ButtonProps> = ({ children, variant = "blue", onClick, href, className = "", icon }) => {
  
  const baseStyles = "relative inline-flex rounded-full px-6 py-2 transition font-semibold w-full ";
  
  const variantStyles = {
    blue: "text-center items-center justify-center bg-[#1D9BF0] text-white hover:bg-[#1A8CD8]",
    white: "text-center items-center justify-center bg-white text-black hover:bg-gray-200",
    outline: "text-center items-center justify-center border-2 border-[#1D9BF0] text-[#1D9BF0] hover:bg-[#E8F5FE]",
    noborder: "text-white hover:text-black hover:bg-white",
  };

  const combinedStyles = `${baseStyles} ${variantStyles[variant]} ${className}`;

  const content = (
    <>
      {/* Icon (only visible if there's enough space) */}
      {icon && <span className="inline absolute left-3">{icon}</span>}

      {/* Centered text */}
      <span className="flex-grow">{children}</span>
    </>
  );

  // Render <a> if href exists, otherwise render <button>
  return href ? (
    <a href={href} className={combinedStyles}>
      {content}
    </a>
  ) : (
    <button onClick={onClick} className={combinedStyles}>
      {content}
    </button>
  );
};

export default Button;