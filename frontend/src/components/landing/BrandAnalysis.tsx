"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function BrandAnalysis() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    try {
      const res = await fetch("/api/analyze-brand", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim() }),
      });

      if (res.ok) {
        const data = await res.json();
        const params = new URLSearchParams({
          brand: data.brand_name || "",
          industry: data.industry || "",
        });
        router.push(`/generate?${params.toString()}`);
      } else {
        router.push("/generate");
      }
    } catch {
      router.push("/generate");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="py-24 md:py-32">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.8 }}
          className="max-w-[560px] mx-auto text-center"
        >
          <h2 className="text-3xl md:text-4xl font-light text-[#1A1A1A] tracking-[-0.01em] mb-10">
            Start creating in seconds
          </h2>

          <form onSubmit={handleAnalyze} className="space-y-5">
            <div className="relative">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="www.yourbrand.com"
                className="w-full px-6 py-4 bg-white border border-[#E5E0D8] text-[#1A1A1A] text-sm tracking-wide placeholder:text-[#8A8A8A] focus:outline-none focus:border-[#C4A265] transition-colors duration-300"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 text-sm font-medium tracking-[0.1em] uppercase text-white transition-all duration-500 disabled:opacity-60"
              style={{
                background: loading
                  ? "#8A8A8A"
                  : "linear-gradient(135deg, #C4A265 0%, #D4B275 100%)",
              }}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-3">
                  <svg
                    className="animate-spin h-4 w-4"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <circle
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="2"
                      opacity="0.3"
                    />
                    <path
                      d="M12 2a10 10 0 0 1 10 10"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                  Analyzing...
                </span>
              ) : (
                "Analyze"
              )}
            </button>
          </form>

          <a
            href="/generate"
            className="inline-block mt-6 text-xs text-[#8A8A8A] hover:text-[#C4A265] transition-colors duration-300 tracking-wide"
          >
            Skip and enter input manually
          </a>
        </motion.div>
      </div>
    </section>
  );
}
