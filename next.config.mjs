import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const nextConfig = {
  reactCompiler: true,
  turbopack: {
    root: __dirname,
  },
  serverExternalPackages: ["lightningcss", "lightningcss-darwin-arm64"],
  reactStrictMode: true,
};

export default nextConfig;
