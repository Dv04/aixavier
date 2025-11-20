'use client';

import dynamic from "next/dynamic";
import { motion } from "framer-motion";
import Terminal from "./Terminal";

const PointField = dynamic(() => import("./PointField"), { ssr: false });

export default function Hero() {
  return (
    <section className="relative isolate overflow-hidden min-h-screen">
      <div className="absolute inset-0 w-full h-full z-0">
        <PointField />
      </div>
      <div className="noise-overlay opacity-10" aria-hidden />

      <div className="relative z-10 flex h-screen flex-col justify-end px-6 pb-12 sm:px-10">
        <div className="max-w-4xl space-y-5">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-[12px] text-slate-200 hdr"
          >
            Transit & logistics · Edge-native · Privacy-first
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, x: -22 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, ease: "easeOut", delay: 0.08 }}
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold leading-tight text-white"
          >
            Edge-native safety intelligence for transit and logistics.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, x: -14 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, ease: "easeOut", delay: 0.16 }}
            className="max-w-2xl text-base text-slate-200"
          >
            Run a reusable pattern catalog beside your existing CCTV. Sub-second detections for trespass, crowding, falls,
            smoke/fire, PPE, and unattended objects. Raw video stays on-site; only metadata leaves the node.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, ease: "easeOut", delay: 0.22 }}
            className="flex flex-wrap items-center gap-4"
          >
            <a
              href="/contact"
              className="rounded-full bg-emerald-500 px-5 py-3 text-sm font-semibold text-black shadow-lg shadow-emerald-500/30 transition hover:-translate-y-0.5"
            >
              Book a pilot
            </a>
            <a
              href="/platform"
              className="rounded-full border border-white/15 px-5 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300"
            >
              See the platform
            </a>
          </motion.div>
        </div>
        <div className="mt-12 w-full max-w-lg">
          <div className="rounded-xl border border-white/12 bg-black/70 p-4 font-mono text-xs text-emerald-200/85 shadow-[0_18px_70px_rgba(0,0,0,0.45)] backdrop-blur">
            <div className="mb-2 flex items-center gap-2 text-[10px] uppercase tracking-[0.16em] text-slate-400 hdr">
              Engineer console
            </div>
            <Terminal />
          </div>
        </div>
      </div>
    </section>
  );
}
