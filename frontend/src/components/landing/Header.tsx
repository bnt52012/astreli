"use client";

import { useState, useEffect } from "react";
import { clsx } from "clsx";
import Logo from "@/components/Logo";

export default function Header() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={clsx(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-500",
        scrolled
          ? "bg-[#FAFAF8]/90 backdrop-blur-md border-b border-[#E5E0D8]"
          : "bg-transparent"
      )}
    >
      <div className="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center group">
          <Logo height={44} />
        </a>

        {/* Right nav */}
        <div className="flex items-center gap-6">
          <a
            href="/login"
            className="text-sm text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-300 tracking-wide"
          >
            Login
          </a>
          <a
            href="/generate"
            className="hidden sm:inline-block px-6 py-2.5 bg-[#1A1A1A] text-[#FAFAF8] text-xs font-medium tracking-[0.1em] uppercase hover:bg-[#C4A265] transition-colors duration-500"
          >
            Get Started
          </a>
        </div>
      </div>
    </header>
  );
}
