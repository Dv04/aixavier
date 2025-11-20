import BentoGrid from "@/components/BentoGrid";
import WedgeTabs from "@/components/WedgeTabs";

export default function SolutionsPage() {
  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-10 sm:px-10">
      <header className="space-y-3">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Solutions</p>
        <h1 className="text-4xl font-semibold text-white hdr">Built for transit and logistics first.</h1>
        <p className="text-sm text-slate-300 max-w-3xl">
          Two wedges, eight reusable patterns, one edge runtime. Deploy on existing cameras and NVRs without streaming raw
          video to the cloud.
        </p>
      </header>
      <WedgeTabs />
      <div>
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr mb-2">Pattern catalog</p>
        <BentoGrid />
      </div>
    </main>
  );
}
