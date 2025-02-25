import Image from "next/image";
import Link from "next/link";

export default function Logo({ width = 250, height = 250 }) {
  return (
    <Link href="/">
      <Image
        src="/logo_100.svg"
        alt="Twatter Logo"
        width={width}
        height={height}
      />
    </Link>
  );
}
