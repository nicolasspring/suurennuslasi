export type ImportJobStatus =
  | "created"
  | "queued"
  | "extracting"
  | "parsing"
  | "geoparsing"
  | "completed"
  | "failed"
  | "cancelled";

export interface ImportJob {
  id: string;
  status: ImportJobStatus;
  progress: number | null;
  created_at: string;
  last_edited: string;
  started_at: string | null;
  finished_at: string | null;
  total_posts: number | null;
  processed_posts: number | null;
  error_message: string | null;
}
