'use client';

import { motion } from "framer-motion";

const stages = [
  {
    title: "Camera / NVR",
    description: "RTSP / ONVIF from existing IP cams + mirrored NVR streams.",
    meta: "4–16 streams / node",
    x: 90,
  },
  {
    title: "Edge Node",
    description: "DeepStream ingest → TensorRT detectors → rules engine. Video stays on LAN.",
    meta: "Latency: <40 ms",
    x: 340,
  },
  {
    title: "Privacy Firewall",
    description: "Faces → SCRFD + ArcFace 0.47 threshold; embeddings encrypted at rest.",
    meta: "FRS audit on-node",
    x: 560,
  },
  {
    title: "Alerts & Metrics",
    description: "MQTT/REST alerts; Prometheus at :9100; circular recorder with 3 s buffer.",
    meta: "Clips optional",
    x: 780,
  },
];

export default function Architecture() {
  const packetKeyframes = {
    cx: [90, 340, 340, 780],
    fill: ["#ff4d4d", "#ff4d4d", "#00ff94", "#00ff94"],
    times: [0, 0.38, 0.5, 1],
  };

  return (
    <section id="architecture" className="relative mx-auto max-w-6xl px-6 pb-24 sm:px-10">
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-cyan-500/10 via-emerald-400/5 to-orange-400/10 blur-3xl" />
      <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-black/70 px-6 py-10 shadow-2xl shadow-cyan-500/10 backdrop-blur">
        <div className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Edge-to-cloud stance</p>
            <h2 className="text-3xl font-semibold text-white hdr">Camera → Edge → Alert, with a privacy firewall in the middle.</h2>
            <p className="mt-2 max-w-3xl text-sm text-slate-300">
              We sit beside your VMS, not inside your cloud. Heavy inference, rules, and storage remain on-site; only
              metadata and optional clips leave the firewall.
            </p>
          </div>
          <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs text-slate-200">
            Hardware-agnostic · NVIDIA AGX/NX · Industrial x86
          </span>
        </div>

        <div className="relative mb-8 h-56 rounded-2xl border border-white/10 bg-gradient-to-r from-cyan-500/10 via-black/40 to-orange-500/10 p-4 overflow-hidden">
          <svg viewBox="0 0 880 180" className="absolute inset-0 h-full w-full">
            <defs>
              <linearGradient id="flow" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#ff4d4d" />
                <stop offset="45%" stopColor="#ff4d4d" />
                <stop offset="46%" stopColor="#00ff94" />
                <stop offset="100%" stopColor="#00ff94" />
              </linearGradient>
            </defs>
            {[0, 60, 120].map((offset) => (
              <path
                key={offset}
                d="M90 110 C 180 60 260 60 340 110 S 520 160 780 110"
                fill="none"
                stroke="url(#flow)"
                strokeWidth="5"
                strokeLinecap="round"
                strokeDasharray="14 8"
                className="animate-[flowline_2.2s_linear_infinite]"
                style={{ animationDelay: `${offset}ms`, opacity: 0.35 - offset * 0.001 }}
              />
            ))}
            <motion.circle
              r="10"
              cy="110"
              initial={{ cx: packetKeyframes.cx[0], fill: packetKeyframes.fill[0] }}
              animate={{ cx: packetKeyframes.cx, fill: packetKeyframes.fill }}
              transition={{ duration: 2.4, repeat: Infinity, ease: "linear", times: packetKeyframes.times }}
            />
          </svg>
        </div>

        <div className="grid gap-4 lg:grid-cols-4">
          {stages.map((stage, idx) => (
            <motion.div
              key={stage.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.4, delay: idx * 0.05 }}
              className="relative rounded-2xl border border-white/10 bg-white/5 p-[1px]"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-cyan-500/10 opacity-0 transition duration-300 hover:opacity-100" />
              <div className="relative h-full rounded-[15px] bg-black/70 px-5 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Hexagon />
                    <h3 className="text-lg font-semibold text-white hdr">{stage.title}</h3>
                  </div>
                  <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] font-mono text-cyan-100">
                    {stage.meta}
                  </span>
                </div>
                <p className="mt-3 text-sm text-slate-300">{stage.description}</p>
                {idx < stages.length - 1 && (
                  <div className="mt-5 flex items-center gap-2 text-[11px] uppercase tracking-[0.3em] text-slate-400">
                    <span className="h-px flex-1 bg-gradient-to-r from-cyan-300/60 via-white/40 to-orange-300/60" />
                    flow
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Hexagon() {
  return (
    <motion.svg
      width="28"
      height="28"
      viewBox="0 0 100 100"
      fill="none"
      stroke="#00FF94"
      strokeWidth="6"
      className="opacity-80"
      animate={{ rotate: 360 }}
      transition={{ duration: 16, repeat: Infinity, ease: "linear" }}
    >
      <path d="M27 10 L73 10 L90 50 L73 90 L27 90 L10 50 Z" />
    </motion.svg>
  );
}
