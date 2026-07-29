"use client";

import { create } from "zustand";

import { sendChatMessage } from "@/services/chat";
import { analyzeVisionMedia } from "@/services/vision";
import { uploadDocument } from "@/services/upload";
import { createId, getFileExtension } from "@/lib/utils";
import {
  SUPPORTED_DOCUMENT_EXTENSIONS,
  SUPPORTED_IMAGE_EXTENSIONS,
  SUPPORTED_VIDEO_EXTENSIONS,
} from "@/lib/constants";
import type { ChatMessageModel } from "@/types/chat";
import type { QueuedFile, UploadableKind } from "@/types/upload";

type ChatStore = {
  conversationId: string;
  messages: ChatMessageModel[];
  isChatLoading: boolean;
  isVisionLoading: boolean;
  isDocumentUploading: boolean;
  uploadedFiles: QueuedFile[];
  addLocalFiles: (files: File[]) => void;
  removeQueuedFile: (id: string) => void;
  resetConversation: () => void;
  sendMessage: (query: string) => Promise<void>;
  uploadDocuments: () => Promise<void>;
  analyzeVisionFile: (fileId: string, prompt?: string) => Promise<void>;
};

function createMessage(
  role: ChatMessageModel["role"],
  content: string,
  kind: ChatMessageModel["kind"],
  title?: string,
): ChatMessageModel {
  return {
    id: createId("msg"),
    role,
    content,
    kind,
    title,
    createdAt: new Date().toISOString(),
  };
}

function classifyFile(file: File): UploadableKind {
  const extension = getFileExtension(file.name);

  if (
    SUPPORTED_DOCUMENT_EXTENSIONS.includes(
      extension as (typeof SUPPORTED_DOCUMENT_EXTENSIONS)[number],
    )
  ) {
    return "document";
  }

  if (
    SUPPORTED_IMAGE_EXTENSIONS.includes(
      extension as (typeof SUPPORTED_IMAGE_EXTENSIONS)[number],
    )
  ) {
    return "image";
  }

  return "video";
}

export const useChatStore = create<ChatStore>((set, get) => ({
  conversationId: createId("conversation"),
  messages: [],
  isChatLoading: false,
  isVisionLoading: false,
  isDocumentUploading: false,
  uploadedFiles: [],
  addLocalFiles: (files) => {
    const queuedFiles = files.map<QueuedFile>((file) => ({
      id: createId("file"),
      file,
      kind: classifyFile(file),
      progress: 0,
      status: "queued",
      previewUrl:
        file.type.startsWith("image/") || file.type.startsWith("video/")
          ? URL.createObjectURL(file)
          : undefined,
    }));

    set((state) => ({
      uploadedFiles: [...queuedFiles, ...state.uploadedFiles],
    }));
  },
  removeQueuedFile: (id) => {
    const target = get().uploadedFiles.find((item) => item.id === id);
    if (target?.previewUrl) {
      URL.revokeObjectURL(target.previewUrl);
    }

    set((state) => ({
      uploadedFiles: state.uploadedFiles.filter((item) => item.id !== id),
    }));
  },
  resetConversation: () => {
    for (const file of get().uploadedFiles) {
      if (file.previewUrl) {
        URL.revokeObjectURL(file.previewUrl);
      }
    }

    set({
      conversationId: createId("conversation"),
      messages: [],
      uploadedFiles: [],
      isChatLoading: false,
      isVisionLoading: false,
      isDocumentUploading: false,
    });
  },
  sendMessage: async (query) => {
    const trimmedQuery = query.trim();
    if (!trimmedQuery) {
      return;
    }

    set((state) => ({
      isChatLoading: true,
      messages: [...state.messages, createMessage("user", trimmedQuery, "chat")],
    }));

    try {
      const response = await sendChatMessage(trimmedQuery);
      set((state) => ({
        messages: [
          ...state.messages,
          createMessage("assistant", response.answer, "chat"),
        ],
      }));
    } finally {
      set({ isChatLoading: false });
    }
  },
  uploadDocuments: async () => {
    const pendingDocuments = get().uploadedFiles.filter(
      (item) => item.kind === "document" && item.status !== "success",
    );

    if (!pendingDocuments.length) {
      return;
    }

    set({ isDocumentUploading: true });

    try {
      for (const item of pendingDocuments) {
        set((state) => ({
          uploadedFiles: state.uploadedFiles.map((file) =>
            file.id === item.id
              ? { ...file, status: "uploading", progress: 0, errorMessage: undefined }
              : file,
          ),
        }));

        try {
          const result = await uploadDocument(item.file, (progress) => {
            set((state) => ({
              uploadedFiles: state.uploadedFiles.map((file) =>
                file.id === item.id ? { ...file, progress } : file,
              ),
            }));
          });

          set((state) => ({
            messages: [
              ...state.messages,
              createMessage(
                "system",
                `Indexed **${result.filename}** with ${result.chunks_created} chunk(s) and ${result.vectors_uploaded} vector(s).`,
                "upload",
                "Document Ready",
              ),
            ],
            uploadedFiles: state.uploadedFiles.map((file) =>
              file.id === item.id
                ? { ...file, progress: 100, status: "success" }
                : file,
            ),
          }));
        } catch (error) {
          const message = error instanceof Error ? error.message : "Upload failed.";
          set((state) => ({
            uploadedFiles: state.uploadedFiles.map((file) =>
              file.id === item.id
                ? { ...file, status: "error", errorMessage: message }
                : file,
            ),
          }));
          throw error;
        }
      }
    } finally {
      set({ isDocumentUploading: false });
    }
  },
  analyzeVisionFile: async (fileId, prompt) => {
    const target = get().uploadedFiles.find((item) => item.id === fileId);
    if (!target) {
      return;
    }

    set({
      isVisionLoading: true,
      messages: [
        ...get().messages,
        createMessage(
          "user",
          prompt?.trim() || `Analyze ${target.file.name}`,
          "vision",
          target.kind === "video" ? "Video Analysis" : "Image Analysis",
        ),
      ],
      uploadedFiles: get().uploadedFiles.map((file) =>
        file.id === fileId
          ? { ...file, status: "uploading", progress: 0, errorMessage: undefined }
          : file,
      ),
    });

    try {
      const result = await analyzeVisionMedia(target.file, prompt, (progress) => {
        set((state) => ({
          uploadedFiles: state.uploadedFiles.map((file) =>
            file.id === fileId ? { ...file, progress } : file,
          ),
        }));
      });

      set((state) => ({
        messages: [
          ...state.messages,
          createMessage("assistant", result.analysis, "vision", result.filename),
        ],
        uploadedFiles: state.uploadedFiles.map((file) =>
          file.id === fileId
            ? { ...file, status: "success", progress: 100 }
            : file,
        ),
      }));
    } finally {
      set({ isVisionLoading: false });
    }
  },
}));
