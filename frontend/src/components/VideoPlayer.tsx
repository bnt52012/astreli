"use client";

export default function VideoPlayer({ url }: { url: string }) {
  return (
    <div className="relative rounded-xl overflow-hidden border" style={{ borderColor: "var(--accent-amber)44" }}>
      <div className="absolute top-3 left-3 flex items-center gap-2 z-10">
        <div
          className="w-2 h-2 rounded-full animate-pulse"
          style={{ background: "#10B981", boxShadow: "0 0 8px #10B98188" }}
        />
        <span className="text-[10px] font-bold tracking-wider" style={{ color: "#10B981" }}>
          VIDÉO PRÊTE
        </span>
      </div>
      <video
        src={url}
        controls
        className="w-full aspect-video bg-black"
        poster=""
      />
      <div className="p-3 flex items-center justify-between" style={{ background: "var(--bg-card)" }}>
        <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>
          H.264 • 1080p • Qualité professionnelle
        </span>
        <a
          href={url}
          download
          className="text-[10px] font-bold px-3 py-1 rounded-full transition-all hover:opacity-80"
          style={{ background: "var(--accent-amber)22", color: "var(--accent-amber)" }}
        >
          TÉLÉCHARGER
        </a>
      </div>
    </div>
  );
}
