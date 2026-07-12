"use client";

import { KeyboardEvent, useState } from "react";
import { ArrowUp, Loader2 } from "lucide-react";

import { UploadButton } from "@/components/upload/upload-button";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

type ChatInputProps = {
  onSubmit: (value: string) => Promise<void>;
  onFilesSelected: (files: File[]) => void;
  disabled?: boolean;
  initialValue?: string;
};

export function ChatInput({
  onSubmit,
  onFilesSelected,
  disabled = false,
  initialValue = "",
}: ChatInputProps) {
  const [value, setValue] = useState(initialValue);

  const submit = async () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) {
      return;
    }

    await onSubmit(trimmed);
    setValue("");
  };

  const handleKeyDown = async (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      await submit();
    }
  };

  return (
    <div className="rounded-[28px] border bg-card p-3 shadow-panel">
      <div className="flex items-end gap-3">
        <UploadButton onFilesSelected={onFilesSelected} />
        <div className="flex-1">
          <Textarea
            value={value}
            onChange={(event) => setValue(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message the assistant. Use Ctrl/Cmd + Enter to send."
            aria-label="Chat message input"
            className="min-h-[72px] resize-none border-0 bg-transparent shadow-none focus-visible:ring-0"
          />
        </div>
        <Button
          type="button"
          size="icon"
          onClick={submit}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
        >
          {disabled ? <Loader2 className="size-4 animate-spin" /> : <ArrowUp className="size-4" />}
        </Button>
      </div>
    </div>
  );
}
