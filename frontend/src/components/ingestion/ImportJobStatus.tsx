import { useEffect } from "react";

import { useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, CircleAlert, LoaderCircle } from "lucide-react";

import {
  IMPORT_JOB_POLLING_INTERVAL_MS,
  useIngestionJob,
} from "../../features/ingestion/hooks/useIngestionJob";
import { usePosts } from "../../features/posts/hooks/usePosts";
import type {
  ImportJob,
  ImportJobStatus,
} from "../../features/ingestion/types";

const IMPORT_STEPS: Array<{ status: ImportJobStatus; label: string }> = [
  { status: "queued", label: "Queued" },
  { status: "extracting", label: "Unpacking archive" },
  { status: "parsing", label: "Reading posts" },
  { status: "geoparsing", label: "Finding locations" },
  { status: "completed", label: "Complete" },
];

const STATUS_DESCRIPTIONS: Record<ImportJobStatus, string> = {
  created: "Creating import job.",
  queued: "Upload complete. Waiting for processing to begin.",
  extracting: "Unpacking the uploaded archive.",
  parsing: "Reading posts from the archive.",
  geoparsing: "Finding locations for imported posts.",
  completed: "Import complete. The map has been refreshed with all posts.",
  failed: "The import could not be completed.",
  cancelled: "The import was cancelled.",
};

interface ImportJobStatusProps {
  initialJob: ImportJob;
  onJobUpdate: (job: ImportJob) => void;
}

function getProgress(job: ImportJob): number | undefined {
  if (
    job.total_posts !== null &&
    job.total_posts > 0 &&
    job.processed_posts !== null
  ) {
    return Math.min((job.processed_posts / job.total_posts) * 100, 100);
  }

  return undefined;
}

export function ImportJobStatus({
  initialJob,
  onJobUpdate,
}: ImportJobStatusProps) {
  const queryClient = useQueryClient();
  const jobQuery = useIngestionJob(initialJob.id);
  const job = jobQuery.data ?? initialJob;
  const isGeoparsing = job.status === "geoparsing";
  const progress = getProgress(job);
  const currentStepIndex = IMPORT_STEPS.findIndex(
    (step) => step.status === job.status,
  );

  usePosts({
    enabled: isGeoparsing,
    refetchInterval: isGeoparsing ? IMPORT_JOB_POLLING_INTERVAL_MS : false,
  });

  useEffect(() => {
    onJobUpdate(job);
  }, [job, onJobUpdate]);

  useEffect(() => {
    if (job.status === "completed") {
      void Promise.all([
        queryClient.invalidateQueries({ queryKey: ["posts"] }),
        queryClient.invalidateQueries({ queryKey: ["sources"] }),
      ]);
    }
  }, [job.status, queryClient]);

  return (
    <div aria-live="polite" className="border-t border-slate-200 pt-4">
      <div className="flex items-start gap-2">
        {job.status === "completed" ? (
          <CheckCircle2
            aria-hidden="true"
            className="mt-0.5 shrink-0 text-green-700"
            size={20}
          />
        ) : job.status === "failed" || job.status === "cancelled" ? (
          <CircleAlert
            aria-hidden="true"
            className="mt-0.5 shrink-0 text-red-700"
            size={20}
          />
        ) : (
          <LoaderCircle
            aria-hidden="true"
            className="mt-0.5 shrink-0 animate-spin text-slate-700"
            size={20}
          />
        )}
        <div>
          <h3 className="font-medium capitalize text-slate-900">
            {job.status}
          </h3>
          <p className="text-sm text-slate-600">
            {STATUS_DESCRIPTIONS[job.status]}
          </p>
        </div>
      </div>

      {progress !== undefined && (
        <div className="mt-3">
          <div className="mb-1 flex justify-between text-xs text-slate-600">
            <span>
              {job.processed_posts} of {job.total_posts} posts located
            </span>
            <span>{Math.round(progress)}%</span>
          </div>
          <progress
            className="h-2 w-full accent-slate-800"
            max={100}
            value={progress}
          >
            {Math.round(progress)}%
          </progress>
        </div>
      )}

      <ol className="mt-4 space-y-2">
        {IMPORT_STEPS.map((step, index) => {
          const isComplete = job.status === "completed" || index < currentStepIndex;
          const isCurrent = index === currentStepIndex;

          return (
            <li
              className="flex items-center gap-2 text-sm text-slate-600"
              key={step.status}
            >
              {isComplete ? (
                <CheckCircle2
                  aria-hidden="true"
                  className="shrink-0 text-green-700"
                  size={16}
                />
              ) : isCurrent ? (
                <LoaderCircle
                  aria-hidden="true"
                  className="shrink-0 animate-spin text-slate-800"
                  size={16}
                />
              ) : (
                <span
                  aria-hidden="true"
                  className="h-4 w-4 shrink-0 rounded-full border border-slate-300"
                />
              )}
              <span className={isCurrent ? "font-medium text-slate-900" : ""}>
                {step.label}
              </span>
            </li>
          );
        })}
      </ol>

      {job.status === "completed" && job.total_posts !== null && (
        <p className="mt-4 text-sm text-slate-600">
          Imported {job.total_posts} post{job.total_posts === 1 ? "" : "s"}.
        </p>
      )}
      {(job.status === "failed" || job.status === "cancelled") && (
        <p className="mt-4 text-sm text-red-700" role="alert">
          {job.error_message ?? STATUS_DESCRIPTIONS[job.status]}
        </p>
      )}
      {jobQuery.isError && (
        <div className="mt-4 text-sm text-red-700" role="alert">
          <p>Could not refresh the import status: {jobQuery.error.message}</p>
          <button
            className="mt-2 font-medium underline"
            onClick={() => {
              void jobQuery.refetch();
            }}
            type="button"
          >
            Retry status check
          </button>
        </div>
      )}
    </div>
  );
}
