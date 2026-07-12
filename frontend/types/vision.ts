import type { BaseApiResponse } from "@/types/api";

export type VisionAnalysisResponse = BaseApiResponse & {
  filename: string;
  media_type: string;
  mime_type: string;
  file_size: number;
  analysis: string;
};
