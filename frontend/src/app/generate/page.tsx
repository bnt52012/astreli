"use client";

import { useState, useEffect, useRef, useCallback, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { clsx } from "clsx";
import {
  analyzeScenario,
  generateVideo,
  getJobStatus,
  getJobResult,
  getLoraModels,
  type Scene,
  type SceneBreakdown,
  type LoRAModel,
  type GenerateRequest,
} from "@/lib/api";
import Logo from "@/components/Logo";

// ── Constants ────────────────────────────────────────────────────────

const PRODUCT_CATEGORIES = [
  { value: "luxury", label: "Luxury" },
  { value: "beauty", label: "Beauty" },
  { value: "fragrance", label: "Fragrance" },
  { value: "jewelry_watches", label: "Jewelry & Watches" },
  { value: "fashion", label: "Fashion" },
  { value: "automotive", label: "Automotive" },
  { value: "sport", label: "Sport" },
  { value: "food_beverage", label: "Food & Beverage" },
  { value: "tech", label: "Tech" },
  { value: "travel", label: "Travel" },
  { value: "real_estate", label: "Real Estate" },
  { value: "home_design", label: "Home & Design" },
];

const PLATFORMS = [
  "Instagram Reels",
  "Instagram Stories",
  "TikTok",
  "YouTube",
  "TV 16:9",
  "LinkedIn",
];

const DURATIONS = [15, 30, 45, 60];

const CAMERA_MOVEMENTS = [
  "static",
  "pan_left",
  "pan_right",
  "tilt_up",
  "tilt_down",
  "tracking",
  "dolly_in",
  "dolly_out",
  "orbit",
  "crane",
  "steadicam",
  "handheld",
];

const TRANSITIONS = ["cut", "fade", "dissolve", "wipe", "xfade"];

const PHASE_LABELS: Record<string, string> = {
  analyzing: "Analyzing scenario...",
  generating_images: "Generating images...",
  animating: "Animating scenes...",
  assembling: "Assembling final video...",
};

// ── Subtle fade animation ────────────────────────────────────────────

const fadeIn = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -12 },
  transition: { duration: 0.35, ease: "easeOut" },
};

// ── Reusable UI pieces ──────────────────────────────────────────────

function InputField({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  type?: string;
}) {
  return (
    <div className="space-y-1.5">
      <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-white border border-[#E5E0D8] px-4 py-3 text-sm text-[#1A1A1A] placeholder:text-[#8A8A8A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md"
      />
    </div>
  );
}

function SelectField({
  label,
  value,
  onChange,
  options,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
  placeholder?: string;
}) {
  return (
    <div className="space-y-1.5">
      <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-white border border-[#E5E0D8] px-4 py-3 text-sm text-[#1A1A1A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md appearance-none cursor-pointer"
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </div>
  );
}

function PrimaryButton({
  children,
  onClick,
  disabled,
  loading,
  className,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  className?: string;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={clsx(
        "px-6 py-3 text-sm font-medium tracking-wide rounded-md transition-all duration-300",
        disabled
          ? "bg-[#E5E0D8] text-[#8A8A8A] cursor-not-allowed"
          : "bg-[#C4A265] text-white hover:bg-[#D4B87A] active:scale-[0.98]",
        className,
      )}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <svg
            className="animate-spin h-4 w-4"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="3"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
          {children}
        </span>
      ) : (
        children
      )}
    </button>
  );
}

function OutlineButton({
  children,
  onClick,
  className,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
}) {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "px-6 py-3 text-sm font-medium tracking-wide rounded-md border border-[#C4A265] text-[#C4A265] hover:bg-[#C4A265] hover:text-white transition-all duration-300 active:scale-[0.98]",
        className,
      )}
    >
      {children}
    </button>
  );
}

// ── Step Indicator ──────────────────────────────────────────────────

function StepIndicator({ current, total }: { current: number; total: number }) {
  return (
    <div className="flex items-center gap-3 mb-8">
      <span className="text-xs font-medium text-[#8A8A8A] tracking-wide uppercase">
        Step {current} of {total}
      </span>
      <div className="flex gap-1.5">
        {Array.from({ length: total }, (_, i) => (
          <div
            key={i}
            className={clsx(
              "h-1.5 rounded-full transition-all duration-500",
              i + 1 === current
                ? "w-6 bg-[#C4A265]"
                : i + 1 < current
                  ? "w-3 bg-[#C4A265]/50"
                  : "w-3 bg-[#E5E0D8]",
            )}
          />
        ))}
      </div>
    </div>
  );
}

