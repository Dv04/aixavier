import type { Metadata } from "next";
import { GeistMono } from "geist/font";
import { Rajdhani } from "next/font/google";
import "./globals.css";
import Providers from "./providers";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

const rajdhani = Rajdhani({ weight: ["600", "700"], subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Project Dhi | Edge Safety Intelligence",
  description:
    "Edge-native safety intelligence that turns passive CCTV into real-time protection for transit, logistics, and critical infrastructure.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="bg-[#050505] text-slate-100">
      <body
        className={`${rajdhani.className} ${GeistMono.variable} antialiased selection:bg-emerald-500/20`}
        suppressHydrationWarning
      >
        <Providers>
          <div className="min-h-screen bg-[#020308]">
            <Header />
            {children}
            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}
