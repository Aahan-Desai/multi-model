"use client";

import { Paperclip } from "lucide-react";
import { useRef } from "react";

import { Button } from "@/components/ui/button";

type UploadButtonProps = {
  onFilesSelected: (files: File[]) => void;
};

export function UploadButton({ onFilesSelected }: UploadButtonProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        multiple
        hidden
        onChange={(event) => {
          const files = Array.from(event.target.files ?? []);
          if (files.length) {
            onFilesSelected(files);
            event.target.value = "";
          }
        }}
      />
      <Button
        type="button"
        variant="outline"
        size="icon"
        aria-label="Upload files"
        onClick={() => inputRef.current?.click()}
      >
        <Paperclip className="size-4" />
      </Button>
    </>
  );
}
