"use client";

import type { ReactNode } from "react";
import { FileText, ImageIcon, TriangleAlert, Video } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { formatFileSize } from "@/lib/utils";
import type { QueuedFile } from "@/types/upload";

type FilePreviewProps = {
  file: QueuedFile;
  onRemove: () => void;
  action?: ReactNode;
};

function getFileIcon(kind: QueuedFile["kind"]) {
  switch (kind) {
    case "document":
      return <FileText className="size-4" />;
    case "image":
      return <ImageIcon className="size-4" />;
    case "video":
      return <Video className="size-4" />;
  }
}

export function FilePreview({ file, onRemove, action }: FilePreviewProps) {
  return (
    <div className="rounded-2xl border bg-background/70 p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="rounded-xl bg-secondary p-2">{getFileIcon(file.kind)}</div>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium">{file.file.name}</p>
            <p className="mt-1 text-xs text-muted-foreground">
              {formatFileSize(file.file.size)}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={file.status === "error" ? "destructive" : "secondary"}>
            {file.status}
          </Badge>
          <Button type="button" size="sm" variant="ghost" onClick={onRemove}>
            Remove
          </Button>
        </div>
      </div>

      {typeof file.progress === "number" && file.status !== "queued" ? (
        <div className="mt-4 space-y-2">
          <Progress value={file.progress} />
          <p className="text-xs text-muted-foreground">{file.progress}% uploaded</p>
        </div>
      ) : null}

      {file.errorMessage ? (
        <div className="mt-3 flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/10 px-3 py-2 text-xs text-danger">
          <TriangleAlert className="mt-0.5 size-4 shrink-0" />
          <span>{file.errorMessage}</span>
        </div>
      ) : null}

      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}
