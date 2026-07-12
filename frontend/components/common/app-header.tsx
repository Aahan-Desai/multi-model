"use client";

import { PanelLeftOpen, Search, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

type AppHeaderProps = {
  onNewChat: () => void;
};

export function AppHeader({ onNewChat }: AppHeaderProps) {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b bg-background/85 px-4 py-4 backdrop-blur md:px-6">
      <div className="flex items-center gap-3">
        <div className="rounded-2xl bg-primary/10 p-2 text-primary">
          <Sparkles className="size-5" />
        </div>
        <div>
          <p className="text-sm font-semibold tracking-wide text-foreground">
            Multi-Model AI Orchestrator
          </p>
          <p className="text-xs text-muted-foreground">
            Chat, retrieval, vision, search, and math in one workspace.
          </p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Badge variant="secondary" className="hidden md:inline-flex">
          Ready for streaming
        </Badge>
        <Button variant="outline" size="sm" className="hidden md:inline-flex">
          <Search className="mr-2 size-4" />
          Settings
        </Button>
        <Button size="sm" onClick={onNewChat}>
          <PanelLeftOpen className="mr-2 size-4" />
          New Chat
        </Button>
      </div>
    </header>
  );
}
