import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-white/5 bg-[#050505]/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-8">
        <div className="space-y-2">
          <p className="text-sm font-semibold tracking-[0.22em] uppercase hdr">Dhi</p>
          <p className="text-xs text-slate-400">Edge-native safety intelligence. Built in the US for transit & logistics.</p>
        </div>
        <div className="flex flex-wrap gap-5 text-sm text-slate-300">
          <Link href="/solutions" className="hover:text-emerald-200">
            Solutions
          </Link>
          <Link href="/platform" className="hover:text-emerald-200">
            Platform
          </Link>
          <Link href="/security" className="hover:text-emerald-200">
            Security
          </Link>
          <Link href="/company" className="hover:text-emerald-200">
            Company
          </Link>
          <Link href="/contact" className="hover:text-emerald-200">
            Contact
          </Link>
        </div>
      </div>
    </footer>
  );
}
