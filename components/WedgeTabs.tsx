'use client';

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const wedges = {
  transit: {
    title: "Transit / Mobility",
    copy:
      "Track trespass, platform red-zone, passenger collapse, aggression inside railcars, and unattended baggage—without streaming raw video off-site.",
    bullets: [
      "Platform edge + tunnel trespass mapped to Restricted-Zone pattern.",
      "Passenger collapse uses pose + temporal smoothing (11.30 ms FP16).",
      "Aggression inside cars flagged by MobileNet-TSM (12.90 → 9.00 ms).",
      "Metadata or short clips only; works with Genetec / Milestone / Avigilon.",
    ],
    cta: "Schedule OCC/PTO workshop",
  },
  logistics: {
    title: "Logistics / Warehousing",
    copy:
      "Forklift–pedestrian conflict, dock door intrusion, PPE compliance, smoke near battery racks, and queue congestion in staging lanes.",
    bullets: [
      "Forklift proximity + unsafe speed: stride=3 clips to stay under 7.2 GB VRAM on NX.",
      "PPE compliance with SCRFD 6.20 ms + ArcFace 2.10 ms; threshold 0.47.",
      "Smoke/Fire at racks via EfficientNet-B0 Fire 9.80 ms FP16.",
      "Occupancy + dwell exported to Prometheus (:9100) for throughput tuning.",
    ],
    cta: "Book DC floor-walk",
  },
};

export default function WedgeTabs() {
  const [active, setActive] = useState<"transit" | "logistics">("transit");
  const data = wedges[active];

  return (
    <section id="pilots" className="mx-auto max-w-6xl px-6 pb-28 sm:px-10">
      <div className="mb-6 flex items-center gap-2">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400">Wedge-first GTM</p>
        <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] text-slate-200">
          US focus · pilots next 6–9 months
        </span>
      </div>
      <div className="flex gap-3 pb-6">
        {(["transit", "logistics"] as const).map((key) => (
          <button
            key={key}
            onClick={() => setActive(key)}
            className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
              active === key
                ? "bg-white text-black shadow-lg shadow-cyan-500/30"
                : "border border-white/10 bg-white/5 text-slate-200 hover:border-cyan-300 hover:text-cyan-100"
            }`}
          >
            {wedges[key].title}
          </button>
        ))}
      </div>

      <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-black/70 p-6 shadow-2xl shadow-orange-500/10">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-orange-500/15 blur-2xl" />
        <AnimatePresence mode="wait">
          <motion.div
            key={active}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.35, ease: "easeOut" }}
            className="relative space-y-4"
          >
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.28em] text-slate-400">{data.title}</p>
                <h3 className="text-2xl font-semibold text-white">Pilot pack</h3>
              </div>
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs text-slate-200">
                Includes edge appliance, rules tuning, SOC/VMS integration
              </span>
            </div>
            <p className="max-w-4xl text-sm text-slate-200">{data.copy}</p>
            <ul className="grid gap-3 sm:grid-cols-2">
              {data.bullets.map((item) => (
                <li
                  key={item}
                  className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-100 shadow-inner shadow-cyan-500/5"
                >
                  <span className="mr-2 text-emerald-400">●</span>
                  {item}
                </li>
              ))}
            </ul>
            <div className="flex flex-wrap gap-3 pt-2">
              <a
                href="mailto:pilots@projectdhi.com"
                className="rounded-full bg-orange-500 px-4 py-2 text-sm font-semibold text-black shadow-lg shadow-orange-500/30 transition hover:-translate-y-0.5"
              >
                {data.cta}
              </a>
              <a
                href="#patterns"
                className="rounded-full border border-white/10 px-4 py-2 text-sm font-semibold text-slate-100 transition hover:border-cyan-300 hover:text-cyan-100"
              >
                View pattern specifics
              </a>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </section>
  );
}
