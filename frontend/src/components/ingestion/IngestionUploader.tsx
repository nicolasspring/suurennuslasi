import { useEffect, useState } from "react";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, CircleAlert, LoaderCircle, Upload } from "lucide-react";

import { uploadIngestionFile } from "../../api/ingestion";
import {
  IMPORT_JOB_POLLING_INTERVAL_MS,
  isTerminalImportJobStatus,
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

export function IngestionUploader() {
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string>();
  const [selectionError, setSelectionError] = useState<string>();

  const uploadMutation = useMutation({
    mutationFn: uploadIngestionFile,
    onSuccess: (job) => {
      setJobId(job.id);
    },
  });
  const jobQuery = useIngestionJob(jobId);
  const job = jobQuery.data ?? (jobId ? uploadMutation.data : undefined);
  const isProcessing =
    uploadMutation.isPending ||
    (job !== undefined && !isTerminalImportJobStatus(job.status));
  const isGeoparsing = job?.status === "geoparsing";
  const progress = job ? getProgress(job) : undefined;

  usePosts({
    enabled: isGeoparsing,
    refetchInterval: isGeoparsing ? IMPORT_JOB_POLLING_INTERVAL_MS : false,
  });

  useEffect(() => {
    if (job?.status === "completed") {
      void queryClient.invalidateQueries({ queryKey: ["posts"] });
    }
  }, [job?.status, queryClient]);

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setSelectionError(undefined);
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setSelectionError("Choose a ZIP archive before starting the import.");
      return;
    }

    setJobId(undefined);
    uploadMutation.reset();
    uploadMutation.mutate(selectedFile);
  }

  const currentStepIndex = job
    ? IMPORT_STEPS.findIndex((step) => step.status === job.status)
    : -1;

  return (
    <section
      aria-label="Import posts"
      className="w-[min(24rem,calc(100vw-2rem))] rounded-lg bg-white p-4 shadow-lg"
    >
      <h1 className="text-lg font-semibold text-slate-900">Import posts</h1>
      <p className="mt-1 text-sm text-slate-600">
        Upload an Instagram ZIP archive to add its posts to the map.
      </p>

      <form className="mt-4 space-y-3" onSubmit={handleSubmit}>
        <label className="block text-sm font-medium text-slate-800" htmlFor="archive">
          ZIP archive
        </label>
        <input
          accept=".zip,application/zip,application/x-zip-compressed"
          aria-describedby="archive-help"
          className="block w-full cursor-pointer rounded border border-slate-300 bg-white text-sm text-slate-700 file:mr-3 file:cursor-pointer file:border-0 file:bg-slate-100 file:px-3 file:py-2 file:text-sm file:font-medium file:text-slate-800 hover:file:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isProcessing}
          id="archive"
          onChange={handleFileChange}
          type="file"
        />
        <p className="text-xs text-slate-500" id="archive-help">
          Processing starts after the upload finishes.
        </p>
        {selectionError && (
          <p className="text-sm text-red-700" role="alert">
            {selectionError}
          </p>
        )}
        {uploadMutation.isError && (
          <p className="text-sm text-red-700" role="alert">
            Upload failed: {uploadMutation.error.message}
          </p>
        )}
        <button
          className="inline-flex w-full items-center justify-center gap-2 rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          disabled={isProcessing}
          type="submit"
        >
          {uploadMutation.isPending ? (
            <LoaderCircle aria-hidden="true" className="animate-spin" size={18} />
          ) : (
            <Upload aria-hidden="true" size={18} />
          )}
          {uploadMutation.isPending ? "Uploading archive..." : "Start import"}
        </button>
      </form>

      {job && (
        <div aria-live="polite" className="mt-5 border-t border-slate-200 pt-4">
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
              <h2 className="font-medium capitalize text-slate-900">
                {job.status}
              </h2>
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
              const isComplete =
                job.status === "completed" || index < currentStepIndex;
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
      )}
    </section>
  );
}
