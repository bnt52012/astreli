"use client";

import { useEffect, useState } from "react";
import { listProjects, type ProjectResponse } from "@/lib/api";

const STATUS_COLORS: Record<string, string> = {
  pending: "#555570",
  analyzing: "#8B5CF6",
  generating_images: "#3B82F6",
  generating_videos: "#10B981",
  assembling: "#F97316",
  completed: "#F59E0B",
  failed: "#EF4444",
};

const STATUS_LABELS: Record<string, string> = {
  pending: "En attente",
  analyzing: "Analyse...",
  generating_images: "Images...",
  generating_videos: "Vidéos...",
  assembling: "Montage...",
  completed: "Terminé",
  failed: "Échec",
};

interface Props {
  onSelect: (project: ProjectResponse) => void;
  refreshTrigger?: number;
}

export default function ProjectList({ onSelect, refreshTrigger }: Props) {
  const [projects, setProjects] = useState<ProjectResponse[]>([]);

  useEffect(() => {
    listProjects().then(setProjects).catch(() => {});
  }, [refreshTrigger]);

  if (projects.length === 0) return null;

  return (
    <div className="space-y-2">
      <h3 className="text-xs font-bold tracking-widest mb-3" style={{ color: "var(--text-muted)" }}>
        PROJETS RÉCENTS
      </h3>
      {projects.map((p) => {
        const color = STATUS_COLORS[p.status] || "#555570";
        return (
          <button
            key={p.id}
            onClick={() => onSelect(p)}
            className="w-full text-left p-3 rounded-lg border transition-all hover:border-opacity-100"
            style={{
              background: "var(--bg-card)",
              borderColor: color + "44",
            }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full" style={{ background: color }} />
                <span className="text-xs font-mono" style={{ color: "var(--text-secondary)" }}>
                  {p.id.slice(0, 8)}...
                </span>
              </div>
              <span className="text-[10px] font-bold tracking-wider" style={{ color }}>
                {STATUS_LABELS[p.status] || p.status}
              </span>
            </div>
            <div className="mt-1 flex items-center justify-between">
              <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>
                {p.scenes_count} scènes • {p.mode === "character_product" ? "Perso+Produit" : "Produit"}
              </span>
              <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>
                {Math.round(p.progress * 100)}%
              </span>
            </div>
          </button>
        );
      })}
    </div>
  );
}
