'use client';

import { motion } from "framer-motion";

export default function ArchitectureTeaser() {
  return (
    <section id="architecture" className="mx-auto max-w-6xl px-6 pb-16 sm:px-10">
      <div className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.16em] text-slate-400 hdr">Edge architecture</p>
            <h3 className="text-2xl font-semibold text-white">Camera → Edge node → Privacy firewall → Alerts.</h3>
            <p className="mt-2 text-base text-slate-200">
              RTSP/ONVIF ingest, DeepStream/TensorRT inference on-site, rules engine, privacy filter, and telemetry/exporter.
              Raw video stays local; only metadata leaves.
            </p>
          </div>
          <a
            href="/platform"
            className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300"
          >
            View platform
          </a>
        </div>
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          {[
            { title: "Ingest", body: "RTSP/ONVIF, mirrored NVR streams; 4–16 cams/node." },
            { title: "Inference + Rules", body: "TensorRT detectors + rule graph; latency 25–52 ms demo profile." },
            { title: "Privacy Firewall", body: "FRS thresholding 0.47; embeddings encrypted; MTLS to control-plane." },
          ].map((item, i) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.35, delay: i * 0.05 }}
              className="rounded-xl border border-white/8 bg-black/60 px-4 py-3 shadow-[0_12px_40px_rgba(0,0,0,0.25)]"
            >
              <p className="hdr text-sm text-emerald-300">{item.title}</p>
              <p className="mt-2 text-sm text-slate-200">{item.body}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
