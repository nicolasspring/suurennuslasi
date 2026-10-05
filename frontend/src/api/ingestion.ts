import { apiFetch } from "./client";
import type { ImportJob } from "../features/ingestion/types";

export interface UploadFailure {
  fileName: string;
  message: string;
}

export interface UploadIngestionFilesResult {
  jobs: ImportJob[];
  failures: UploadFailure[];
}

export async function uploadIngestionFile(file: File): Promise<ImportJob> {
  const formData = new FormData();
  formData.append("file", file);

  return apiFetch<ImportJob>("/ingest/file", {
    method: "POST",
    body: formData,
  });
}

export async function uploadIngestionFiles(
  files: File[],
): Promise<UploadIngestionFilesResult> {
  const results = await Promise.allSettled(
    files.map((file) => uploadIngestionFile(file)),
  );
  const jobs: ImportJob[] = [];
  const failures: UploadFailure[] = [];

  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      jobs.push(result.value);
      return;
    }

    failures.push({
      fileName: files[index].name,
      message:
        result.reason instanceof Error
          ? result.reason.message
          : "The upload failed with an unexpected error.",
    });
  });

  return { jobs, failures };
}

export async function getIngestionJobStatus(
  jobId: string,
): Promise<ImportJob> {
  return apiFetch<ImportJob>(`/ingest/job/${jobId}/status`);
}
