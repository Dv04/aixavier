export default function SocialProof() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-14 sm:px-10">
      <div className="rounded-2xl border border-white/8 bg-white/5 px-6 py-6 backdrop-blur">
        <p className="text-xs uppercase tracking-[0.16em] text-slate-400 hdr">Readiness</p>
        <div className="mt-3 flex flex-col gap-4 text-sm text-slate-200 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-base text-slate-200">
            Validated on NVIDIA AGX/NX and industrial x86 edge nodes. Built for RTSP/ONVIF and VMS networks (Genetec,
            Milestone, Avigilon).
          </p>
          <div className="flex flex-wrap gap-3 text-[12px] text-slate-300">
            <span className="rounded-full border border-emerald-400/30 bg-black/30 px-3 py-1">On-site inference</span>
            <span className="rounded-full border border-emerald-400/30 bg-black/30 px-3 py-1">Metadata-only egress</span>
            <span className="rounded-full border border-emerald-400/30 bg-black/30 px-3 py-1">Pilot-ready</span>
          </div>
        </div>
      </div>
    </section>
  );
}
