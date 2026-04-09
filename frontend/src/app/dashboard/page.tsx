"use client";

import { useState } from "react";
import ProjectForm from "@/components/ProjectForm";
import PipelineVisualizer from "@/components/PipelineVisualizer";
import VideoPlayer from "@/components/VideoPlayer";
import ProjectList from "@/components/ProjectList";
import { usePipeline } from "@/hooks/usePipeline";
import type { ProjectResponse } from "@/lib/api";

export default function Dashboard() {
  const [activeProject, setActiveProject] = useState<ProjectResponse | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const pipelineState = usePipeline(activeProject?.id ?? null);

  const handleCreated = (project: ProjectResponse) => {
    setActiveProject(project);
    setRefreshTrigger((n) => n + 1);
  };

  const handleSelectProject = (project: ProjectResponse) => {
    setActiveProject(project);
  };

  const isCompleted = pipelineState?.status === "completed";
  const videoUrl = pipelineState?.video_url || activeProject?.video_url;

  return (
    <div className="min-h-screen relative overflow-hidden" style={{ background: "#0d0d1a", color: "#e0e0f0", fontFamily: "'JetBrains Mono', monospace" }}>
      <div className="relative z-10 max-w-6xl mx-auto px-4 py-8">
        <header className="text-center mb-10">
          <h1 className="text-3xl font-extrabold tracking-[6px] uppercase" style={{ color: "#F59E0B" }}>
            AdGenAI
          </h1>
          <p className="text-[11px] tracking-[3px] mt-2" style={{ color: "#555570" }}>
            PIPELINE DE GENERATION PUBLICITAIRE 100% IA
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <aside className="lg:col-span-1">
            <ProjectList onSelect={handleSelectProject} refreshTrigger={refreshTrigger} />
          </aside>
          <main className="lg:col-span-3 space-y-8">
            {activeProject && (
              <section className="rounded-xl p-6 border" style={{ background: "#12122a", borderColor: "#2a2a4a" }}>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full animate-pulse" style={{ background: isCompleted ? "#10B981" : "#F59E0B" }} />
                    <h2 className="text-sm font-bold tracking-wider">PROJET {activeProject.id.slice(0, 8).toUpperCase()}</h2>
                  </div>
                  <span className="text-xs font-mono" style={{ color: "#555570" }}>
                    {Math.round((pipelineState?.progress ?? activeProject.progress) * 100)}%
                  </span>
                </div>
                <PipelineVisualizer state={pipelineState} />
              </section>
            )}
            {isCompleted && videoUrl && <VideoPlayer url={videoUrl} />}
            <section className="rounded-xl p-6 border" style={{ background: "#12122a", borderColor: "#2a2a4a" }}>
              <h2 className="text-sm font-bold tracking-widest mb-6" style={{ color: "#F59E0B" }}>NOUVEAU PROJET</h2>
              <ProjectForm onCreated={handleCreated} />
            </section>
          </main>
        </div>
      </div>
    </div>
  );
}
