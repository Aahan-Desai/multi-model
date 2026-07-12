"use client";

import { Clock3, MessagesSquare, Plus, Settings2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const historyItems = [
  "RAG knowledge base draft",
  "Image analysis walkthrough",
  "Math and reasoning session",
];

type SidebarProps = {
  onNewChat: () => void;
};

export function Sidebar({ onNewChat }: SidebarProps) {
  return (
    <aside className="flex h-full flex-col border-r bg-card/80 px-4 py-5 backdrop-blur">
      <div className="flex items-center gap-3 px-2 pb-6">
        <div className="rounded-2xl bg-primary/10 p-2 text-primary">
          <MessagesSquare className="size-5" />
        </div>
        <div>
          <p className="text-sm font-semibold">Assistant Console</p>
          <p className="text-xs text-muted-foreground">
            Production-ready operator view
          </p>
        </div>
      </div>

      <Button onClick={onNewChat} className="justify-start rounded-xl">
        <Plus className="mr-2 size-4" />
        New Chat
      </Button>

      <div className="mt-8 flex-1">
        <div className="mb-3 flex items-center gap-2 px-2 text-xs uppercase tracking-[0.24em] text-muted-foreground">
          <Clock3 className="size-3.5" />
          Recent Conversations
        </div>
        <div className="space-y-2">
          {historyItems.map((item, index) => (
            <button
              key={item}
              type="button"
              className={cn(
                "w-full rounded-xl border border-transparent px-3 py-3 text-left transition",
                index === 0
                  ? "bg-secondary text-secondary-foreground"
                  : "text-muted-foreground hover:border-border hover:bg-secondary/60 hover:text-foreground",
              )}
            >
              <p className="truncate text-sm font-medium">{item}</p>
              <p className="mt-1 text-xs">
                Placeholder for future multi-chat history.
              </p>
            </button>
          ))}
        </div>
      </div>

      <button
        type="button"
        className="mt-6 flex items-center gap-3 rounded-xl border border-border/70 px-3 py-3 text-left text-sm text-muted-foreground transition hover:bg-secondary/70 hover:text-foreground"
      >
        <Settings2 className="size-4" />
        Settings placeholder
      </button>
    </aside>
  );
}
