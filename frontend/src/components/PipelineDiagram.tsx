import { useState } from "react";

const STEPS = {
  start: {
    id: "start",
    label: "CLIENT",
    subtitle: "Entrées du projet",
    detail:
      "Le service marketing fournit :\n• Scénario publicitaire (texte libre)\n• Photos mannequin (optionnel) → détermine le MODE\n• Photos décor / produit (optionnel)\n• Musique, logo marque (optionnel)",
    color: "#F59E0B",
  },
  detect: {
    id: "detect",
    label: "DÉTECTION MODE",
    subtitle: "Mannequin fourni ?",
    detail:
      "Le pipeline vérifie une seule chose :\nle client a-t-il uploadé des photos de mannequin ?\n\n→ OUI  →  Mode PERSONNAGE + PRODUIT\n→ NON  →  Mode PRODUIT UNIQUEMENT\n\nCe choix se propage à TOUTES les étapes suivantes.",
    color: "#EF4444",
  },
  gpt: {
    id: "gpt",
    label: "ÉTAPE 1 — GPT-4o",
    subtitle: "Analyse du scénario",
    detail:
      "GPT-4o agit comme directeur artistique.\nIl découpe le scénario en scènes individuelles.\n\nMode PERSONNAGE + PRODUIT :\n  GPT-4o tag chaque scène → « personnage » ou « produit »\n\nMode PRODUIT UNIQUEMENT :\n  Toutes les scènes → « produit »\n\nPour chaque scène il génère :\n• Prompt image (anglais, détaillé)\n• Prompt vidéo (mouvement, caméra)\n• Durée, transition, mouvement caméra",
    color: "#8B5CF6",
  },
  gemini_pro: {
    id: "gemini_pro",
    label: "Nano Banana Pro",
    subtitle: "gemini-3-pro-image-preview",
    detail:
      "Scènes « personnage » uniquement.\n\n• Session chat persistante ouverte en début de pipeline\n• Photos mannequin envoyées → Gemini mémorise le visage\n  (REMPLACE le LoRA traditionnel)\n• Chaque scène personnage générée dans la MÊME session\n  → consistance visage garantie\n• Jusqu'à 14 images de référence (mannequin + décors)\n• Résolution jusqu'à 4K\n• Raisonnement avancé (Thinking)\n• ~0.134$ / image",
    color: "#3B82F6",
  },
  gemini_flash: {
    id: "gemini_flash",
    label: "Nano Banana 2",
    subtitle: "gemini-3.1-flash-image-preview",
    detail:
      "Scènes « produit » (dans les deux modes).\n\n• Appel one-shot (pas de session chat)\n• Pas besoin de consistance faciale\n• Photos produit / décor passées en référence\n• Plus rapide, 3× moins cher\n• ~0.039$ / image\n• Qualité largement suffisante pour objets",
    color: "#06B6D4",
  },
  kling_v01: {
    id: "kling_v01",
    label: "Kling-Video-01",
    subtitle: "Animation personnage",
    detail:
      "Scènes « personnage » uniquement.\n\n• Optimisé mouvements humains naturels\n• Marche, gestes, expressions, retournement\n• Image → vidéo (2-10 secondes)\n• Processus asynchrone :\n  soumission → polling 10s → téléchargement MP4",
    color: "#10B981",
  },
  kling_v3: {
    id: "kling_v3",
    label: "Kling-V3",
    subtitle: "Animation produit",
    detail:
      "Scènes « produit » (dans les deux modes).\n\n• Optimisé rotations d'objets\n• Reflets, jeux de lumière, orbite caméra\n• Image → vidéo (2-10 secondes)\n• Processus asynchrone :\n  soumission → polling 10s → téléchargement MP4",
    color: "#10B981",
  },
  ffmpeg: {
    id: "ffmpeg",
    label: "ÉTAPE 4 — FFmpeg",
    subtitle: "Assemblage final",
    detail:
      "Monte tous les clips dans l'ordre du scénario :\n\n• Mise à l'échelle uniforme 1920×1080\n• Transitions entre scènes (fade / dissolve / wipe)\n  → type décidé par GPT-4o\n• Fondu d'entrée / sortie global\n• Musique de fond + fade audio\n• Logo marque en overlay (coin supérieur droit)\n• Export H.264 qualité professionnelle",
    color: "#F97316",
  },
  output: {
    id: "output",
    label: "SORTIE",
    subtitle: "Vidéo publicitaire finale",
    detail: "Fichier .mp4 prêt à diffuser.\nQualité broadcast, H.264, 1080p.\n\nCoût estimé par vidéo de 30s (5 scènes) :\n• Mode PRODUIT : ~0.20$ (images) + Kling\n• Mode MIXTE : ~0.55$ (images) + Kling",
    color: "#F59E0B",
  },
};

