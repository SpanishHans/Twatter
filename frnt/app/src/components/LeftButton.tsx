import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  variant?: "blue" | "white" | "outline" | "noborder";
  onClick?: () => void;
  href?: string;
  className?: string;
  icon?: React.ReactNode; // Optional icon
};

const LButton: React.FC<ButtonProps> = ({ children, variant = "blue", onClick, href, className = "", icon }) => {
  
  const baseStyles = "relative inline-flex rounded-full px-4 py-2 transition font-semibold w-full text-center items-center justify-center";
  
  const variantStyles = {
    blue: "bg-[#1D9BF0] text-white hover:bg-[#1A8CD8]",
    white: "bg-white text-black hover:bg-gray-200",
    outline: "border-2 border-[#1D9BF0] text-[#1D9BF0] hover:bg-[#E8F5FE]",
    noborder: "text-white hover:text-black hover:bg-white",
  };

  // ✅ Fix: Use backticks for template literals
  const combinedStyles = `${baseStyles} ${variantStyles[variant]} ${className}`;

  const content = (
    <span className="relative flex items-center w-full">
      {/* Icon (only visible if there's enough space) */}
      {icon && <span className="absolute left-0">{icon}</span>}

      {/* ✅ Fix: Remove extra `${}` */}
      <span className={variant === "noborder" ? "ml-11" : ""}>{children}</span>
    </span>
  );

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

export default LButton;