// ── Sidebar ─────────────────────────────────────────────────────────

function Sidebar({
  mobileOpen,
  onClose,
}: {
  mobileOpen: boolean;
  onClose: () => void;
}) {
  const navItems = [
    { label: "New Project", href: "/generate", active: true },
    { label: "My Videos", href: "#", disabled: true },
    { label: "LoRA Models", href: "/lora", disabled: false },
    { label: "Settings", href: "#", disabled: true },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/20 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={clsx(
          "fixed top-0 left-0 h-full w-[280px] bg-white border-r border-[#E5E0D8] z-50 flex flex-col transition-transform duration-300 lg:translate-x-0",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        {/* Logo */}
        <div className="px-6 h-16 flex items-center border-b border-[#E5E0D8]">
          <a href="/" className="flex items-center group">
            <Logo height={24} />
          </a>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-6 px-3">
          <ul className="space-y-1">
            {navItems.map((item) => (
              <li key={item.label}>
                <a
                  href={item.disabled ? undefined : item.href}
                  onClick={(e) => {
                    if (item.disabled) e.preventDefault();
                    onClose();
                  }}
                  className={clsx(
                    "flex items-center px-4 py-2.5 rounded-md text-sm transition-all duration-200",
                    item.active
                      ? "border-l-2 border-[#C4A265] bg-[#FAFAF8] text-[#1A1A1A] font-medium"
                      : item.disabled
                        ? "text-[#8A8A8A] cursor-not-allowed"
                        : "text-[#4A4A4A] hover:text-[#1A1A1A] hover:bg-[#FAFAF8]",
                  )}
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* User section */}
        <div className="px-6 py-4 border-t border-[#E5E0D8]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-[#1A1A1A] flex items-center justify-center">
              <span className="text-[11px] font-medium text-[#FAFAF8]">
                AB
              </span>
            </div>
            <span className="text-sm text-[#4A4A4A]">Account</span>
          </div>
        </div>
      </aside>
    </>
  );
}

// ── Step 1: Brand & Product Setup ───────────────────────────────────

function Step1Brand({
  brandName,
  setBrandName,
  productName,
  setProductName,
  productCategory,
  setProductCategory,
  productImages,
  setProductImages,
  brandLogo,
  setBrandLogo,
  loraModelId,
  setLoraModelId,
  loraModels,
  onNext,
}: {
  brandName: string;
  setBrandName: (v: string) => void;
  productName: string;
  setProductName: (v: string) => void;
  productCategory: string;
  setProductCategory: (v: string) => void;
  productImages: File[];
  setProductImages: (v: File[]) => void;
  brandLogo: File | null;
  setBrandLogo: (v: File | null) => void;
  loraModelId: string;
  setLoraModelId: (v: string) => void;
  loraModels: LoRAModel[];
  onNext: () => void;
}) {
  const productInputRef = useRef<HTMLInputElement>(null);
  const logoInputRef = useRef<HTMLInputElement>(null);
  const selectedLora = loraModels.find((m) => m.model_id === loraModelId);

  const canProceed = brandName.trim().length > 0 && productName.trim().length > 0;

  function handleProductFiles(files: FileList | null) {
    if (!files) return;
    const next = [...productImages, ...Array.from(files)].slice(0, 5);
    setProductImages(next);
  }

  function removeProductImage(idx: number) {
    setProductImages(productImages.filter((_, i) => i !== idx));
  }

  return (
    <motion.div {...fadeIn} className="space-y-8">
      <div>
        <h2 className="text-2xl font-light text-[#1A1A1A] tracking-tight">
          Brand & Product
        </h2>
        <p className="mt-1 text-sm text-[#8A8A8A]">
          Tell us about your brand and the product to feature.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <InputField
          label="Brand Name"
          value={brandName}
          onChange={setBrandName}
          placeholder="e.g. Maison Lumiere"
        />
        <InputField
          label="Product Name"
          value={productName}
          onChange={setProductName}
          placeholder="e.g. Eclat Doré Eau de Parfum"
        />
      </div>

      <SelectField
        label="Product Category"
        value={productCategory}
        onChange={setProductCategory}
        options={PRODUCT_CATEGORIES}
        placeholder="Select a category"
      />

      {/* Product images upload */}
      <div className="space-y-1.5">
        <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
          Product Images
        </label>
        <div
          onClick={() => productInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            handleProductFiles(e.dataTransfer.files);
          }}
          className="border-2 border-dashed border-[#E5E0D8] rounded-lg p-8 text-center cursor-pointer hover:border-[#C4A265] transition-colors"
        >
          <p className="text-sm text-[#4A4A4A]">
            Drop product images here or click to browse
          </p>
          <p className="text-xs text-[#8A8A8A] mt-1">Up to 5 images</p>
          <input
            ref={productInputRef}
            type="file"
            accept="image/*"
            multiple
            className="hidden"
            onChange={(e) => handleProductFiles(e.target.files)}
          />
        </div>
        {productImages.length > 0 && (
          <div className="flex gap-3 mt-3 flex-wrap">
            {productImages.map((file, i) => (
              <div key={i} className="relative group">
                <img
                  src={URL.createObjectURL(file)}
                  alt={`Product ${i + 1}`}
                  className="w-16 h-16 object-cover rounded-md border border-[#E5E0D8]"
                />
                <button
                  onClick={() => removeProductImage(i)}
                  className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-[#1A1A1A] text-white rounded-full text-[10px] flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  x
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Brand logo upload */}
      <div className="space-y-1.5">
        <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
          Brand Logo
        </label>
        <div
          onClick={() => logoInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files?.[0]) setBrandLogo(e.dataTransfer.files[0]);
          }}
          className="border-2 border-dashed border-[#E5E0D8] rounded-lg p-6 text-center cursor-pointer hover:border-[#C4A265] transition-colors"
        >
          {brandLogo ? (
            <div className="flex items-center justify-center gap-3">
              <img
                src={URL.createObjectURL(brandLogo)}
                alt="Logo"
                className="w-10 h-10 object-contain"
              />
              <span className="text-sm text-[#4A4A4A]">{brandLogo.name}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setBrandLogo(null);
                }}
                className="text-xs text-[#8A8A8A] hover:text-[#1A1A1A] underline"
              >
                Remove
              </button>
            </div>
          ) : (
            <>
              <p className="text-sm text-[#4A4A4A]">
                Drop brand logo here or click to browse
              </p>
              <p className="text-xs text-[#8A8A8A] mt-1">Single file</p>
            </>
          )}
          <input
            ref={logoInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => {
              if (e.target.files?.[0]) setBrandLogo(e.target.files[0]);
            }}
          />
        </div>
      </div>

      {/* LoRA model selector */}
      <div className="space-y-1.5">
        <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
          Brand Ambassador Model
        </label>
        <select
          value={loraModelId}
          onChange={(e) => setLoraModelId(e.target.value)}
          className="w-full bg-white border border-[#E5E0D8] px-4 py-3 text-sm text-[#1A1A1A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md appearance-none cursor-pointer"
        >
          <option value="">No mannequin — product only</option>
          {loraModels.map((m) => (
            <option key={m.model_id} value={m.model_id}>
              {m.name}
            </option>
          ))}
        </select>
        {selectedLora && (
          <p className="text-xs text-[#8A8A8A] mt-1">
            Trigger word:{" "}
            <span className="font-medium text-[#C4A265]">
              {selectedLora.trigger_word}
            </span>
          </p>
        )}
      </div>

      <div className="pt-4">
        <PrimaryButton onClick={onNext} disabled={!canProceed}>
          Next
        </PrimaryButton>
      </div>
    </motion.div>
  );
}

// ── Step 2: Scenario ────────────────────────────────────────────────

function Step2Scenario({
  scenario,
  setScenario,
  platforms,
  setPlatforms,
  duration,
  setDuration,
  analyzing,
  onAnalyze,
  onBack,
}: {
  scenario: string;
  setScenario: (v: string) => void;
  platforms: string[];
  setPlatforms: (v: string[]) => void;
  duration: number;
  setDuration: (v: number) => void;
  analyzing: boolean;
  onAnalyze: () => void;
  onBack: () => void;
}) {
  const maxChars = 2000;

  function togglePlatform(p: string) {
    setPlatforms(
      platforms.includes(p)
        ? platforms.filter((x) => x !== p)
        : [...platforms, p],
    );
  }

  return (
    <motion.div {...fadeIn} className="space-y-8">
      <div>
        <h2 className="text-2xl font-light text-[#1A1A1A] tracking-tight">
          Your Scenario
        </h2>
        <p className="mt-1 text-sm text-[#8A8A8A]">
          Describe the advertising scenario you envision.
        </p>
      </div>

      {/* Scenario textarea */}
      <div className="space-y-1.5">
        <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
          Scenario
        </label>
        <textarea
          value={scenario}
          onChange={(e) =>
            setScenario(e.target.value.slice(0, maxChars))
          }
          placeholder={`Describe your advertising scenario...\n\nExample: A woman in an elegant Parisian apartment discovers our new perfume. She picks up the bottle from a marble vanity, admires its golden reflections in morning light, then applies it to her wrist with a graceful gesture. The camera follows her as she walks through sun-drenched rooms toward a balcony overlooking the Seine.`}
          className="w-full bg-white border border-[#E5E0D8] px-4 py-3 text-sm text-[#1A1A1A] placeholder:text-[#8A8A8A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md resize-none"
          style={{ minHeight: 200 }}
        />
        <p className="text-xs text-[#8A8A8A] text-right">
          {scenario.length} / {maxChars} characters
        </p>
      </div>

      {/* Platforms */}
      <div className="space-y-1.5">
        <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
          Target Platforms
        </label>
        <div className="flex flex-wrap gap-3">
          {PLATFORMS.map((p) => (
            <label
              key={p}
              className={clsx(
                "flex items-center gap-2 px-3 py-2 border rounded-md text-sm cursor-pointer transition-all",
                platforms.includes(p)
                  ? "border-[#C4A265] bg-[#C4A265]/5 text-[#1A1A1A]"
                  : "border-[#E5E0D8] text-[#4A4A4A] hover:border-[#C4A265]/50",
              )}
            >
              <input
                type="checkbox"
                checked={platforms.includes(p)}
                onChange={() => togglePlatform(p)}
                className="sr-only"
              />
              <div
                className={clsx(
                  "w-4 h-4 rounded border flex items-center justify-center transition-colors",
                  platforms.includes(p)
                    ? "bg-[#C4A265] border-[#C4A265]"
                    : "border-[#E5E0D8]",
                )}
              >
                {platforms.includes(p) && (
                  <svg
                    className="w-3 h-3 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={3}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </div>
              {p}
            </label>
          ))}
        </div>
      </div>

      {/* Duration */}
      <div className="space-y-1.5">
        <label className="block text-xs font-medium tracking-wide text-[#4A4A4A] uppercase">
          Duration
        </label>
        <div className="flex gap-3">
          {DURATIONS.map((d) => (
            <label
              key={d}
              className={clsx(
                "px-4 py-2 border rounded-md text-sm cursor-pointer transition-all",
                duration === d
                  ? "border-[#C4A265] bg-[#C4A265] text-white"
                  : "border-[#E5E0D8] text-[#4A4A4A] hover:border-[#C4A265]/50",
              )}
            >
              <input
                type="radio"
                name="duration"
                checked={duration === d}
                onChange={() => setDuration(d)}
                className="sr-only"
              />
              {d}s
            </label>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-4 pt-4">
        <button
          onClick={onBack}
          className="px-6 py-3 text-sm text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors"
        >
          Back
        </button>
        <PrimaryButton
          onClick={onAnalyze}
          disabled={scenario.trim().length === 0}
          loading={analyzing}
        >
          {analyzing ? "Analyzing..." : "Analyze Scenario"}
        </PrimaryButton>
      </div>
    </motion.div>
  );
}

// ── Step 3: Scene Review ────────────────────────────────────────────

function Step3Scenes({
  scenes,
  setScenes,
  onGenerate,
  onBack,
}: {
  scenes: Scene[];
  setScenes: (s: Scene[]) => void;
  onGenerate: () => void;
  onBack: () => void;
}) {
  function updateScene(idx: number, patch: Partial<Scene>) {
    const next = scenes.map((s, i) => (i === idx ? { ...s, ...patch } : s));
    setScenes(next);
  }

  function deleteScene(idx: number) {
    if (!confirm("Remove this scene?")) return;
    setScenes(scenes.filter((_, i) => i !== idx));
  }

  function addScene() {
    const newScene: Scene = {
      id: scenes.length + 1,
      type: "produit",
      description: "",
      duration: 4.0,
      camera_movement: "static",
      transition: "cut",
    };
    setScenes([...scenes, newScene]);
  }

  const typeBadge = (type: Scene["type"]) => {
    const styles: Record<string, string> = {
      personnage: "bg-[#C4A265] text-white",
      produit: "bg-[#E5E0D8] text-[#4A4A4A]",
      transition: "border border-[#C4A265] text-[#C4A265] bg-transparent",
    };
    return styles[type] || styles.produit;
  };

  return (
    <motion.div {...fadeIn} className="space-y-8">
      <div>
        <h2 className="text-2xl font-light text-[#1A1A1A] tracking-tight">
          Scene Breakdown
        </h2>
        <p className="mt-1 text-sm text-[#8A8A8A]">
          Review and adjust your scenes.
        </p>
      </div>

      <div className="space-y-4">
        {scenes.map((scene, idx) => (
          <motion.div
            key={scene.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.05 }}
            className="bg-[#FAFAF8] border border-[#E5E0D8] rounded-lg p-5 space-y-4"
          >
            {/* Header row */}
            <div className="flex items-center gap-3">
              <div className="w-7 h-7 rounded-full bg-[#C4A265] text-white text-xs font-medium flex items-center justify-center flex-shrink-0">
                {idx + 1}
              </div>
              <span
                className={clsx(
                  "text-[10px] font-medium uppercase tracking-wider px-2 py-0.5 rounded",
                  typeBadge(scene.type),
                )}
              >
                {scene.type}
              </span>
              <div className="flex-1" />
              <button
                onClick={() => deleteScene(idx)}
                className="text-[#8A8A8A] hover:text-[#1A1A1A] transition-colors text-lg leading-none"
                title="Remove scene"
              >
                &times;
              </button>
            </div>

            {/* Description */}
            <textarea
              value={scene.description}
              onChange={(e) =>
                updateScene(idx, { description: e.target.value })
              }
              className="w-full bg-white border border-[#E5E0D8] px-4 py-3 text-sm text-[#1A1A1A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md resize-none"
              rows={2}
              placeholder="Scene description..."
            />

            {/* Controls row */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Duration slider */}
              <div className="space-y-1">
                <label className="text-[10px] font-medium text-[#8A8A8A] uppercase tracking-wider">
                  Duration: {scene.duration.toFixed(1)}s
                </label>
                <input
                  type="range"
                  min={2}
                  max={8}
                  step={0.5}
                  value={scene.duration}
                  onChange={(e) =>
                    updateScene(idx, {
                      duration: parseFloat(e.target.value),
                    })
                  }
                  className="w-full accent-[#C4A265]"
                />
              </div>

              {/* Camera */}
              <div className="space-y-1">
                <label className="text-[10px] font-medium text-[#8A8A8A] uppercase tracking-wider">
                  Camera
                </label>
                <select
                  value={scene.camera_movement}
                  onChange={(e) =>
                    updateScene(idx, { camera_movement: e.target.value })
                  }
                  className="w-full bg-white border border-[#E5E0D8] px-3 py-2 text-xs text-[#1A1A1A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md appearance-none"
                >
                  {CAMERA_MOVEMENTS.map((c) => (
                    <option key={c} value={c}>
                      {c.replace(/_/g, " ")}
                    </option>
                  ))}
                </select>
              </div>

              {/* Transition */}
              <div className="space-y-1">
                <label className="text-[10px] font-medium text-[#8A8A8A] uppercase tracking-wider">
                  Transition
                </label>
                <select
                  value={scene.transition}
                  onChange={(e) =>
                    updateScene(idx, { transition: e.target.value })
                  }
                  className="w-full bg-white border border-[#E5E0D8] px-3 py-2 text-xs text-[#1A1A1A] focus:border-[#C4A265] focus:outline-none transition-colors rounded-md appearance-none"
                >
                  {TRANSITIONS.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Add scene */}
      <button
        onClick={addScene}
        className="w-full py-3 border-2 border-dashed border-[#E5E0D8] rounded-lg text-sm text-[#8A8A8A] hover:border-[#C4A265] hover:text-[#C4A265] transition-colors"
      >
        + Add Scene
      </button>

      {/* Actions */}
      <div className="flex gap-4 pt-4">
        <button
          onClick={onBack}
          className="px-6 py-3 text-sm text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors"
        >
          Back
        </button>
        <PrimaryButton
          onClick={onGenerate}
          disabled={scenes.length === 0}
          className="text-base px-8 py-3.5"
        >
          Generate Video
        </PrimaryButton>
      </div>
    </motion.div>
  );
}

// ── Step 4: Generation Progress ─────────────────────────────────────

function Step4Progress({
  progress,
  phase,
  scenes,
}: {
  progress: number;
  phase: string;
  scenes: { id: number; status: string }[];
}) {
  const phaseLabel =
    PHASE_LABELS[phase] ||
    (progress < 10
      ? PHASE_LABELS.analyzing
      : progress < 45
        ? PHASE_LABELS.generating_images
        : progress < 85
          ? PHASE_LABELS.animating
          : PHASE_LABELS.assembling);

  return (
    <motion.div {...fadeIn} className="space-y-10">
      <div className="text-center space-y-3">
        <h2 className="text-2xl font-light text-[#1A1A1A] tracking-tight">
          Creating your video...
        </h2>
        <p className="text-sm text-[#8A8A8A]">{phaseLabel}</p>
      </div>

      {/* Progress bar */}
      <div className="max-w-lg mx-auto">
        <div className="h-1.5 bg-[#E5E0D8] rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-[#C4A265] rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          />
        </div>
        <p className="text-xs text-[#8A8A8A] mt-2 text-center">
          {Math.round(progress)}%
        </p>
      </div>

      {/* Scene grid */}
      {scenes.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {scenes.map((s) => (
            <div
              key={s.id}
              className="aspect-video bg-[#E5E0D8] rounded-lg overflow-hidden flex items-center justify-center"
            >
              {s.status === "completed" ? (
                <div className="w-full h-full bg-[#1A1A1A]/10 flex items-center justify-center">
                  <svg
                    className="w-6 h-6 text-[#C4A265]"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
              ) : (
                <span className="text-xs text-[#8A8A8A] animate-pulse">
                  Generating...
                </span>
              )}
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}

// ── Step 5: Result ──────────────────────────────────────────────────

function Step5Result({
  videoUrl,
  scenes,
  onNewProject,
}: {
  videoUrl: string | null;
  scenes: { id: number; status: string }[];
  onNewProject: () => void;
}) {
  return (
    <motion.div {...fadeIn} className="space-y-10">
      <div className="text-center space-y-2">
        <div className="flex items-center justify-center gap-2">
          <svg
            className="w-6 h-6 text-[#C4A265]"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M5 13l4 4L19 7"
            />
          </svg>
          <h2 className="text-2xl font-light text-[#1A1A1A] tracking-tight">
            Your video is ready
          </h2>
        </div>
      </div>

      {/* Video player */}
      <div className="max-w-3xl mx-auto">
        <div className="aspect-video bg-[#1A1A1A] rounded-lg overflow-hidden flex items-center justify-center relative group">
          {videoUrl ? (
            <video
              src={videoUrl}
              controls
              className="w-full h-full object-contain"
            />
          ) : (
            <button className="flex flex-col items-center gap-3 text-[#FAFAF8]/60 hover:text-[#FAFAF8] transition-colors">
              <svg
                className="w-14 h-14"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M8 5v14l11-7z" />
              </svg>
              <span className="text-sm">Preview</span>
            </button>
          )}
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex justify-center gap-4">
        <OutlineButton
          onClick={() => {
            if (videoUrl) {
              const a = document.createElement("a");
              a.href = videoUrl;
              a.download = "astreli-video.mp4";
              a.click();
            }
          }}
        >
          Download MP4
        </OutlineButton>
        <PrimaryButton onClick={() => alert("Export coming soon")}>
          Export for Platforms
        </PrimaryButton>
      </div>

      {/* Scene thumbnails */}
      {scenes.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-xs font-medium text-[#8A8A8A] uppercase tracking-wider">
            Scene Breakdown
          </h3>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {scenes.map((s) => (
              <div
                key={s.id}
                className="w-28 h-16 bg-[#E5E0D8] rounded-md flex-shrink-0 flex items-center justify-center"
              >
                <span className="text-[10px] text-[#8A8A8A]">
                  Scene {s.id}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* New project */}
      <div className="text-center">
        <button
          onClick={onNewProject}
          className="text-sm text-[#8A8A8A] hover:text-[#C4A265] transition-colors underline underline-offset-4"
        >
          Create Another Video
        </button>
      </div>
    </motion.div>
  );
}

// ── Main Page ───────────────────────────────────────────────────────

export default function GeneratePage() {
  return (
    <Suspense fallback={null}>
      <GeneratePageContent />
    </Suspense>
  );
}

function GeneratePageContent() {
  const searchParams = useSearchParams();

  // Step state
  const [currentStep, setCurrentStep] = useState(1);

  // Sidebar
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Step 1 state
  const [brandName, setBrandName] = useState(searchParams.get("brand") || "");
  const [productName, setProductName] = useState("");
  const [productCategory, setProductCategory] = useState("");
  const [productImages, setProductImages] = useState<File[]>([]);
  const [brandLogo, setBrandLogo] = useState<File | null>(null);
  const [loraModelId, setLoraModelId] = useState("");
  const [loraModels, setLoraModels] = useState<LoRAModel[]>([]);

  // Step 2 state
  const [scenario, setScenario] = useState("");
  const [platforms, setPlatforms] = useState<string[]>([]);
  const [duration, setDuration] = useState(30);
  const [analyzing, setAnalyzing] = useState(false);

  // Step 3 state
  const [scenes, setScenes] = useState<Scene[]>([]);

  // Step 4 state
  const [jobId, setJobId] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [phase, setPhase] = useState("");
  const [generationScenes, setGenerationScenes] = useState<
    { id: number; status: string }[]
  >([]);

  // Step 5 state
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  // Polling ref
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Fetch LoRA models on mount
  useEffect(() => {
    getLoraModels()
      .then(setLoraModels)
      .catch(() => {});
  }, []);

  // Cleanup polling
  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  // ── Handlers ────────────────────────────────────────────────────

  const handleAnalyze = useCallback(async () => {
    setAnalyzing(true);
    try {
      const mode = loraModelId ? "mannequin" : "product";
      const result: SceneBreakdown = await analyzeScenario(
        scenario,
        mode,
        productCategory || "luxury",
      );
      setScenes(result.scenes);
      setCurrentStep(3);
    } catch (err) {
      console.error("Analyze failed:", err);
      // Fallback: create a placeholder scene so the user can continue
      setScenes([
        {
          id: 1,
          type: "produit",
          description: scenario.slice(0, 200),
          duration: 4.0,
          camera_movement: "static",
          transition: "fade",
        },
      ]);
      setCurrentStep(3);
    } finally {
      setAnalyzing(false);
    }
  }, [scenario, loraModelId, productCategory]);

  const handleGenerate = useCallback(async () => {
    setCurrentStep(4);
    setProgress(0);
    setPhase("analyzing");
    setGenerationScenes(scenes.map((s) => ({ id: s.id, status: "pending" })));

    const fileToDataURL = (file: File): Promise<string> =>
      new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });

    try {
      // Convert uploaded product photos + logo to base64 data URLs
      const productImagesB64 = await Promise.all(productImages.map(fileToDataURL));
      const brandLogoB64 = brandLogo ? await fileToDataURL(brandLogo) : undefined;

      const req: GenerateRequest = {
        brand_name: brandName,
        product_name: productName,
        product_category: productCategory || "luxury",
        scenario,
        scenes,
        platforms,
        duration,
        lora_model_id: loraModelId || undefined,
        product_images: productImagesB64,
        brand_logo: brandLogoB64,
      };
      const { job_id } = await generateVideo(req);
      setJobId(job_id);

      // Start polling
      pollRef.current = setInterval(async () => {
        try {
          const status = await getJobStatus(job_id);
          setProgress(status.progress);
          setPhase(status.phase);
          if (status.scenes) {
            setGenerationScenes(
              status.scenes.map((s: { id: number; status: string }) => ({
                id: s.id,
                status: s.status,
              })),
            );
          }

          if (status.status === "completed") {
            if (pollRef.current) clearInterval(pollRef.current);
            try {
              const result = await getJobResult(job_id);
              setVideoUrl(result.video_url);
            } catch {
              /* result may be in status response */
            }
            setCurrentStep(5);
          } else if (status.status === "failed") {
            if (pollRef.current) clearInterval(pollRef.current);
            alert("Generation failed. Please try again.");
            setCurrentStep(3);
          }
        } catch {
          /* ignore transient polling errors */
        }
      }, 3000);
    } catch (err) {
      console.error("Generate failed:", err);
      alert("Failed to start generation. Please try again.");
      setCurrentStep(3);
    }
  }, [
    brandName,
    productName,
    productCategory,
    scenario,
    scenes,
    platforms,
    duration,
    loraModelId,
    productImages,
    brandLogo,
  ]);

  const handleNewProject = useCallback(() => {
    setBrandName("");
    setProductName("");
    setProductCategory("");
    setProductImages([]);
    setBrandLogo(null);
    setLoraModelId("");
    setScenario("");
    setPlatforms([]);
    setDuration(30);
    setScenes([]);
    setJobId(null);
    setProgress(0);
    setPhase("");
    setGenerationScenes([]);
    setVideoUrl(null);
    setCurrentStep(1);
  }, []);

  return (
    <div className="min-h-screen bg-[#FAFAF8]">
      <Sidebar mobileOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Mobile header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-14 bg-white border-b border-[#E5E0D8] z-30 flex items-center px-4">
        <button
          onClick={() => setSidebarOpen(true)}
          className="text-[#1A1A1A] p-1"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5"
            />
          </svg>
        </button>
        <span className="ml-3">
          <Logo height={20} />
        </span>
      </div>

      {/* Main content */}
      <main className="lg:ml-[280px] min-h-screen">
        <div className="max-w-3xl mx-auto px-6 py-12 pt-20 lg:pt-12">
          {currentStep <= 3 && (
            <StepIndicator current={currentStep} total={5} />
          )}

          <AnimatePresence mode="wait">
            {currentStep === 1 && (
              <Step1Brand
                key="step1"
                brandName={brandName}
                setBrandName={setBrandName}
                productName={productName}
                setProductName={setProductName}
                productCategory={productCategory}
                setProductCategory={setProductCategory}
                productImages={productImages}
                setProductImages={setProductImages}
                brandLogo={brandLogo}
                setBrandLogo={setBrandLogo}
                loraModelId={loraModelId}
                setLoraModelId={setLoraModelId}
                loraModels={loraModels}
                onNext={() => setCurrentStep(2)}
              />
            )}
            {currentStep === 2 && (
              <Step2Scenario
                key="step2"
                scenario={scenario}
                setScenario={setScenario}
                platforms={platforms}
                setPlatforms={setPlatforms}
                duration={duration}
                setDuration={setDuration}
                analyzing={analyzing}
                onAnalyze={handleAnalyze}
                onBack={() => setCurrentStep(1)}
              />
            )}
            {currentStep === 3 && (
              <Step3Scenes
                key="step3"
                scenes={scenes}
                setScenes={setScenes}
                onGenerate={handleGenerate}
                onBack={() => setCurrentStep(2)}
              />
            )}
            {currentStep === 4 && (
              <Step4Progress
                key="step4"
                progress={progress}
                phase={phase}
                scenes={generationScenes}
              />
            )}
            {currentStep === 5 && (
              <Step5Result
                key="step5"
                videoUrl={videoUrl}
                scenes={generationScenes}
                onNewProject={handleNewProject}
              />
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
