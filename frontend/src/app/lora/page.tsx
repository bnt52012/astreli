"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { getLoraModels, deleteLora } from "@/lib/api";
import type { LoRAModel } from "@/lib/api";
import Logo from "@/components/Logo";

// ── Sidebar ─────────────────────────────────────────────────────────────

function Sidebar() {
  const navItems = [
    { label: "New Project", href: "/generate", active: false, disabled: false },
    { label: "My Videos", href: "#", active: false, disabled: true },
    { label: "LoRA Models", href: "/lora", active: true, disabled: false },
    { label: "Settings", href: "#", active: false, disabled: true },
  ];

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-[280px] bg-white border-r border-[#E5E0D8] flex flex-col z-50">
      {/* Logo */}
      <div className="px-8 py-8">
        <Link href="/" className="block">
          <Logo height={40} />
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.label}
            href={item.disabled ? "#" : item.href}
            className={`
              flex items-center px-4 py-3 text-sm transition-colors relative
              ${item.active
                ? "text-[#1A1A1A] font-medium bg-[#FAFAF8]"
                : item.disabled
                  ? "text-[#8A8A8A] cursor-not-allowed"
                  : "text-[#4A4A4A] hover:text-[#1A1A1A] hover:bg-[#FAFAF8]"
              }
            `}
            onClick={item.disabled ? (e) => e.preventDefault() : undefined}
          >
            {item.active && (
              <span className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 bg-[#C4A265] rounded-r" />
            )}
            {item.label}
          </Link>
        ))}
      </nav>

      {/* User */}
      <div className="px-8 py-6 border-t border-[#E5E0D8]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-[#C4A265] flex items-center justify-center text-white text-xs font-medium">
            AB
          </div>
          <span className="text-sm text-[#4A4A4A]">Account</span>
        </div>
      </div>
    </aside>
  );
}

// ── Confirmation Dialog ─────────────────────────────────────────────────

