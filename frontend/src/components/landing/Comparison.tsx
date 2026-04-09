"use client";

import { motion } from "framer-motion";

const TRADITIONAL = [
  { label: "Budget", value: "€10,000 +" },
  { label: "Timeline", value: "1 week" },
  { label: "Team", value: "15+ people" },
  { label: "Weather", value: "Dependent" },
  { label: "Iterations", value: "2-3 max" },
  { label: "Platforms", value: "Re-shoot needed" },
];

const ASTRELI = [
  { label: "Budget", value: "From €1,200" },
  { label: "Timeline", value: "1 hour" },
  { label: "Team", value: "Just you" },
  { label: "Weather", value: "Always perfect" },
  { label: "Iterations", value: "Unlimited" },
  { label: "Platforms", value: "All formats, one click" },
];

export default function Comparison() {
  return (
    <section className="py-28 md:py-36 bg-[#1A1A1A]">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <p className="text-xs text-[#C4A265] tracking-[0.2em] uppercase mb-4">
            The new standard
          </p>
          <h2 className="text-3xl md:text-5xl font-light text-[#FAFAF8] tracking-[-0.01em]">
            Everything changes.
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-0 max-w-[900px] mx-auto">
          {/* Traditional */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.7 }}
            className="border border-[#333] p-10 md:p-12"
          >
            <p className="text-xs text-[#666] tracking-[0.2em] uppercase mb-8">
              Traditional Shoot
            </p>
            <div className="space-y-6">
              {TRADITIONAL.map((item) => (
                <div key={item.label} className="flex justify-between items-baseline">
                  <span className="text-sm text-[#666] font-light">
                    {item.label}
                  </span>
                  <span className="text-sm text-[#999] font-light">
                    {item.value}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Astreli */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="border border-[#C4A265]/30 bg-[#C4A265]/[0.04] p-10 md:p-12"
          >
            <p className="text-xs text-[#C4A265] tracking-[0.2em] uppercase mb-8">
              Astreli
            </p>
            <div className="space-y-6">
              {ASTRELI.map((item) => (
                <div key={item.label} className="flex justify-between items-baseline">
                  <span className="text-sm text-[#999] font-light">
                    {item.label}
                  </span>
                  <span className="text-sm text-[#FAFAF8] font-normal">
                    {item.value}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
