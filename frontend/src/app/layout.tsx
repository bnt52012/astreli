import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Astreli — AI-Powered Advertising",
  description:
    "From scenario to broadcast-ready video in minutes. Astreli replaces traditional ad shoots with a 100% AI pipeline.",
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  openGraph: {
    title: "Astreli — AI-Powered Advertising",
    description:
      "From scenario to broadcast-ready video in minutes. Not months.",
    url: "https://astreli.ai",
    siteName: "Astreli",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
