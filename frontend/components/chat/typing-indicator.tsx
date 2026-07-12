import { ThinkingAnimation } from "@/components/chat/thinking-animation";

export function TypingIndicator() {
  return (
    <div className="flex items-center gap-3 rounded-2xl border bg-card px-4 py-3 shadow-panel">
      <div className="rounded-full bg-primary/10 px-2 py-1 text-xs font-semibold text-primary">
        Assistant
      </div>
      <ThinkingAnimation />
      <span className="text-sm text-muted-foreground">Thinking...</span>
    </div>
  );
}
