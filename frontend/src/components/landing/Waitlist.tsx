"use client";

import { motion } from "framer-motion";
import { useState } from "react";

export default function Waitlist() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubmitted(true);
    }
  };

  return (
    <section id="waitlist" className="py-28 md:py-36 bg-[#1A1A1A]">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.8 }}
          className="max-w-[600px] mx-auto text-center"
        >
          <p className="text-xs text-[#C4A265] tracking-[0.2em] uppercase mb-4">
            Early Access
          </p>
          <h2 className="text-3xl md:text-4xl font-light text-[#FAFAF8] tracking-[-0.01em] mb-6">
            Be among the first to
            <br />
            revolutionize your advertising.
          </h2>
          <p className="text-[15px] text-[#999] font-light mb-12">
            Currently in private beta. Limited spots available.
          </p>

          {!submitted ? (
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
                className="flex-1 px-6 py-4 bg-[#2A2A2A] border border-[#333] text-[#FAFAF8] text-sm tracking-wide placeholder:text-[#666] focus:outline-none focus:border-[#C4A265]/50 transition-colors duration-300"
              />
              <button
                type="submit"
                className="px-10 py-4 bg-[#C4A265] text-[#1A1A1A] text-sm font-medium tracking-[0.1em] uppercase hover:bg-[#D4B87A] transition-colors duration-300 whitespace-nowrap"
              >
                Request Access
              </button>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="py-6"
            >
              <p className="text-[#C4A265] text-sm tracking-wide">
                Thank you. We&apos;ll be in touch soon.
              </p>
            </motion.div>
          )}

          <p className="text-xs text-[#555] mt-6">
            No spam. Unsubscribe anytime.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