type StepKey = keyof typeof STEPS;

const Node = ({ step, isActive, onClick, x, y, w, h }: {
  step: StepKey; isActive: boolean; onClick: (s: StepKey) => void;
  x: number; y: number; w: number; h: number;
}) => {
  const s = STEPS[step];
  return (
    <g
      onClick={() => onClick(step)}
      style={{ cursor: "pointer" }}
      className="node-group"
    >
      <rect
        x={x}
        y={y}
        width={w}
        height={h}
        rx={6}
        fill={isActive ? s.color + "22" : "#1a1a2e"}
        stroke={isActive ? s.color : "#2a2a4a"}
        strokeWidth={isActive ? 2.5 : 1.5}
        style={{
          transition: "all 0.3s ease",
          filter: isActive ? `drop-shadow(0 0 12px ${s.color}66)` : "none",
        }}
      />
      <text
        x={x + w / 2}
        y={y + (h > 50 ? 22 : 18)}
        textAnchor="middle"
        fill={s.color}
        fontSize="11"
        fontWeight="700"
        fontFamily="'JetBrains Mono', 'Fira Code', monospace"
        letterSpacing="0.5"
      >
        {s.label}
      </text>
      <text
        x={x + w / 2}
        y={y + (h > 50 ? 38 : 32)}
        textAnchor="middle"
        fill="#8888aa"
        fontSize="8.5"
        fontFamily="'JetBrains Mono', monospace"
      >
        {s.subtitle}
      </text>
    </g>
  );
};

const Arrow = ({ x1, y1, x2, y2, label, labelOffset, color = "#444466" }: {
  x1: number; y1: number; x2: number; y2: number;
  label?: string; labelOffset?: { x?: number; y?: number }; color?: string;
}) => {
  const midY = (y1 + y2) / 2;
  return (
    <g>
      <path
        d={`M${x1},${y1} C${x1},${midY} ${x2},${midY} ${x2},${y2}`}
        fill="none"
        stroke={color}
        strokeWidth="1.5"
        markerEnd="url(#arrowhead)"
        strokeDasharray={color !== "#444466" ? "none" : "none"}
      />
      {label && (
        <text
          x={(x1 + x2) / 2 + (labelOffset?.x || 0)}
          y={midY + (labelOffset?.y || 0)}
          textAnchor="middle"
          fill={color === "#444466" ? "#666688" : color}
          fontSize="8"
          fontFamily="'JetBrains Mono', monospace"
          fontWeight="600"
        >
          {label}
        </text>
      )}
    </g>
  );
};

const StraightArrow = ({ x1, y1, x2, y2, color = "#444466" }: {
  x1: number; y1: number; x2: number; y2: number; color?: string;
}) => (
  <line
    x1={x1} y1={y1} x2={x2} y2={y2}
    stroke={color} strokeWidth="1.5"
    markerEnd="url(#arrowhead)"
  />
);

