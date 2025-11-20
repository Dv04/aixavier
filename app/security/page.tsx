const bullets = [
  "Raw video stays on the customer LAN; metadata-only by default; optional short clips with explicit policy.",
  "MTLS between edge nodes and control-plane; signed agent updates; config and secrets encrypted at rest.",
  "FRS privacy: SCRFD + ArcFace threshold 0.47; embeddings encrypted; audit trails for enroll/match.",
  "Least-privilege edge footprint: minimal services, locked-down ports, on-node degraded mode when offline.",
  "FIPS direction: designed to align with 140-3 expectations for crypto modules and tamper evidence.",
];

export default function SecurityPage() {
  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-10 sm:px-10">
      <header className="space-y-3">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Security & Privacy</p>
        <h1 className="text-4xl font-semibold text-white hdr">Privacy by design. Edge by default.</h1>
        <p className="text-sm text-slate-300 max-w-3xl">
          We assume regulated, unionized, and bandwidth-constrained environments. Video stays local; metadata leaves with
          controls and auditability.
        </p>
      </header>
      <section className="grid gap-4 sm:grid-cols-2">
        {bullets.map((b) => (
          <div key={b} className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-200">
            {b}
          </div>
        ))}
      </section>
    </main>
  );
}