function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel,
  danger,
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  message: string;
  confirmLabel: string;
  danger?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/30" onClick={onCancel} />
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="relative bg-white border border-[#E5E0D8] p-8 max-w-md w-full mx-4 shadow-lg"
      >
        <h3 className="text-lg font-medium text-[#1A1A1A] mb-2">{title}</h3>
        <p className="text-sm text-[#4A4A4A] mb-6">{message}</p>
        <div className="flex gap-3 justify-end">
          <button
            onClick={onCancel}
            className="px-6 py-2.5 text-sm text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className={`px-6 py-2.5 text-sm font-medium tracking-[0.05em] uppercase transition-colors ${
              danger
                ? "bg-red-600 text-white hover:bg-red-700"
                : "bg-[#C4A265] text-white hover:bg-[#D4B87A]"
            }`}
          >
            {confirmLabel}
          </button>
        </div>
      </motion.div>
    </div>
  );
}

// ── Upload Icon SVG ─────────────────────────────────────────────────────

function UploadIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      width="40"
      height="40"
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M20 28V12M20 12L14 18M20 12L26 18"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M8 28V32H32V28"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

// ── Main Page ───────────────────────────────────────────────────────────

type TrainingState = "idle" | "training" | "complete";

export default function LoRAPage() {
  // Upload state
  const [photos, setPhotos] = useState<{ file: File; preview: string }[]>([]);
  const [modelName, setModelName] = useState("");
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Training state
  const [trainingState, setTrainingState] = useState<TrainingState>("idle");
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [confirmTrain, setConfirmTrain] = useState(false);

  // Models state
  const [models, setModels] = useState<LoRAModel[]>([]);
  const [modelsLoading, setModelsLoading] = useState(true);
  const [deleteTarget, setDeleteTarget] = useState<LoRAModel | null>(null);

  // ── Fetch models on mount ──────────────────────────────────────────
  const fetchModels = useCallback(async () => {
    try {
      const data = await getLoraModels();
      setModels(data);
    } catch {
      // API not available yet — that's fine
    } finally {
      setModelsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchModels();
  }, [fetchModels]);

  // ── File handling ──────────────────────────────────────────────────
  const addFiles = useCallback((files: FileList | File[]) => {
    const fileArray = Array.from(files).filter((f) =>
      f.type.startsWith("image/")
    );
    fileArray.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPhotos((prev) => {
          if (prev.some((p) => p.file.name === file.name && p.file.size === file.size)) {
            return prev;
          }
          return [...prev, { file, preview: e.target?.result as string }];
        });
      };
      reader.readAsDataURL(file);
    });
  }, []);

  const removePhoto = useCallback((index: number) => {
    setPhotos((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      if (e.dataTransfer.files.length > 0) {
        addFiles(e.dataTransfer.files);
      }
    },
    [addFiles]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        addFiles(e.target.files);
      }
    },
    [addFiles]
  );

  // ── Training ───────────────────────────────────────────────────────
  const canStartTraining = photos.length >= 10 && modelName.trim().length > 0 && trainingState === "idle";

  const startTraining = async () => {
    setConfirmTrain(false);
    setTrainingState("training");
    setTrainingProgress(0);

    // Fire the API call (non-blocking, OK if it fails in demo)
    fetch("/api/lora/train", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_name: modelName.trim() }),
    }).catch(() => {});

    // Simulate progress over ~20 seconds
    const interval = setInterval(() => {
      setTrainingProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTrainingState("complete");
          fetchModels();
          return 100;
        }
        return prev + 5;
      });
    }, 1000);
  };

  // ── Delete model ───────────────────────────────────────────────────
  const handleDelete = async (model: LoRAModel) => {
    try {
      await deleteLora(model.model_id);
      setModels((prev) => prev.filter((m) => m.model_id !== model.model_id));
    } catch {
      // Silently fail for now
    }
    setDeleteTarget(null);
  };

  // ── Render ─────────────────────────────────────────────────────────
  const photoMinimum = 10;
  const photoCount = photos.length;
  const progressPercent = Math.min((photoCount / photoMinimum) * 100, 100);

  return (
    <div className="min-h-screen bg-[#FAFAF8]" style={{ fontFamily: "Inter, sans-serif" }}>
      <Sidebar />

      {/* Main content */}
      <main className="ml-[280px] min-h-screen">
        <div className="max-w-4xl mx-auto px-12 py-16 space-y-16">
          {/* ── Section 1: Header ────────────────────────────────── */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-3xl font-light text-[#1A1A1A] mb-4">
              Train Your Brand Model
            </h1>
            <p className="text-[#4A4A4A] font-light leading-relaxed max-w-2xl">
              Upload 10-20 photos of your brand ambassador. Our AI will learn
              their face for perfect consistency across all campaigns.
            </p>
          </motion.section>

          {/* ── Section 2: Upload & Train ─────────────────────────── */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="space-y-8"
          >
            {/* Drag & Drop Zone */}
            <div
              onClick={() => fileInputRef.current?.click()}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              className={`
                border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors
                ${isDragOver
                  ? "border-[#C4A265] bg-[#C4A265]/5"
                  : "border-[#E5E0D8] hover:border-[#C4A265]/50"
                }
              `}
            >
              <UploadIcon
                className={`mx-auto mb-4 ${isDragOver ? "text-[#C4A265]" : "text-[#8A8A8A]"}`}
              />
              <p className="text-sm text-[#1A1A1A] mb-1">
                Drop photos here or click to browse
              </p>
              <p className="text-xs text-[#8A8A8A]">
                10-20 photos recommended. Front face, profile, 3/4 view, full body.
              </p>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                className="hidden"
                onChange={handleFileSelect}
              />
            </div>

            {/* Image Preview Grid */}
            {photos.length > 0 && (
              <div>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-4">
                  <AnimatePresence>
                    {photos.map((photo, index) => (
                      <motion.div
                        key={photo.file.name + photo.file.size}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        className="relative aspect-square rounded-lg overflow-hidden group"
                      >
                        <img
                          src={photo.preview}
                          alt={`Upload ${index + 1}`}
                          className="w-full h-full object-cover"
                        />
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            removePhoto(index);
                          }}
                          className="absolute top-2 right-2 w-6 h-6 bg-black/60 text-white rounded-full flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity hover:bg-black/80"
                        >
                          &times;
                        </button>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>

                {/* Photo count & progress */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-[#4A4A4A]">
                      {photoCount} / {photoMinimum} minimum photos
                    </span>
                    {photoCount >= photoMinimum && (
                      <span className="text-[#C4A265] text-xs font-medium">Ready</span>
                    )}
                  </div>
                  <div className="w-full h-1.5 bg-[#E5E0D8] rounded-full overflow-hidden">
                    <div
                      className="h-full bg-[#C4A265] rounded-full transition-all duration-300"
                      style={{ width: `${progressPercent}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Model Name Input */}
            <div>
              <label className="block text-sm text-[#1A1A1A] mb-2">
                Model Name
              </label>
              <input
                type="text"
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                placeholder="e.g., Sophie Martin"
                className="w-full bg-white border border-[#E5E0D8] px-4 py-3 text-sm text-[#1A1A1A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-none"
              />
            </div>

            {/* Training Button / Progress */}
            {trainingState === "idle" && (
              <button
                disabled={!canStartTraining}
                onClick={() => setConfirmTrain(true)}
                className="bg-[#C4A265] text-white text-sm font-medium tracking-[0.05em] uppercase px-8 py-3 hover:bg-[#D4B87A] transition-colors disabled:bg-[#E5E0D8] disabled:text-[#8A8A8A] disabled:cursor-not-allowed"
              >
                Start Training
              </button>
            )}

            {trainingState === "training" && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-3"
              >
                <p className="text-sm text-[#4A4A4A]">
                  Training your model... This typically takes 15-20 minutes.
                </p>
                <div className="w-full h-2 bg-[#E5E0D8] rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-[#C4A265] rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${trainingProgress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
                <p className="text-xs text-[#8A8A8A]">{trainingProgress}%</p>
              </motion.div>
            )}

            {trainingState === "complete" && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white border border-[#E5E0D8] p-6"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-[#C4A265]/10 flex items-center justify-center">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path
                        d="M3 8.5L6.5 12L13 4"
                        stroke="#C4A265"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-[#1A1A1A]">
                      Your model is ready!
                    </p>
                    <p className="text-xs text-[#8A8A8A]">
                      You can now use it in projects.
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.section>

          {/* ── Section 3: My Models ──────────────────────────────── */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-6"
          >
            <h2 className="text-xl font-light text-[#1A1A1A]">Your Models</h2>

            {modelsLoading ? (
              <div className="text-sm text-[#8A8A8A]">Loading models...</div>
            ) : models.length === 0 ? (
              <p className="text-sm text-[#8A8A8A]">
                No models trained yet. Upload photos above to get started.
              </p>
            ) : (
              <div className="space-y-4">
                {models.map((model) => (
                  <div
                    key={model.model_id}
                    className="bg-white border border-[#E5E0D8] p-6"
                  >
                    <div className="flex items-start justify-between">
                      <div className="space-y-2">
                        <h3 className="text-sm font-semibold text-[#1A1A1A]">
                          {model.name}
                        </h3>
                        <p className="text-xs font-mono text-[#8A8A8A]">
                          {model.trigger_word}
                        </p>
                        <div className="flex items-center gap-3">
                          {model.status === "ready" ? (
                            <span className="inline-flex items-center gap-1.5 text-xs text-[#6B7C5E] bg-[#6B7C5E]/10 px-2.5 py-1 rounded-full">
                              <span className="w-1.5 h-1.5 rounded-full bg-[#6B7C5E]" />
                              Ready
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 text-xs text-[#C4A265] bg-[#C4A265]/10 px-2.5 py-1 rounded-full">
                              <span className="w-1.5 h-1.5 rounded-full bg-[#C4A265] animate-pulse" />
                              Training
                            </span>
                          )}
                          <span className="text-xs text-[#8A8A8A]">
                            {new Date(model.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3 shrink-0">
                        <Link
                          href={`/generate?lora=${model.model_id}`}
                          className="bg-[#C4A265] text-white text-xs font-medium tracking-[0.05em] uppercase px-5 py-2 hover:bg-[#D4B87A] transition-colors"
                        >
                          Use in Project
                        </Link>
                        <button
                          onClick={() => setDeleteTarget(model)}
                          className="text-sm text-[#8A8A8A] hover:text-red-600 transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.section>
        </div>
      </main>

      {/* Confirmation Dialogs */}
      <ConfirmDialog
        open={confirmTrain}
        title="Start Training"
        message="Training takes 15-20 minutes. Continue?"
        confirmLabel="Start Training"
        onConfirm={startTraining}
        onCancel={() => setConfirmTrain(false)}
      />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Delete Model"
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This cannot be undone.`}
        confirmLabel="Delete"
        danger
        onConfirm={() => deleteTarget && handleDelete(deleteTarget)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
