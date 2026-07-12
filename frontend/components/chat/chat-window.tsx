"use client";

import { useMemo } from "react";

import { ChatMessage } from "@/components/chat/chat-message";
import { EmptyState } from "@/components/chat/empty-state";
import { TypingIndicator } from "@/components/chat/typing-indicator";
import { useAutoScroll } from "@/hooks/use-auto-scroll";
import type { ChatMessageModel } from "@/types/chat";

type ChatWindowProps = {
  messages: ChatMessageModel[];
  isLoading: boolean;
  onSuggestionClick: (value: string) => void;
};

export function ChatWindow({
  messages,
  isLoading,
  onSuggestionClick,
}: ChatWindowProps) {
  const endRef = useAutoScroll(messages.length + Number(isLoading));

  const hasMessages = useMemo(() => messages.length > 0, [messages.length]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 md:px-6">
      {!hasMessages ? (
        <EmptyState onSuggestionClick={onSuggestionClick} />
      ) : (
        <div className="space-y-5">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading ? <TypingIndicator /> : null}
          <div ref={endRef} />
        </div>
      )}
    </div>
  );
}
