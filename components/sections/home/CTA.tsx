export default function CTA() {
  return (
    <section className="mx-auto max-w-5xl px-6 pb-20 text-center sm:px-10">
      <div className="rounded-3xl border border-white/10 bg-gradient-to-r from-emerald-500/10 via-black/70 to-cyan-500/10 px-6 py-10 shadow-[0_30px_120px_rgba(0,0,0,0.5)] backdrop-blur">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-300 hdr">Lighthouse pilots</p>
        <h3 className="mt-3 text-3xl font-semibold text-white hdr">Ready to light up your first site?</h3>
        <p className="mt-3 text-sm text-slate-200">
          We start with transit platforms and logistics DCs: 4–16 streams per node, on-site inference, privacy firewall on
          by default. Let’s scope your pilot.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <a
            href="/contact"
            className="rounded-full bg-white text-black px-5 py-3 text-sm font-semibold shadow-lg shadow-emerald-500/30 transition hover:-translate-y-0.5"
          >
            Talk to us
          </a>
          <a
            href="/platform"
            className="rounded-full border border-white/15 bg-white/5 px-5 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-emerald-300"
          >
            View platform
          </a>
        </div>
      </div>
    </section>
  );
}
