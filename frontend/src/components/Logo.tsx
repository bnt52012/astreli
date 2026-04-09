import Image from "next/image";

interface LogoProps {
  /** Height in pixels — width scales proportionally */
  height?: number;
  className?: string;
}

/**
 * Astreli logo image component.
 * Original aspect ratio is ~5:1 (467×93).
 */
export default function Logo({ height = 32, className }: LogoProps) {
  const width = Math.round(height * (467 / 93));

  return (
    <Image
      src="/logo.png"
      alt="Astreli"
      width={width}
      height={height}
      className={className}
      priority
    />
  );
}
