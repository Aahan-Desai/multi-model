"use client";

import { useMemo, useState } from "react";
import { Eye, Loader2 } from "lucide-react";

import { FilePreview } from "@/components/upload/file-preview";
import { ImagePreview } from "@/components/vision/image-preview";
import { VideoPreview } from "@/components/vision/video-preview";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { QueuedFile } from "@/types/upload";

type VisionPanelProps = {
  files: QueuedFile[];
  isLoading: boolean;
  onAnalyze: (fileId: string, prompt?: string) => Promise<void>;
  onRemove: (fileId: string) => void;
};

export function VisionPanel({
  files,
  isLoading,
  onAnalyze,
  onRemove,
}: VisionPanelProps) {
  const [promptByFile, setPromptByFile] = useState<Record<string, string>>({});

  const visionFiles = useMemo(
    () => files.filter((file) => file.kind === "image" || file.kind === "video"),
    [files],
  );

  return (
    <section className="rounded-[28px] border bg-card p-5 shadow-panel">
      <div className="mb-4">
        <h2 className="text-base font-semibold">Vision</h2>
        <p className="text-sm text-muted-foreground">
          Preview image and video uploads, then send them to the dedicated vision endpoint.
        </p>
      </div>

      <div className="space-y-4">
        {visionFiles.length ? (
          visionFiles.map((file) => (
            <div key={file.id} className="space-y-3">
              {file.previewUrl ? (
                file.kind === "image" ? (
                  <ImagePreview src={file.previewUrl} alt={file.file.name} />
                ) : (
                  <VideoPreview src={file.previewUrl} />
                )
              ) : null}
              <FilePreview
                file={file}
                onRemove={() => onRemove(file.id)}
                action={
                  <div className="space-y-3">
                    <Input
                      value={promptByFile[file.id] ?? ""}
                      onChange={(event) =>
                        setPromptByFile((current) => ({
                          ...current,
                          [file.id]: event.target.value,
                        }))
                      }
                      placeholder="Optional prompt, e.g. Summarize the scene and highlight anomalies."
                      aria-label={`Prompt for ${file.file.name}`}
                    />
                    <Button
                      type="button"
                      className="w-full"
                      disabled={isLoading}
                      onClick={() => onAnalyze(file.id, promptByFile[file.id])}
                    >
                      {isLoading ? (
                        <Loader2 className="mr-2 size-4 animate-spin" />
                      ) : (
                        <Eye className="mr-2 size-4" />
                      )}
                      Analyze {file.kind}
                    </Button>
                  </div>
                }
              />
            </div>
          ))
        ) : (
          <div className="rounded-2xl border border-dashed px-4 py-8 text-center text-sm text-muted-foreground">
            Add an image or video from the composer to preview and analyze it here.
          </div>
        )}
      </div>
    </section>
  );
}
