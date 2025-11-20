'use client';

import { motion } from "framer-motion";
import { useState } from "react";

const patterns = [
  {
    title: "Restricted-Zone Intrusion",
    blurb: "Geofenced ROI + dwell-time rules tuned for track edges, dock doors, and forklift-only aisles.",
    metric: "<40 ms rule eval",
    detail: "DeepStream primary-gie batching=2 keeps end-to-end under 40 ms.",
    accent: "from-cyan-400/40 via-transparent to-orange-400/30",
  },
  {
    title: "Person-Down / Collapse",
    blurb: "Pose + temporal smoothing to catch collapses behind racks, on platforms, or between vehicles.",
    metric: "11.30 ms pose FP16",
    detail: "yolov11n-pose FP16; exports live in models/usecases/pose/fp16/",
    accent: "from-emerald-400/30 via-transparent to-cyan-300/30",
  },
  {
    title: "Smoke / Fire Anomalies",
    blurb: "Haze and flame cues for battery rooms, concession stands, and electrical cabinets.",
    metric: "9.80 ms fire FP16",
    detail: "EfficientNet-B0 Fire FP16 (INT8 6.70 ms) with on-node suppression.",
    accent: "from-orange-500/40 via-transparent to-amber-300/30",
  },
  {
    title: "Aggression / Violence",
    blurb: "Action detector flags fights in railcars, concourses, yards, or break rooms.",
    metric: "12.90 → 9.00 ms",
    detail: "MobileNet-TSM FP16/INT8; clip batch=1 on NX to stay under 7.2 GB VRAM.",
    accent: "from-red-500/40 via-transparent to-cyan-300/20",
  },
  {
    title: "PPE & Staff Presence",
    blurb: "Checks hi-vis, helmets, and staff-at-door semantics without sending faces to cloud.",
    metric: "6.20 ms detect",
    detail: "SCRFD-500M face detect + MobileFaceNet ArcFace 2.10 ms; threshold 0.47.",
    accent: "from-emerald-400/40 via-transparent to-slate-200/10",
  },
  {
    title: "Vehicle–Person Conflict",
    blurb: "Forklift proximity, unsafe speed, door interference, and platform edge conflicts.",
    metric: "stride=3 safe",
    detail: "Action clips stride=3; keeps NX memory below 7.2 GB while tracking.",
    accent: "from-cyan-300/30 via-transparent to-amber-400/20",
  },
  {
    title: "Crowding & Dwell",
    blurb: "Density and over-capacity alarms for platforms, gates, staging lanes, or docks.",
    metric: "25 FPS ingest",
    detail: "Profile demo targets 25 FPS; exporter surfaces occupancy metrics at /metrics.",
    accent: "from-blue-400/30 via-transparent to-green-300/20",
  },
  {
    title: "Unattended / Suspicious Objects",
    blurb: "Detects bags or pallets left too long in sensitive zones; clips stay local.",
    metric: "3 s ring buffer",
    detail: "Recorder queue max-size-time=3s; keeps pre/post context without cloud egress.",
    accent: "from-amber-400/30 via-transparent to-orange-500/30",
  },
];

export default function BentoGrid() {
  const [hovered, setHovered] = useState<number | null>(null);
  return (
    <section id="patterns" className="relative z-10 mx-auto px-6 pb-24 sm:px-10">
      <div className="mb-8 flex items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Pattern Catalog</p>
          <h2 className="text-3xl font-semibold text-white hdr">8 canonical patterns, parameterised per site.</h2>
        </div>
        <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">
          Runs on NVIDIA AGX/NX + industrial x86
        </span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 max-w-7xl mx-auto p-4">
        {patterns.map((pattern, idx) => {
          const colSpan =
            pattern.title === "Restricted-Zone Intrusion" || pattern.title === "Person-Down / Collapse"
              ? "md:col-span-2"
              : "";
          return (
            <motion.div
              key={pattern.title}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ amount: 0.2, once: true }}
              transition={{ type: "spring", stiffness: 200, damping: 20, delay: idx * 0.04 }}
              onHoverStart={() => setHovered(idx)}
              onHoverEnd={() => setHovered(null)}
              className={`group relative overflow-hidden rounded-xl p-[1px] h-full min-h-[200px] ${colSpan}`}
              style={{ opacity: hovered !== null && hovered !== idx ? 0.6 : 1, transition: "opacity 180ms ease" }}
            >
              <div className="absolute inset-0 bg-[conic-gradient(from_0deg,rgba(0,255,148,0.3),rgba(255,69,0,0.35),rgba(0,255,148,0.3))] animate-[spin_12s_linear_infinite]" />
              <div className="absolute inset-[1px] bg-black rounded-xl" />
              <div className="relative flex h-full flex-col gap-4 rounded-[14px] bg-black/75 px-5 py-4 backdrop-blur-sm transition duration-300 group-hover:-translate-y-1 border border-white/5">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-white hdr">{pattern.title}</h3>
                  <span className="text-4xl font-mono font-bold text-emerald-400 leading-none">{pattern.metric}</span>
                </div>
                <p className="text-sm text-slate-300">{pattern.blurb}</p>
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.7)]" />
                  {pattern.detail}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
