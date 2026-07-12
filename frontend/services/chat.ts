import { api } from "@/lib/api";
import type { ChatResponse } from "@/types/chat";

export async function sendChatMessage(query: string) {
  const response = await api.post<ChatResponse>("/chat", {
    query,
  });

  return response.data;
}
