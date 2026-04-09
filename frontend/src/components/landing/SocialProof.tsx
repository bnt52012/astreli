"use client";

import { motion } from "framer-motion";

export default function SocialProof() {
  return (
    <section className="py-20 border-t border-[#E5E0D8]">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.8 }}
          className="text-center text-sm text-[#8A8A8A] tracking-[0.12em]"
        >
          Built for the world&apos;s most prestigious brands.
        </motion.p>
      </div>
    </section>
  );
}
