export default function ContactPage() {
  return (
    <main className="mx-auto flex max-w-4xl flex-col gap-8 px-6 py-12 sm:px-10">
      <header className="space-y-3">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Contact</p>
        <h1 className="text-4xl font-semibold text-white hdr">Book a pilot.</h1>
        <p className="text-sm text-slate-300">
          Tell us about your site (transit platforms, depots, DCs). We’ll scope cameras, patterns, and hardware fit.
        </p>
      </header>
      <form className="grid gap-4 rounded-2xl border border-white/10 bg-white/5 p-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="text-sm text-slate-200">
            Name
            <input
              className="mt-2 w-full rounded-lg border border-white/10 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-emerald-300"
              name="name"
              placeholder="Jane Doe"
            />
          </label>
          <label className="text-sm text-slate-200">
            Email
            <input
              className="mt-2 w-full rounded-lg border border-white/10 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-emerald-300"
              name="email"
              type="email"
              placeholder="jane@company.com"
            />
          </label>
        </div>
        <label className="text-sm text-slate-200">
          Organization
          <input
            className="mt-2 w-full rounded-lg border border-white/10 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-emerald-300"
            name="org"
            placeholder="City Transit / 3PL / Operator"
          />
        </label>
        <label className="text-sm text-slate-200">
          What are you trying to protect?
          <textarea
            className="mt-2 w-full rounded-lg border border-white/10 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-emerald-300"
            name="context"
            rows={4}
            placeholder="Platforms, depots, DC floor, dock doors, etc."
          />
        </label>
        <button
          type="submit"
          className="mt-2 w-full rounded-full bg-white px-5 py-3 text-sm font-semibold text-black shadow-lg shadow-emerald-500/30 transition hover:-translate-y-0.5"
        >
          Request pilot
        </button>
      </form>
    </main>
  );
}
