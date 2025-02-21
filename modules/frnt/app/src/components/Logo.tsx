import Image from "next/image";
import Link from "next/link";

export default function Logo() {
  return (
      <Link href="/">
        <Image
          src="/logo_100.svg"
          alt="Twatter Logo"
          width={250}
          height={250}
        />
      </Link>

  );
}
