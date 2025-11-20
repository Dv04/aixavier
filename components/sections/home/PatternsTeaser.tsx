'use client';

import { motion } from "framer-motion";

const patterns = [
  "Restricted-Zone Intrusion",
  "Person-Down",
  "Smoke/Fire",
  "Aggression",
  "PPE Compliance",
  "Vehicle–Person Conflict",
  "Crowding / Dwell",
  "Unattended Objects",
];

export default function PatternsTeaser() {
  return (
    <section className="mx-auto max-w-6xl px-6 pb-16 sm:px-10">
      <div className="flex items-center justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-slate-400 hdr">Pattern catalog</p>
          <h2 className="mt-2 text-3xl font-semibold text-white">Reusable patterns, tuned per site.</h2>
          <p className="mt-3 text-base text-slate-300">
            One catalog, many environments. Swap rules, ROIs, thresholds, and playbooks without rebuilding models.
          </p>
        </div>
        <a
          href="/solutions"
          className="hidden rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300 sm:inline-flex"
        >
          View all patterns
        </a>
      </div>
      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
        {patterns.map((name, i) => (
          <motion.div
            key={name}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.35, delay: i * 0.02 }}
            className="rounded-xl border border-white/8 bg-white/5 px-4 py-4 text-sm text-slate-100 shadow-[0_12px_40px_rgba(0,0,0,0.25)]"
          >
            <span className="hdr text-[11px] text-emerald-300">{String(i + 1).padStart(2, "0")}</span>
            <div className="mt-2 text-base font-semibold text-white">{name}</div>
          </motion.div>
        ))}
      </div>
      <a
        href="/solutions"
        className="mt-4 inline-block rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300 sm:hidden"
      >
        View all patterns
      </a>
    </section>
  );
}
