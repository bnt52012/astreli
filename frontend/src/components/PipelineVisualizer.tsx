"use client";

import { type PipelineUpdate } from "@/lib/api";
import clsx from "clsx";

const STEPS = [
  { key: "pending", label: "INIT", color: "#555570" },
  { key: "analyzing", label: "ANALYSE", color: "#8B5CF6" },
  { key: "generating_images", label: "IMAGES", color: "#3B82F6" },
  { key: "generating_videos", label: "VIDÉOS", color: "#10B981" },
  { key: "assembling", label: "MONTAGE", color: "#F97316" },
  { key: "completed", label: "TERMINÉ", color: "#F59E0B" },
];

function getStepIndex(status: string): number {
  const idx = STEPS.findIndex((s) => s.key === status);
  return idx >= 0 ? idx : 0;
}

export default function PipelineVisualizer({ state }: { state: PipelineUpdate | null }) {
  const currentStep = state ? getStepIndex(state.status) : 0;
  const isFailed = state?.status === "failed";

  return (
    <div className="w-full">
      {/* Progress bar */}
      <div className="relative h-2 rounded-full overflow-hidden mb-6"
        style={{ background: "var(--bg-card)" }}>
        <div
          className="h-full rounded-full transition-all duration-700 ease-out"
          style={{
            width: `${(state?.progress ?? 0) * 100}%`,
            background: isFailed
              ? "#EF4444"
              : `linear-gradient(90deg, #8B5CF6, #3B82F6, #10B981, #F59E0B)`,
          }}
        />
      </div>

      {/* Step indicators */}
      <div className="flex justify-between items-center gap-1">
        {STEPS.map((step, i) => {
          const isActive = i === currentStep;
          const isDone = i < currentStep;
          const color = isFailed && isActive ? "#EF4444" : step.color;

          return (
            <div key={step.key} className="flex flex-col items-center flex-1">
              <div
                className={clsx(
                  "w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-500",
                  isActive && "ring-2 ring-offset-2 ring-offset-[#0d0d1a] scale-110",
                )}
                style={{
                  background: isDone || isActive ? color + "33" : "var(--bg-card)",
                  borderColor: isDone || isActive ? color : "var(--border)",
                  borderWidth: 2,
                  color: isDone || isActive ? color : "var(--text-muted)",
                  ringColor: isActive ? color : undefined,
                }}
              >
                {isDone ? "✓" : i + 1}
              </div>
              <span
                className="mt-2 text-[10px] font-semibold tracking-wider"
                style={{ color: isDone || isActive ? color : "var(--text-muted)" }}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Scene grid */}
      {state && state.scenes.length > 0 && (
        <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {state.scenes.map((scene) => (
            <div
              key={scene.id}
              className="rounded-lg p-3 border transition-all"
              style={{
                background: "var(--bg-card)",
                borderColor: scene.status === "video_ready"
                  ? "#10B98166"
                  : scene.error
                  ? "#EF444466"
                  : "var(--border)",
              }}
            >
              <div className="flex items-center gap-2 mb-1">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{
                    background: scene.type === "character" ? "#3B82F6" : "#06B6D4",
                  }}
                />
                <span className="text-[10px] font-bold" style={{ color: "var(--text-secondary)" }}>
                  SCÈNE {scene.id}
                </span>
              </div>
              <div className="text-[9px] uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                {scene.type === "character" ? "Personnage" : "Produit"}
              </div>
              <div
                className="mt-1 text-[10px] font-semibold"
                style={{
                  color: scene.error
                    ? "#EF4444"
                    : scene.status === "video_ready"
                    ? "#10B981"
                    : scene.status === "image_ready"
                    ? "#3B82F6"
                    : "var(--text-muted)",
                }}
              >
                {scene.error
                  ? "ERREUR"
                  : scene.status === "video_ready"
                  ? "PRÊT"
                  : scene.status === "image_ready"
                  ? "IMAGE ✓"
                  : "EN ATTENTE"}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error display */}
      {state?.error && (
        <div className="mt-4 p-3 rounded-lg border border-red-500/30 bg-red-500/10 text-red-400 text-sm">
          {state.error}
        </div>
      )}
    </div>
  );
}
