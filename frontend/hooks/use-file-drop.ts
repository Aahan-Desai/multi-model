"use client";

import type { DragEvent } from "react";
import { useMemo, useState } from "react";

type UseFileDropOptions = {
  onFilesDropped: (files: File[]) => void;
};

export function useFileDrop({ onFilesDropped }: UseFileDropOptions) {
  const [isDragging, setIsDragging] = useState(false);

  const handlers = useMemo(
    () => ({
      onDragEnter: (event: DragEvent<HTMLElement>) => {
        event.preventDefault();
        setIsDragging(true);
      },
      onDragOver: (event: DragEvent<HTMLElement>) => {
        event.preventDefault();
        if (!isDragging) {
          setIsDragging(true);
        }
      },
      onDragLeave: (event: DragEvent<HTMLElement>) => {
        event.preventDefault();

        if (event.currentTarget === event.target) {
          setIsDragging(false);
        }
      },
      onDrop: (event: DragEvent<HTMLElement>) => {
        event.preventDefault();
        setIsDragging(false);

        const files = Array.from(event.dataTransfer.files ?? []);
        if (files.length) {
          onFilesDropped(files);
        }
      },
    }),
    [isDragging, onFilesDropped],
  );

  return {
    isDragging,
    handlers,
  };
}
