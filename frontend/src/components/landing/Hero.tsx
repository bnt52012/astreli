"use client";

import { motion } from "framer-motion";
import Logo from "@/components/Logo";

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Subtle animated gradient background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[#FAFAF8]" />
        <div
          className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full opacity-[0.04]"
          style={{
            background:
              "radial-gradient(circle, #C4A265 0%, transparent 70%)",
            animation: "pulse-slow 8s ease-in-out infinite",
          }}
        />
        <div
          className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] rounded-full opacity-[0.03]"
          style={{
            background:
              "radial-gradient(circle, #C4A265 0%, transparent 70%)",
            animation: "pulse-slow 12s ease-in-out infinite reverse",
          }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-[1200px] mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
          className="mb-10 flex justify-center"
        >
          <Logo height={48} />
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-[#C4A265] text-sm font-medium tracking-[0.2em] uppercase mb-8"
        >
          The future of advertising
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.4 }}
          className="text-5xl sm:text-6xl md:text-7xl lg:text-[5.5rem] font-light text-[#1A1A1A] leading-[1.1] tracking-[-0.02em] mb-8"
        >
          Your next campaign,
          <br />
          <span className="italic font-light">powered by AI.</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.7 }}
          className="text-lg md:text-xl text-[#4A4A4A] font-light max-w-xl mx-auto mb-12 leading-relaxed"
        >
          From scenario to broadcast-ready video in minutes.
          <br className="hidden sm:block" /> Not months.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1 }}
        >
          <a
            href="#waitlist"
            className="inline-block px-10 py-4 bg-[#1A1A1A] text-[#FAFAF8] text-sm font-medium tracking-[0.1em] uppercase rounded-none hover:bg-[#C4A265] transition-colors duration-500"
          >
            Request Early Access
          </a>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2, duration: 1 }}
          className="absolute bottom-12 left-1/2 -translate-x-1/2"
        >
          <div className="w-[1px] h-12 bg-gradient-to-b from-transparent via-[#C4A265] to-transparent opacity-40 animate-pulse" />
        </motion.div>
      </div>

      <style jsx>{`
        @keyframes pulse-slow {
          0%,
          100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.04;
          }
          50% {
            transform: translate(-50%, -50%) scale(1.15);
            opacity: 0.07;
          }
        }
      `}</style>
    </section>
  );
}
