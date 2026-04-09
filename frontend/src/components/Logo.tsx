import Image from "next/image";

interface LogoProps {
  /** Height in pixels — width scales proportionally (1:1 source) */
  height?: number;
  className?: string;
}

/**
 * Astreli logo image component.
 * Source is 1024×1024 (square — includes icon + wordmark).
 */
export default function Logo({ height = 40, className }: LogoProps) {
  return (
    <Image
      src="/logo.png"
      alt="Astreli"
      width={height}
      height={height}
      className={className}
      priority
    />
  );
}
