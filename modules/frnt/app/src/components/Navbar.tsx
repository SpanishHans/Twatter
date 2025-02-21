import Image from "next/image";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex justify-between p-4 bg-white-100 text-white">
      <Image
            src="/logo_100.svg" // No need to use @ alias
            alt="Twatter Logo"
            width='50'
            height='50'
          />
      <div className="flex gap-4 items-center p-4">
        <Link href="/feed">Feed</Link>
        <Link href="/login">Login</Link>
        <Link href="/register">Register</Link>
      </div>
    </nav>
  );
}
