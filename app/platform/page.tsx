import Architecture from "@/components/Architecture";

const specs = [
  { title: "Ingest", body: "RTSP/ONVIF, mirrored NVR streams; tiler + reconnect; demo profile 4–16 cams/node." },
  { title: "Inference", body: "TensorRT engines for pose/violence/fire/object; DeepStream pipelines; intervals tuned per profile." },
  { title: "Rules engine", body: "ROI, dwell, line-cross, schedules; emits MQTT/REST events and structured logs." },
  { title: "Privacy firewall", body: "FRS threshold 0.47; embeddings encrypted; MTLS; signed updates." },
  { title: "Recorder", body: "Circular buffer with 3s pre/post; watermarking and export pipelines." },
  { title: "Observability", body: "Prometheus at :9100; Grafana dashboards; exporter traces OTA." },
];

export default function PlatformPage() {
  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-10 sm:px-10">
      <header className="space-y-3">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400 hdr">Platform</p>
        <h1 className="text-4xl font-semibold text-white hdr">Edge architecture with a privacy firewall.</h1>
        <p className="text-sm text-slate-300 max-w-3xl">
          Everything heavy runs on-site: ingest, inference, rules, and recorder. Only metadata leaves the node unless you
          choose to attach short clips.
        </p>
      </header>

      <Architecture />

      <section className="grid gap-4 sm:grid-cols-2">
        {specs.map((item) => (
          <div key={item.title} className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="hdr text-sm text-emerald-300">{item.title}</p>
            <p className="mt-2 text-sm text-slate-200">{item.body}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
