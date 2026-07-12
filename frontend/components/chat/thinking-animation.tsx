import { cn } from "@/lib/utils";

type ThinkingAnimationProps = {
  className?: string;
};

export function ThinkingAnimation({ className }: ThinkingAnimationProps) {
  return (
    <div className={cn("flex items-center gap-1.5", className)} aria-hidden="true">
      {[0, 1, 2].map((index) => (
        <span
          key={index}
          className="size-2 rounded-full bg-primary/70 animate-pulseDot"
          style={{ animationDelay: `${index * 0.12}s` }}
        />
      ))}
    </div>
  );
}
