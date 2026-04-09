"use client";

import { motion } from "framer-motion";

const STEPS = [
  {
    number: "01",
    title: "Write your scenario",
    description:
      "Describe your vision in plain language. Our AI understands your creative intent, your brand, and your audience.",
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="6" y="4" width="20" height="24" rx="2" />
        <line x1="10" y1="10" x2="22" y2="10" />
        <line x1="10" y1="14" x2="22" y2="14" />
        <line x1="10" y1="18" x2="18" y2="18" />
      </svg>
    ),
  },
  {
    number: "02",
    title: "AI generates every scene",
    description:
      "Our pipeline analyzes, decomposes, and renders each scene with cinematic precision. No compromises.",
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="4" y="6" width="24" height="20" rx="2" />
        <polygon points="13,12 13,22 22,17" fill="currentColor" opacity="0.3" />
        <polygon points="13,12 13,22 22,17" />
      </svg>
    ),
  },
  {
    number: "03",
    title: "Download your video",
    description:
      "Broadcast-ready in every format. Instagram, TikTok, YouTube, TV. One click, all platforms.",
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M16 4 L16 22" />
        <polyline points="10,17 16,23 22,17" />
        <line x1="6" y1="28" x2="26" y2="28" />
      </svg>
    ),
  },
];

export default function HowItWorks() {
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
            How it works
          </p>
          <h2 className="text-3xl md:text-5xl font-light text-[#1A1A1A] tracking-[-0.01em]">
            Three steps. Infinite possibilities.
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-16 md:gap-12">
          {STEPS.map((step, i) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.7, delay: i * 0.15 }}
              className="text-center md:text-left"
            >
              <div className="text-[#C4A265] mb-6 flex justify-center md:justify-start">
                {step.icon}
              </div>
              <p className="text-xs text-[#8A8A8A] tracking-[0.2em] uppercase mb-3">
                Step {step.number}
              </p>
              <h3 className="text-xl md:text-2xl font-normal text-[#1A1A1A] mb-4 tracking-[-0.01em]">
                {step.title}
              </h3>
              <p className="text-[15px] text-[#4A4A4A] font-light leading-relaxed">
                {step.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