export default function PipelineDiagram() {
  const [active, setActive] = useState<StepKey>("detect");

  const detail = STEPS[active];

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0d0d1a",
        color: "#e0e0f0",
        fontFamily: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "24px 16px",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Grid background */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "linear-gradient(#1a1a3010 1px, transparent 1px), linear-gradient(90deg, #1a1a3010 1px, transparent 1px)",
          backgroundSize: "40px 40px",
          pointerEvents: "none",
        }}
      />

      {/* Title */}
      <div style={{ textAlign: "center", marginBottom: 20, zIndex: 1 }}>
        <h1
          style={{
            fontSize: 22,
            fontWeight: 800,
            letterSpacing: 3,
            color: "#F59E0B",
            margin: 0,
            textTransform: "uppercase",
          }}
        >
          AdGenAI Pipeline
        </h1>
        <p style={{ color: "#555570", fontSize: 10, marginTop: 4, letterSpacing: 1.5 }}>
          CLIQUEZ SUR CHAQUE BLOC POUR VOIR LE DÉTAIL
        </p>
      </div>

      {/* SVG Diagram */}
      <svg
        viewBox="0 0 620 620"
        style={{
          width: "100%",
          maxWidth: 620,
          zIndex: 1,
        }}
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth="8"
            markerHeight="6"
            refX="7"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 8 3, 0 6" fill="#555577" />
          </marker>
        </defs>

        {/* ── ROW 0: CLIENT ── */}
        <Node step="start" isActive={active === "start"} onClick={setActive}
          x={230} y={10} w={160} h={48} />

        {/* Arrow → DETECT */}
        <StraightArrow x1={310} y1={58} x2={310} y2={80} />

        {/* ── ROW 1: DETECT MODE ── */}
        <Node step="detect" isActive={active === "detect"} onClick={setActive}
          x={210} y={80} w={200} h={48} />

        {/* Branch arrows */}
        <Arrow x1={270} y1={128} x2={150} y2={175}
          label="OUI → mannequin" labelOffset={{ x: -40, y: -6 }} color="#EF4444" />
        <Arrow x1={350} y1={128} x2={470} y2={175}
          label="NON" labelOffset={{ x: 30, y: -6 }} color="#555577" />

        {/* ── ROW 2: MODE LABELS ── */}
        <rect x={70} y={175} width={160} height={30} rx={4}
          fill="#EF444418" stroke="#EF4444" strokeWidth={1} strokeDasharray="4 2" />
        <text x={150} y={194} textAnchor="middle" fill="#EF4444"
          fontSize="10" fontWeight="700" fontFamily="'JetBrains Mono', monospace">
          MODE PERSONNAGE + PRODUIT
        </text>

        <rect x={390} y={175} width={160} height={30} rx={4}
          fill="#06B6D418" stroke="#06B6D4" strokeWidth={1} strokeDasharray="4 2" />
        <text x={470} y={194} textAnchor="middle" fill="#06B6D4"
          fontSize="10" fontWeight="700" fontFamily="'JetBrains Mono', monospace">
          MODE PRODUIT UNIQUEMENT
        </text>

        {/* Arrows → GPT-4o */}
        <StraightArrow x1={150} y1={205} x2={260} y2={228} />
        <StraightArrow x1={470} y1={205} x2={360} y2={228} />

        {/* ── ROW 3: GPT-4o ── */}
        <Node step="gpt" isActive={active === "gpt"} onClick={setActive}
          x={210} y={228} w={200} h={48} />

        {/* GPT → ETAPE 2 label */}
        <text x={310} y={296} textAnchor="middle" fill="#444466"
          fontSize="9" fontFamily="'JetBrains Mono', monospace" fontWeight="600">
          ÉTAPE 2 — Génération images
        </text>

        {/* Branch from GPT to two Gemini models */}
        <Arrow x1={260} y1={276} x2={140} y2={318}
          label="personnage" labelOffset={{ x: -30, y: -6 }} color="#3B82F6" />
        <Arrow x1={360} y1={276} x2={470} y2={318}
          label="produit" labelOffset={{ x: 30, y: -6 }} color="#06B6D4" />

        {/* ── ROW 4: GEMINI MODELS ── */}
        <Node step="gemini_pro" isActive={active === "gemini_pro"} onClick={setActive}
          x={40} y={318} w={200} h={52} />
        <Node step="gemini_flash" isActive={active === "gemini_flash"} onClick={setActive}
          x={370} y={318} w={210} h={52} />

        {/* Chat badge on Pro */}
        <rect x={175} y={350} width={56} height={16} rx={8}
          fill="#3B82F644" stroke="#3B82F6" strokeWidth={0.8} />
        <text x={203} y={361} textAnchor="middle" fill="#3B82F6"
          fontSize="7" fontWeight="700" fontFamily="'JetBrains Mono', monospace">
          CHAT 💬
        </text>

        {/* One-shot badge on Flash */}
        <rect x={505} y={350} width={66} height={16} rx={8}
          fill="#06B6D444" stroke="#06B6D4" strokeWidth={0.8} />
        <text x={538} y={361} textAnchor="middle" fill="#06B6D4"
          fontSize="7" fontWeight="700" fontFamily="'JetBrains Mono', monospace">
          ONE-SHOT ⚡
        </text>

        {/* ETAPE 3 label */}
        <text x={310} y={400} textAnchor="middle" fill="#444466"
          fontSize="9" fontFamily="'JetBrains Mono', monospace" fontWeight="600">
          ÉTAPE 3 — Animation vidéo
        </text>

        {/* Arrows to Kling */}
        <Arrow x1={140} y1={370} x2={140} y2={415}
          label="" color="#10B981" />
        <Arrow x1={475} y1={370} x2={475} y2={415}
          label="" color="#10B981" />

        {/* ── ROW 5: KLING MODELS ── */}
        <Node step="kling_v01" isActive={active === "kling_v01"} onClick={setActive}
          x={40} y={415} w={200} h={52} />
        <Node step="kling_v3" isActive={active === "kling_v3"} onClick={setActive}
          x={370} y={415} w={210} h={52} />

        {/* Arrows to FFmpeg */}
        <Arrow x1={140} y1={467} x2={260} y2={505} color="#F97316" />
        <Arrow x1={475} y1={467} x2={360} y2={505} color="#F97316" />

        {/* ── ROW 6: FFMPEG ── */}
        <Node step="ffmpeg" isActive={active === "ffmpeg"} onClick={setActive}
          x={210} y={505} w={200} h={48} />

        {/* Arrow to output */}
        <StraightArrow x1={310} y1={553} x2={310} y2={572} color="#F59E0B" />

        {/* ── ROW 7: OUTPUT ── */}
        <Node step="output" isActive={active === "output"} onClick={setActive}
          x={210} y={572} w={200} h={42} />
      </svg>

      {/* Detail panel */}
      <div
        style={{
          marginTop: 16,
          width: "100%",
          maxWidth: 580,
          background: "#12122a",
          border: `1.5px solid ${detail.color}44`,
          borderRadius: 8,
          padding: "16px 20px",
          zIndex: 1,
          minHeight: 120,
          transition: "border-color 0.3s ease",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <div
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: detail.color,
              boxShadow: `0 0 8px ${detail.color}88`,
            }}
          />
          <span style={{ color: detail.color, fontSize: 13, fontWeight: 700, letterSpacing: 1 }}>
            {detail.label}
          </span>
          <span style={{ color: "#555570", fontSize: 10 }}>
            {detail.subtitle}
          </span>
        </div>
        <pre
          style={{
            color: "#aaaacc",
            fontSize: 11,
            lineHeight: 1.6,
            margin: 0,
            whiteSpace: "pre-wrap",
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          {detail.detail}
        </pre>
      </div>

      {/* Footer */}
      <p style={{ color: "#333348", fontSize: 8, marginTop: 16, letterSpacing: 2, zIndex: 1 }}>
        ADGENAI © 2026 — PIPELINE v1.0
      </p>
    </div>
  );
}
