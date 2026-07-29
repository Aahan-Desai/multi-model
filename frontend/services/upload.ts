import { api } from "@/lib/api";
import type { IngestionResult } from "@/types/upload";

export async function uploadDocument(
  file: File,
  onProgress?: (progress: number) => void,
) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<IngestionResult>("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress(progressEvent) {
      if (!progressEvent.total || !onProgress) {
        return;
      }

      onProgress(Math.round((progressEvent.loaded / progressEvent.total) * 100));
    },
  });

  return response.data;
}
