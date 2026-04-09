"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";
import Logo from "@/components/Logo";

const NAV_LINKS = [
  { label: "Generate", href: "/generate" },
  { label: "LoRA Models", href: "/lora" },
];

export default function NavBar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-[#FAFAF8]/95 backdrop-blur-md border-b border-[#E5E0D8]">
      <div className="max-w-[1200px] mx-auto px-6 h-full flex items-center justify-between">
        {/* Left: Logo + Nav Links */}
        <div className="flex items-center gap-10">
          <Link href="/" className="flex items-center shrink-0">
            <Logo height={38} />
          </Link>

          {/* Desktop nav links */}
          <nav className="hidden md:flex items-center gap-8">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm tracking-wide transition-colors duration-300 ${
                  pathname === link.href
                    ? "text-[#1A1A1A] font-medium"
                    : "text-[#6A6A6A] hover:text-[#1A1A1A]"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* Right: Login + CTA (desktop) */}
        <div className="hidden md:flex items-center gap-6">
          <Link
            href="/login"
            className="text-sm text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-300 tracking-wide"
          >
            Login
          </Link>
          <Link
            href="/generate"
            className="px-6 py-2.5 bg-[#C4A265] text-white text-xs font-medium tracking-[0.1em] uppercase hover:bg-[#D4B87A] transition-colors duration-300"
          >
            Get Started
          </Link>
        </div>

        {/* Mobile: Hamburger */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden text-[#1A1A1A] p-1"
          aria-label="Menu"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            {mobileOpen ? (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            ) : (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5"
              />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile dropdown */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-[#FAFAF8] border-b border-[#E5E0D8] overflow-hidden"
          >
            <nav className="px-6 py-4 space-y-1">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className={`block py-3 text-sm tracking-wide transition-colors ${
                    pathname === link.href
                      ? "text-[#1A1A1A] font-medium"
                      : "text-[#6A6A6A]"
                  }`}
                >
                  {link.label}
                </Link>
              ))}
              <div className="pt-3 border-t border-[#E5E0D8] mt-2 space-y-3">
                <Link
                  href="/login"
                  onClick={() => setMobileOpen(false)}
                  className="block py-2 text-sm text-[#4A4A4A]"
                >
                  Login
                </Link>
                <Link
                  href="/generate"
                  onClick={() => setMobileOpen(false)}
                  className="block text-center py-3 bg-[#C4A265] text-white text-xs font-medium tracking-[0.1em] uppercase"
                >
                  Get Started
                </Link>
              </div>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
