'use client';

import { motion } from "framer-motion";

export default function SecurityTeaser() {
  const items = [
    "Raw video stays on the LAN; optional short clips only.",
    "MTLS between edge nodes and control-plane; signed updates.",
    "Encrypted embeddings; audit logs for FRS operations.",
  ];
  return (
    <section className="mx-auto max-w-6xl px-6 pb-14 sm:px-10">
      <div className="rounded-2xl border border-white/10 bg-black/70 px-6 py-6 backdrop-blur">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Security & Privacy</p>
        <div className="mt-3 grid gap-3 sm:grid-cols-3">
          {items.map((text, i) => (
            <motion.div
              key={text}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.3, delay: i * 0.05 }}
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200"
            >
              {text}
            </motion.div>
          ))}
        </div>
        <a
          href="/security"
          className="mt-4 inline-block rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300"
        >
          View security posture
        </a>
      </div>
    </section>
  );
}
