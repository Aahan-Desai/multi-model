"use client";

import { useCallback } from "react";
import { motion } from "framer-motion";
import { toast } from "sonner";

import { ChatInput } from "@/components/chat/chat-input";
import { ChatWindow } from "@/components/chat/chat-window";
import { AppHeader } from "@/components/common/app-header";
import { Sidebar } from "@/components/sidebar/sidebar";
import { DocumentUploadPanel } from "@/features/upload/components/document-upload-panel";
import { VisionWorkbench } from "@/features/vision/components/vision-workbench";
import { useFileDrop } from "@/hooks/use-file-drop";
import { getApiErrorMessage, isTimeoutError } from "@/lib/api";
import { getFileExtension } from "@/lib/utils";
import {
  SUPPORTED_DOCUMENT_EXTENSIONS,
  SUPPORTED_IMAGE_EXTENSIONS,
  SUPPORTED_VIDEO_EXTENSIONS,
} from "@/lib/constants";
import { useChatStore } from "@/stores/chat-store";

export function AssistantWorkspace() {
  const {
    messages,
    uploadedFiles,
    isChatLoading,
    isVisionLoading,
    isDocumentUploading,
    addLocalFiles,
    removeQueuedFile,
    resetConversation,
    sendMessage,
    uploadDocuments,
    analyzeVisionFile,
  } = useChatStore();

  const handleFilesSelected = useCallback(
    (files: File[]) => {
      const supportedExtensions = new Set([
        ...SUPPORTED_DOCUMENT_EXTENSIONS,
        ...SUPPORTED_IMAGE_EXTENSIONS,
        ...SUPPORTED_VIDEO_EXTENSIONS,
      ]);

      const supportedFiles = files.filter((file) =>
        supportedExtensions.has(
          getFileExtension(file.name) as (typeof SUPPORTED_DOCUMENT_EXTENSIONS)[number],
        ),
      );
      const rejectedFiles = files.filter(
        (file) =>
          !supportedExtensions.has(
            getFileExtension(file.name) as (typeof SUPPORTED_DOCUMENT_EXTENSIONS)[number],
          ),
      );

      if (supportedFiles.length) {
        addLocalFiles(supportedFiles);
        toast.success(`${supportedFiles.length} file(s) added to the workspace.`);
      }

      if (rejectedFiles.length) {
        toast.error(
          `${rejectedFiles.length} file(s) were skipped because they are not supported by the current backend.`,
        );
      }
    },
    [addLocalFiles],
  );

  const { isDragging, handlers } = useFileDrop({
    onFilesDropped: handleFilesSelected,
  });

  const handleChatSubmit = useCallback(
    async (value: string) => {
      try {
        await sendMessage(value);
      } catch (error) {
        const message = isTimeoutError(error)
          ? "The assistant took too long to respond."
          : getApiErrorMessage(error);
        toast.error(message);
      }
    },
    [sendMessage],
  );

  const handleDocumentUpload = useCallback(async () => {
    try {
      await uploadDocuments();
      toast.success("Document ingestion finished.");
    } catch (error) {
      toast.error(getApiErrorMessage(error));
    }
  }, [uploadDocuments]);

  const handleVisionAnalysis = useCallback(
    async (fileId: string, prompt?: string) => {
      try {
        await analyzeVisionFile(fileId, prompt);
        toast.success("Vision analysis completed.");
      } catch (error) {
        toast.error(getApiErrorMessage(error));
      }
    },
    [analyzeVisionFile],
  );

  return (
    <div className="h-screen overflow-hidden" {...handlers}>
      <div className="grid h-full md:grid-cols-[280px_minmax(0,1fr)]">
        <div className="hidden md:block">
          <Sidebar onNewChat={resetConversation} />
        </div>

        <div className="flex min-h-0 flex-col">
          <AppHeader onNewChat={resetConversation} />

          <div className="grid min-h-0 flex-1 gap-4 p-4 md:grid-cols-[minmax(0,1fr)_360px] md:p-6">
            <motion.section
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35 }}
              className="flex min-h-0 flex-col rounded-[32px] border bg-card/75 shadow-panel"
            >
              <ChatWindow
                messages={messages}
                isLoading={isChatLoading}
                onSuggestionClick={handleChatSubmit}
              />
              <div className="border-t p-4 md:p-5">
                <ChatInput
                  onSubmit={handleChatSubmit}
                  onFilesSelected={handleFilesSelected}
                  disabled={isChatLoading}
                />
              </div>
            </motion.section>

            <motion.aside
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.35, delay: 0.05 }}
              className="min-h-0 space-y-4 overflow-y-auto"
            >
              <DocumentUploadPanel
                files={uploadedFiles}
                isUploading={isDocumentUploading}
                onUpload={handleDocumentUpload}
                onRemove={removeQueuedFile}
              />
              <VisionWorkbench
                files={uploadedFiles}
                isLoading={isVisionLoading}
                onAnalyze={handleVisionAnalysis}
                onRemove={removeQueuedFile}
              />
            </motion.aside>
          </div>
        </div>
      </div>

      {isDragging ? (
        <div className="pointer-events-none absolute inset-0 z-50 flex items-center justify-center bg-background/70 backdrop-blur-sm">
          <div className="rounded-[32px] border border-primary/30 bg-card px-8 py-10 text-center shadow-panel">
            <p className="text-lg font-semibold">Drop files anywhere to add them</p>
            <p className="mt-2 text-sm text-muted-foreground">
              Documents go to RAG upload. Images and videos are staged for vision analysis.
            </p>
          </div>
        </div>
      ) : null}
    </div>
  );
}
