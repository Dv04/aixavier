'use client';

import { useEffect } from "react";

type Props = {
  children: React.ReactNode;
};

export default function Providers({ children }: Props) {
  // Enforce dark theme and allow future theme toggles without extra wiring.
  useEffect(() => {
    const root = document.documentElement;
    root.dataset.theme = "dark";
    root.classList.add("dark");
  }, []);

  return <>{children}</>;
}
