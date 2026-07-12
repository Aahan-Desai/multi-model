import type { BaseApiResponse } from "@/types/api";

export type ChatResponse = BaseApiResponse & {
  answer: string;
};

export type ConversationRole = "user" | "assistant" | "system";

export type MessageKind = "chat" | "upload" | "vision";

export type ChatMessageModel = {
  id: string;
  role: ConversationRole;
  content: string;
  createdAt: string;
  kind: MessageKind;
  title?: string;
};
