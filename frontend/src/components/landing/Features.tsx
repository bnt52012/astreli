"use client";

import { motion } from "framer-motion";

const FEATURES = [
  {
    title: "Ultra-realistic generation",
    description:
      "Gemini vision and Kling AI video pipeline produce frames indistinguishable from a professional shoot.",
    icon: (
      <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="14" cy="14" r="10" />
        <circle cx="14" cy="14" r="4" />
        <line x1="14" y1="2" x2="14" y2="4" />
        <line x1="14" y1="24" x2="14" y2="26" />
        <line x1="2" y1="14" x2="4" y2="14" />
        <line x1="24" y1="14" x2="26" y2="14" />
      </svg>
    ),
  },
  {
    title: "Brand consistency guaranteed",
    description:
      "LoRA fine-tuning ensures your brand ambassador appears with perfect likeness across every scene.",
    icon: (
      <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="14" cy="10" r="5" />
        <path d="M6 24 C6 19 10 16 14 16 C18 16 22 19 22 24" />
      </svg>
    ),
  },
  {
    title: "12 industries mastered",
    description:
      "Trained on 50,000+ luxury advertising analyses. From haute couture to fine jewelry, we speak your visual language.",
    icon: (
      <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="4" y="4" width="8" height="8" rx="1" />
        <rect x="16" y="4" width="8" height="8" rx="1" />
        <rect x="4" y="16" width="8" height="8" rx="1" />
        <rect x="16" y="16" width="8" height="8" rx="1" />
      </svg>
    ),
  },
  {
    title: "Multi-platform, one pipeline",
    description:
      "Instagram Reels, TikTok, YouTube pre-roll, TV broadcast. Every format rendered from a single scenario.",
    icon: (
      <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="2" y="6" width="16" height="12" rx="1.5" />
        <rect x="14" y="10" width="12" height="14" rx="1.5" />
      </svg>
    ),
  },
];

export default function Features() {
  return (
    <section className="py-28 md:py-36">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <p className="text-xs text-[#C4A265] tracking-[0.2em] uppercase mb-4">
            Capabilities
          </p>
          <h2 className="text-3xl md:text-5xl font-light text-[#1A1A1A] tracking-[-0.01em]">
            Engineered for excellence.
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-16 gap-y-16 max-w-[900px] mx-auto">
          {FEATURES.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 25 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
            >
              <div className="text-[#C4A265] mb-5">{feature.icon}</div>
              <h3 className="text-lg font-normal text-[#1A1A1A] mb-3 tracking-[-0.01em]">
                {feature.title}
              </h3>
              <p className="text-[15px] text-[#4A4A4A] font-light leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
