"use client";

const LINKS = [
  { label: "About", href: "/about" },
  { label: "Pricing", href: "/pricing" },
  { label: "Contact", href: "/contact" },
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
];

const SOCIALS = [
  {
    label: "LinkedIn",
    href: "#",
    icon: (
      <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
        <path d="M2 4a2 2 0 1 1 4 0 2 2 0 0 1-4 0zm.5 3h3v9h-3V7zm5.5 0h2.9l.1 1.2C11.6 7.4 12.6 7 13.8 7 16 7 17 8.5 17 11v5h-3v-4.5c0-1.4-.5-2-1.5-2s-1.8.7-1.8 2V16H8V7z" />
      </svg>
    ),
  },
  {
    label: "Instagram",
    href: "#",
    icon: (
      <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
        <path d="M9 1.5c2 0 2.3 0 3.1.1.8 0 1.2.2 1.5.3.4.1.7.3 1 .6.3.3.5.6.6 1 .1.3.2.7.3 1.5 0 .8.1 1 .1 3.1s0 2.3-.1 3.1c0 .8-.2 1.2-.3 1.5-.1.4-.3.7-.6 1-.3.3-.6.5-1 .6-.3.1-.7.2-1.5.3-.8 0-1 .1-3.1.1s-2.3 0-3.1-.1c-.8 0-1.2-.2-1.5-.3-.4-.1-.7-.3-1-.6-.3-.3-.5-.6-.6-1-.1-.3-.2-.7-.3-1.5 0-.8-.1-1-.1-3.1s0-2.3.1-3.1c0-.8.2-1.2.3-1.5.1-.4.3-.7.6-1 .3-.3.6-.5 1-.6.3-.1.7-.2 1.5-.3.8 0 1-.1 3.1-.1zM9 0C6.9 0 6.6 0 5.8.1 5 .1 4.4.3 3.9.5c-.5.2-1 .5-1.4.9-.4.4-.7.9-.9 1.4C1.3 3.4 1.1 4 1.1 4.8 1 5.6 1 5.9 1 8s0 2.4.1 3.2c0 .8.2 1.4.4 1.9.2.5.5 1 .9 1.4.4.4.9.7 1.4.9.5.2 1.1.4 1.9.4.8.1 1.1.1 3.2.1s2.4 0 3.2-.1c.8 0 1.4-.2 1.9-.4.5-.2 1-.5 1.4-.9.4-.4.7-.9.9-1.4.2-.5.4-1.1.4-1.9.1-.8.1-1.1.1-3.2s0-2.4-.1-3.2c0-.8-.2-1.4-.4-1.9-.2-.5-.5-1-.9-1.4-.4-.4-.9-.7-1.4-.9C13.4.3 12.8.1 12 .1 11.4 0 11.1 0 9 0zm0 4.4a4.6 4.6 0 1 0 0 9.2 4.6 4.6 0 0 0 0-9.2zM9 12a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.8-7.8a1.1 1.1 0 1 0 0-2.2 1.1 1.1 0 0 0 0 2.2z" />
      </svg>
    ),
  },
  {
    label: "X",
    href: "#",
    icon: (
      <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
        <path d="M13.5 1.5h2.5l-5.5 6.3 6.5 8.6h-5l-4-5.2-4.5 5.2H1l5.9-6.7L.5 1.5h5.1l3.6 4.7 4.3-4.7zm-.9 13.4h1.4L5.5 2.9H4l8.6 12z" />
      </svg>
    ),
  },
];

export default function Footer() {
  return (
    <footer className="py-16 border-t border-[#E5E0D8]">
      <div className="max-w-[1200px] mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold tracking-[0.08em] text-[#1A1A1A] uppercase">
              Astreli
            </span>
            <span className="text-[9px] text-[#C4A265] font-medium tracking-widest uppercase mt-0.5">
              .ai
            </span>
          </div>

          {/* Links */}
          <nav className="flex items-center gap-8">
            {LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-xs text-[#8A8A8A] hover:text-[#1A1A1A] transition-colors duration-300 tracking-wide"
              >
                {link.label}
              </a>
            ))}
          </nav>

          {/* Socials */}
          <div className="flex items-center gap-5">
            {SOCIALS.map((social) => (
              <a
                key={social.label}
                href={social.href}
                aria-label={social.label}
                className="text-[#8A8A8A] hover:text-[#1A1A1A] transition-colors duration-300"
              >
                {social.icon}
              </a>
            ))}
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-xs text-[#8A8A8A]">
            &copy; 2026 Astreli. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
