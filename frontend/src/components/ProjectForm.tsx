"use client";

import { useRef, useState } from "react";
import { createProject, type ProjectResponse } from "@/lib/api";

interface Props {
  onCreated: (project: ProjectResponse) => void;
}

export default function ProjectForm({ onCreated }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const formRef = useRef<HTMLFormElement>(null);

  const [mannequinFiles, setMannequinFiles] = useState<File[]>([]);
  const [productFiles, setProductFiles] = useState<File[]>([]);
  const [decorFiles, setDecorFiles] = useState<File[]>([]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const form = formRef.current!;
    const fd = new FormData();

    fd.append("scenario", (form.elements.namedItem("scenario") as HTMLTextAreaElement).value);

    const brandName = (form.elements.namedItem("brand_name") as HTMLInputElement).value;
    if (brandName) fd.append("brand_name", brandName);

    const brandTone = (form.elements.namedItem("brand_tone") as HTMLInputElement).value;
    if (brandTone) fd.append("brand_tone", brandTone);

    mannequinFiles.forEach((f) => fd.append("mannequin_images", f));
    productFiles.forEach((f) => fd.append("product_images", f));
    decorFiles.forEach((f) => fd.append("decor_images", f));

    const logo = (form.elements.namedItem("logo") as HTMLInputElement).files?.[0];
    if (logo) fd.append("logo", logo);

    const music = (form.elements.namedItem("music") as HTMLInputElement).files?.[0];
    if (music) fd.append("music", music);

    try {
      const project = await createProject(fd);
      onCreated(project);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const mode = mannequinFiles.length > 0 ? "character_product" : "product_only";

  return (
    <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
      {/* Mode indicator */}
      <div className="flex items-center gap-3 p-3 rounded-lg" style={{ background: "var(--bg-card)" }}>
        <div
          className="w-3 h-3 rounded-full"
          style={{
            background: mode === "character_product" ? "#EF4444" : "#06B6D4",
            boxShadow: `0 0 8px ${mode === "character_product" ? "#EF444488" : "#06B6D488"}`,
          }}
        />
        <span className="text-xs font-bold tracking-wider" style={{
          color: mode === "character_product" ? "#EF4444" : "#06B6D4",
        }}>
          MODE: {mode === "character_product" ? "PERSONNAGE + PRODUIT" : "PRODUIT UNIQUEMENT"}
        </span>
      </div>

      {/* Scenario */}
      <div>
        <label className="block text-xs font-bold tracking-wider mb-2" style={{ color: "var(--accent-amber)" }}>
          SCÉNARIO PUBLICITAIRE *
        </label>
        <textarea
          name="scenario"
          required
          rows={6}
          placeholder="Décrivez votre publicité en langage naturel. Ex: Une femme élégante entre dans un loft parisien baigné de lumière dorée. Elle découvre un flacon de parfum posé sur une table en marbre..."
          className="w-full rounded-lg p-4 text-sm resize-none focus:outline-none focus:ring-2 transition"
          style={{
            background: "var(--bg-card)",
            border: "1px solid var(--border)",
            color: "var(--text-primary)",
          }}
        />
      </div>

      {/* Brand */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-bold tracking-wider mb-2" style={{ color: "var(--text-secondary)" }}>
            MARQUE
          </label>
          <input
            name="brand_name"
            type="text"
            placeholder="Nom de la marque"
            className="w-full rounded-lg p-3 text-sm focus:outline-none focus:ring-2 transition"
            style={{ background: "var(--bg-card)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
          />
        </div>
        <div>
          <label className="block text-xs font-bold tracking-wider mb-2" style={{ color: "var(--text-secondary)" }}>
            TON
          </label>
          <input
            name="brand_tone"
            type="text"
            placeholder="Luxueux, énergique, minimaliste..."
            className="w-full rounded-lg p-3 text-sm focus:outline-none focus:ring-2 transition"
            style={{ background: "var(--bg-card)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
          />
        </div>
      </div>

      {/* File uploads */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <FileUploadZone
          label="PHOTOS MANNEQUIN"
          sublabel="Optionnel — active le mode personnage"
          accept="image/*"
          multiple
          files={mannequinFiles}
          onChange={setMannequinFiles}
          accentColor="#EF4444"
        />
        <FileUploadZone
          label="PHOTOS PRODUIT"
          sublabel="Référence visuelle du produit"
          accept="image/*"
          multiple
          files={productFiles}
          onChange={setProductFiles}
          accentColor="#06B6D4"
        />
        <FileUploadZone
          label="PHOTOS DÉCOR"
          sublabel="Environnement, ambiance"
          accept="image/*"
          multiple
          files={decorFiles}
          onChange={setDecorFiles}
          accentColor="#8B5CF6"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-bold tracking-wider mb-2" style={{ color: "var(--text-secondary)" }}>
            LOGO
          </label>
          <input
            name="logo"
            type="file"
            accept="image/*"
            className="w-full text-xs file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-bold file:cursor-pointer"
            style={{ color: "var(--text-muted)" }}
          />
        </div>
        <div>
          <label className="block text-xs font-bold tracking-wider mb-2" style={{ color: "var(--text-secondary)" }}>
            MUSIQUE
          </label>
          <input
            name="music"
            type="file"
            accept="audio/*"
            className="w-full text-xs file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-bold file:cursor-pointer"
            style={{ color: "var(--text-muted)" }}
          />
        </div>
      </div>

      {error && (
        <div className="p-3 rounded-lg border border-red-500/30 bg-red-500/10 text-red-400 text-sm">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full py-4 rounded-lg font-bold text-sm tracking-widest transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed"
        style={{
          background: loading
            ? "var(--bg-card)"
            : "linear-gradient(135deg, #F59E0B, #F97316)",
          color: loading ? "var(--text-muted)" : "#0d0d1a",
        }}
      >
        {loading ? "LANCEMENT DU PIPELINE..." : "GÉNÉRER LA PUBLICITÉ"}
      </button>
    </form>
  );
}


function FileUploadZone({
  label,
  sublabel,
  accept,
  multiple,
  files,
  onChange,
  accentColor,
}: {
  label: string;
  sublabel: string;
  accept: string;
  multiple?: boolean;
  files: File[];
  onChange: (files: File[]) => void;
  accentColor: string;
}) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <div
      className="rounded-lg p-4 border-2 border-dashed cursor-pointer transition-all hover:border-opacity-100 text-center"
      style={{
        borderColor: files.length > 0 ? accentColor : "var(--border)",
        background: files.length > 0 ? accentColor + "08" : "var(--bg-card)",
      }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        className="hidden"
        onChange={(e) => {
          const selected = Array.from(e.target.files || []);
          onChange(selected);
        }}
      />
      <div className="text-xs font-bold tracking-wider mb-1" style={{ color: accentColor }}>
        {label}
      </div>
      <div className="text-[10px]" style={{ color: "var(--text-muted)" }}>
        {sublabel}
      </div>
      {files.length > 0 && (
        <div className="mt-2 text-[10px] font-bold" style={{ color: accentColor }}>
          {files.length} fichier{files.length > 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}
