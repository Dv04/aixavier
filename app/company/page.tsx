export default function CompanyPage() {
  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-10 sm:px-10">
      <header className="space-y-3">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Company</p>
        <h1 className="text-4xl font-semibold text-white hdr">Built by operators of large video systems.</h1>
        <p className="text-sm text-slate-300 max-w-3xl">
          Founders from edge AI, VMS, and safety systems. We build for regulated, high-density environments where latency,
          privacy, and reliability decide outcomes.
        </p>
      </header>
      <section className="rounded-2xl border border-white/10 bg-white/5 p-6 text-sm text-slate-200">
        <p>
          We are US-based, focused on transit and logistics as wedge markets. The platform is designed to pass CISO, unions,
          and infrastructure security reviews: edge-first, privacy-by-default, hardware-agnostic.
        </p>
        <p className="mt-3">
          Looking for exceptional engineers and deployment leaders who have shipped on NVIDIA edge, industrial PCs, and
          multi-site rollouts. Contact us if you’ve run safety, security, or mission-critical video at scale.
        </p>
      </section>
    </main>
  );
}
