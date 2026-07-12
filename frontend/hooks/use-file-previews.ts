"use client";

import { useEffect, useMemo } from "react";

import type { QueuedFile } from "@/types/upload";

type UseFilePreviewsOptions = {
  files: File[];
  classifyFile: (file: File) => QueuedFile["kind"];
};

export function useFilePreviews({
  files,
  classifyFile,
}: UseFilePreviewsOptions) {
  const items = useMemo(
    () =>
      files.map((file) => {
        const kind = classifyFile(file);
        const previewUrl =
          kind === "image" || kind === "video"
            ? URL.createObjectURL(file)
            : undefined;

        return {
          file,
          kind,
          previewUrl,
        };
      }),
    [classifyFile, files],
  );

  useEffect(() => {
    return () => {
      for (const item of items) {
        if (item.previewUrl) {
          URL.revokeObjectURL(item.previewUrl);
        }
      }
    };
  }, [items]);

  return items;
}
