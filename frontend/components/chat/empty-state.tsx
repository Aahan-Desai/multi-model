import { DEFAULT_CHAT_SUGGESTIONS } from "@/lib/constants";

type EmptyStateProps = {
  onSuggestionClick: (value: string) => void;
};

export function EmptyState({ onSuggestionClick }: EmptyStateProps) {
  return (
    <div className="mx-auto flex max-w-3xl flex-col items-center justify-center px-6 py-16 text-center">
      <div className="rounded-3xl border bg-card/80 px-5 py-3 text-sm text-muted-foreground shadow-panel">
        Multi-capability assistant workspace
      </div>
      <h1 className="mt-6 text-balance text-4xl font-semibold tracking-tight md:text-5xl">
        Route questions, documents, images, and videos through one interface.
      </h1>
      <p className="mt-4 max-w-2xl text-pretty text-base text-muted-foreground md:text-lg">
        The frontend sends chat, upload, and vision requests to the existing
        FastAPI backend exactly as implemented, while keeping the UI modular
        enough for future streaming, traces, and multi-conversation support.
      </p>
      <div className="mt-10 grid w-full gap-3 md:grid-cols-2">
        {DEFAULT_CHAT_SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            type="button"
            onClick={() => onSuggestionClick(suggestion)}
            className="rounded-2xl border bg-background/70 px-4 py-4 text-left transition hover:border-primary/40 hover:bg-secondary/50"
          >
            <p className="text-sm font-medium">{suggestion}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
