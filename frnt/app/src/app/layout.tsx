import type { Metadata } from "next";
import { Raleway, Syne, Roboto } from "next/font/google";
import "./globals.css";

const raleway = Raleway({
  variable: "--font-raleyway",
  subsets: ["latin"],
  weight: ["100", "300", "500", "700", "900"], // Choose required weights
});

const syne = Syne({
  variable: "--font-syne",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"], // Choose required weights
});

const roboto = Roboto({
  variable: "--font-roboto",
  subsets: ["latin"],
  weight: ["100", "300", "500", "700", "900"], // Choose required weights
});

export const metadata: Metadata = {
  title: "Twatter",
  description: "The place where twats exist",
};
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${syne.variable} ${roboto.variable} ${raleway.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
