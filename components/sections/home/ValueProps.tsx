export default function ValueProps() {
  const items = [
    {
      title: "Edge-first by design",
      body: "Runs beside your cameras and VMS. No raw video to the cloud, ever—only metadata unless you opt-in to clips.",
    },
    {
      title: "Pattern catalog as IP",
      body: "8 canonical patterns reused across sites with rules, KPIs, and playbooks to accelerate rollouts.",
    },
    {
      title: "Built for regulated ops",
      body: "FIPS-minded posture: MTLS, signed updates, encrypted embeddings, audit trails, and degraded mode on-site.",
    },
  ];
  return (
    <section className="mx-auto max-w-6xl px-6 pb-14 sm:px-10">
      <div className="grid gap-4 sm:grid-cols-3">
        {items.map((item) => (
          <div key={item.title} className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
            <p className="hdr text-sm text-emerald-300">{item.title}</p>
            <p className="mt-3 text-sm text-slate-200">{item.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
