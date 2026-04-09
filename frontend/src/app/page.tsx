import Hero from "@/components/landing/Hero";
import BrandAnalysis from "@/components/landing/BrandAnalysis";
import SocialProof from "@/components/landing/SocialProof";
import HowItWorks from "@/components/landing/HowItWorks";
import Comparison from "@/components/landing/Comparison";
import Features from "@/components/landing/Features";
import DemoVideo from "@/components/landing/DemoVideo";
import Waitlist from "@/components/landing/Waitlist";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <>
      <main>
        <Hero />
        <BrandAnalysis />
        <SocialProof />
        <HowItWorks />
        <Comparison />
        <Features />
        <DemoVideo />
        <Waitlist />
      </main>
      <Footer />
    </>
  );
}
