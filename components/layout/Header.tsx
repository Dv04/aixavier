'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const links = [
  { href: "/", label: "Home" },
  { href: "/solutions", label: "Solutions" },
  { href: "/platform", label: "Platform" },
  { href: "/security", label: "Security" },
  { href: "/company", label: "Company" },
];

export default function Header() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-30 border-b border-white/5 bg-[#050505]/75 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-3 sm:px-8">
        <Link href="/" className="flex items-center gap-2 text-sm font-semibold tracking-[0.24em] uppercase hdr">
          DHI
          <span className="text-xs rounded-full border border-emerald-400/40 px-2 py-0.5 text-emerald-200/90">EDGE</span>
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-slate-200 sm:flex">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={clsx(
                "transition hover:text-emerald-200",
                pathname === link.href ? "text-emerald-300" : "text-slate-200"
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <Link
          href="/contact"
          className="rounded-full border border-white/20 bg-white/5 px-4 py-2 text-xs font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300 hover:bg-white/10"
        >
          Book a pilot
        </Link>
      </div>
    </header>
  );
}
