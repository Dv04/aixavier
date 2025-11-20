import Hero from "../components/Hero";
import WedgeTabs from "../components/WedgeTabs";
import SocialProof from "@/components/sections/home/SocialProof";
import PatternsTeaser from "@/components/sections/home/PatternsTeaser";
import ArchitectureTeaser from "@/components/sections/home/ArchitectureTeaser";
import SecurityTeaser from "@/components/sections/home/SecurityTeaser";
import CTA from "@/components/sections/home/CTA";
import ValueProps from "@/components/sections/home/ValueProps";

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col gap-6">
      <Hero />
      <SocialProof />
      <ValueProps />
      <PatternsTeaser />
      <ArchitectureTeaser />
      <SecurityTeaser />
      <CTA />
    </main>
  );
}
