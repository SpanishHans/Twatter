// src/components/Topbar.tsx
import Link from "next/link";

const Topbar = () => {
  return (
    <nav className="flex items-center justify-between p-4 bg-white shadow-md">
      <Link href="/" className="text-2xl font-bold text-blue-600">
        Twatter 🐦
      </Link>

      <div className="space-x-4">
        <Link href="/login" className="hover:underline">
          Login
        </Link>
        <Link href="/register" className="hover:underline">
          Register
        </Link>
      </div>
    </nav>
  );
};

export default Topbar;
