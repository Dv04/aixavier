'use client';

import { useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const rawLogs = [
  "[ingest] INIT camera=CAM_WEB fps=25 profile=demo",
  "[ingest] CONNECTING rtsp://depot-cam-01 → NVMM zero-copy",
  "[ingest] STREAM UP codec=h264 tiler=2x2 drop-on-late=0",
  "[detector] pose rtmpose_m latency=25.5ms track=3 first_seen=1763013534.197",
  "[detector] pose rtmpose_m latency=52.3ms track=2 first_seen=1763013534.699",
  "[rules] pose.gesture=halt score=0.80 → emit event camera=CAM_WEB",
  "[privacy] FRS threshold=0.47 embeddings=encrypted audit=artifacts/privacy/frs_audit.log",
  "[exporter] metrics ready http://localhost:9100/metrics",
  "[recorder] circular_buffer pre=3s post=3s path=artifacts/recordings",
  "[events] mqtt publish topic=diagnostics/edge status=ok",
  "[ingest] LOADING fallback demo://synthetic when stream absent",
];

function useTypingEffect(lines: string[]) {
  const [completed, setCompleted] = useState<string[]>([]);
  const [current, setCurrent] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    let lineIdx = 0;
    let charIdx = 0;
    let timeout: ReturnType<typeof setTimeout> | undefined;

    const tick = () => {
      const line = lines[lineIdx];
      setCurrent(line.slice(0, charIdx + 1));
      charIdx += 1;

      if (charIdx >= line.length) {
        setCompleted((prev) => [...prev, line].slice(-10));
        setCurrent("");
        lineIdx += 1;
        charIdx = 0;
        if (lineIdx >= lines.length) {
          setDone(true);
          return;
        }
        const pause = /LOADING|CONNECTING/i.test(line) ? 400 : 140;
        timeout = setTimeout(tick, pause);
      } else {
        timeout = setTimeout(tick, 10);
      }
    };

    timeout = setTimeout(tick, 300);
    return () => {
      if (timeout) clearTimeout(timeout);
    };
  }, [lines]);

  return { completed, current, done };
}

export default function Terminal() {
  const logs = useMemo(() => rawLogs, []);
  const { completed, current, done } = useTypingEffect(logs);
  const viewportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (viewportRef.current) {
      viewportRef.current.scrollTop = viewportRef.current.scrollHeight;
    }
  }, [completed, current]);

  return (
    <div className="relative w-full overflow-hidden">
      <div className="flex items-center gap-2 pb-2 text-xs text-slate-400">
        <span className="h-2 w-2 rounded-full bg-orange-500 shadow-[0_0_12px_rgba(249,115,22,0.7)]" />
        <span className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.7)]" />
        <span className="h-2 w-2 rounded-full bg-slate-400" />
        <span className="font-mono uppercase tracking-[0.18em] text-slate-300">Edge Event Bus</span>
      </div>
      <div
        ref={viewportRef}
        className="max-h-48 overflow-hidden font-mono text-[12px] leading-relaxed text-emerald-200 whitespace-pre-wrap"
      >
        <AnimatePresence initial={false}>
          {completed.map((line, i) => (
            <motion.div
              key={`${line}-${i}`}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.18, ease: "easeOut" }}
              className="whitespace-pre"
            >
              <span className="text-cyan-300">$</span>{" "}
              <span className="text-slate-50">
                {line}
              </span>
            </motion.div>
          ))}
          {!done && current && (
            <motion.div
              key={`current-${current.length}`}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.12, ease: "easeOut" }}
              className="whitespace-pre"
            >
              <span className="text-cyan-300">$</span>{" "}
              <span className="text-slate-50">
                {current}
                <span className="animate-[blink_1s_steps(2,start)_infinite]">_</span>
              </span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
