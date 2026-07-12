export type IngestionResult = {
  filename: string;
  chunks_created: number;
  vectors_uploaded: number;
};

export type UploadStatus =
  | "idle"
  | "queued"
  | "uploading"
  | "success"
  | "error";

export type UploadableKind = "document" | "image" | "video";

export type QueuedFile = {
  id: string;
  file: File;
  kind: UploadableKind;
  progress: number;
  status: UploadStatus;
  previewUrl?: string;
  errorMessage?: string;
};
