import { apiFetch } from "./client";
import type { ImportJob } from "../features/ingestion/types";

export async function uploadIngestionFile(file: File): Promise<ImportJob> {
  const formData = new FormData();
  formData.append("file", file);

  return apiFetch<ImportJob>("/ingest/file", {
    method: "POST",
    body: formData,
  });
}

export async function getIngestionJobStatus(
  jobId: string,
): Promise<ImportJob> {
  return apiFetch<ImportJob>(`/ingest/job/${jobId}/status`);
}
