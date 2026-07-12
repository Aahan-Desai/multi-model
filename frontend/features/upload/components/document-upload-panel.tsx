"use client";

import { Database, Loader2 } from "lucide-react";

import { FilePreview } from "@/components/upload/file-preview";
import { Button } from "@/components/ui/button";
import type { QueuedFile } from "@/types/upload";

type DocumentUploadPanelProps = {
  files: QueuedFile[];
  isUploading: boolean;
  onUpload: () => Promise<void>;
  onRemove: (fileId: string) => void;
};

export function DocumentUploadPanel({
  files,
  isUploading,
  onUpload,
  onRemove,
}: DocumentUploadPanelProps) {
  const documentFiles = files.filter((file) => file.kind === "document");

  return (
    <section className="rounded-[28px] border bg-card p-5 shadow-panel">
      <div className="mb-4">
        <h2 className="text-base font-semibold">Document Upload</h2>
        <p className="text-sm text-muted-foreground">
          Drag in PDFs, DOCX, TXT, CSV, and other supported files for RAG ingestion.
        </p>
      </div>

      <div className="space-y-4">
        {documentFiles.length ? (
          <>
            {documentFiles.map((file) => (
              <FilePreview
                key={file.id}
                file={file}
                onRemove={() => onRemove(file.id)}
              />
            ))}
            <Button
              type="button"
              className="w-full"
              onClick={onUpload}
              disabled={isUploading}
            >
              {isUploading ? (
                <Loader2 className="mr-2 size-4 animate-spin" />
              ) : (
                <Database className="mr-2 size-4" />
              )}
              Upload Documents
            </Button>
          </>
        ) : (
          <div className="rounded-2xl border border-dashed px-4 py-8 text-center text-sm text-muted-foreground">
            Add one or more document files from the composer to stage them here.
          </div>
        )}
      </div>
    </section>
  );
}
