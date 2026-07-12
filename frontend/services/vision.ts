import { api } from "@/lib/api";
import type { VisionAnalysisResponse } from "@/types/vision";

export async function analyzeVisionMedia(
  file: File,
  prompt?: string,
  onProgress?: (progress: number) => void,
) {
  const formData = new FormData();
  formData.append("file", file);

  if (prompt) {
    formData.append("prompt", prompt);
  }

  const response = await api.post<VisionAnalysisResponse>(
    "/vision/analyze",
    formData,
    {
      onUploadProgress(progressEvent) {
        if (!progressEvent.total || !onProgress) {
          return;
        }

        onProgress(Math.round((progressEvent.loaded / progressEvent.total) * 100));
      },
    },
  );

  return response.data;
}
