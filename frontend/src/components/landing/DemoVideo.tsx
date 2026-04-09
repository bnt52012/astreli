"use client";

import { motion } from "framer-motion";

export default function DemoVideo() {
  return (
    <section className="py-28 md:py-36 border-t border-[#E5E0D8]">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <p className="text-xs text-[#C4A265] tracking-[0.2em] uppercase mb-4">
            Demo
          </p>
          <h2 className="text-3xl md:text-5xl font-light text-[#1A1A1A] tracking-[-0.01em]">
            See Astreli in action.
          </h2>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="max-w-[900px] mx-auto"
        >
          {/* Video placeholder */}
          <div className="relative aspect-video bg-[#1A1A1A] group cursor-pointer overflow-hidden">
            {/* Subtle border */}
            <div className="absolute inset-0 border border-[#333]" />

            {/* Play button */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-20 h-20 rounded-full border border-[#C4A265]/40 flex items-center justify-center group-hover:border-[#C4A265] group-hover:bg-[#C4A265]/10 transition-all duration-500">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  className="ml-1"
                >
                  <polygon
                    points="6,3 20,12 6,21"
                    fill="#C4A265"
                    opacity="0.8"
                  />
                </svg>
              </div>
            </div>

            {/* Astreli watermark */}
            <div className="absolute bottom-6 right-6">
              <span className="text-xs text-[#666] tracking-[0.15em] uppercase">
                astreli.ai
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
