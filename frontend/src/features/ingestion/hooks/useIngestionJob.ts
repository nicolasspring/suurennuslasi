import { useQuery } from "@tanstack/react-query";

import { getIngestionJobStatus } from "../../../api/ingestion";

import type { ImportJobStatus } from "../types";

export const IMPORT_JOB_POLLING_INTERVAL_MS = 2_000;

export function isTerminalImportJobStatus(status: ImportJobStatus): boolean {
  return (
    status === "completed" || status === "failed" || status === "cancelled"
  );
}

export function useIngestionJob(jobId: string | undefined) {
  return useQuery({
    queryKey: ["ingestion-job", jobId],
    queryFn: () => {
      if (!jobId) {
        throw new Error("An import job ID is required to check its status.");
      }

      return getIngestionJobStatus(jobId);
    },
    enabled: jobId !== undefined,
    retry: 2,
    refetchInterval: (query) => {
      const status = query.state.data?.status;

      return status && isTerminalImportJobStatus(status)
        ? false
        : IMPORT_JOB_POLLING_INTERVAL_MS;
    },
  });
}
